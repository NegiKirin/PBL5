import os

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


current_directory = os.path.dirname(os.path.abspath(__file__)) + '\\'

# MoveNet Pose 6 Point => 5 edges
NEIGHBOR_BASE = [ (0, 2), (2, 4), (1, 3), (3, 5), (0, 1) ]

class Graph():
  def __init__(self, hop_size):

    self.get_edge()
    self.hop_size = hop_size # để định rõ khoảng cách giữa các frame hoặc thời điểm lấy mẫu liên tiếp
    self.hop_dis = self.get_hop_distance(self.num_node, self.edge, hop_size=hop_size)


    self.get_adjacency()

  # Phương thức này trả về một chuỗi biểu diễn của ma trận kết nối (adjacency matrix) của đồ thị.
  def __str__(self):
    return self.A

  # Phương thức này được sử dụng để xác định các cạnh của đồ thị
  def get_edge(self):
    self.num_node = 6
    self_link = [(i, i) for i in range(self.num_node)] # ループ
    neighbor_base = NEIGHBOR_BASE
    neighbor_link = [(i , j ) for (i, j) in neighbor_base]
    self.edge = self_link + neighbor_link

  # Phương thức này tính toán ma trận kết nối của đồ thị dựa
  def get_adjacency(self):
    valid_hop = range(0, self.hop_size + 1, 1)
    adjacency = np.zeros((self.num_node, self.num_node))
    for hop in valid_hop:
        adjacency[self.hop_dis == hop] = 1
    normalize_adjacency = self.normalize_digraph(adjacency)
    A = np.zeros((len(valid_hop), self.num_node, self.num_node))
    for i, hop in enumerate(valid_hop):
        A[i][self.hop_dis == hop] = normalize_adjacency[self.hop_dis == hop]
    self.A = A

  # Phương thức này tính toán khoảng cách (hop distance) giữa các nút trong đồ thị
  def get_hop_distance(self, num_node, edge, hop_size):
    A = np.zeros((num_node, num_node))
    for i, j in edge:
        A[j, i] = 1
        A[i, j] = 1
    hop_dis = np.zeros((num_node, num_node)) + np.inf
    transfer_mat = [np.linalg.matrix_power(A, d) for d in range(hop_size + 1)]
    arrive_mat = (np.stack(transfer_mat) > 0)
    for d in range(hop_size, -1, -1):
        hop_dis[arrive_mat[d]] = d
    return hop_dis

  # Phương thức này được sử dụng để chuẩn hóa ma trận kết nối của đồ thị
  def normalize_digraph(self, A):
    Dl = np.sum(A, 0)
    num_node = A.shape[0]
    Dn = np.zeros((num_node, num_node))
    for i in range(num_node):
        if Dl[i] > 0:
            Dn[i, i] = Dl[i]**(-1)
    DAD = np.dot(A, Dn)
    return DAD

class SpatialGraphConvolution(nn.Module):
  def __init__(self, in_channels, out_channels, s_kernel_size):
    super().__init__()
    self.s_kernel_size = s_kernel_size
    self.conv = nn.Conv2d(in_channels=in_channels,
                          out_channels=out_channels * s_kernel_size,
                          kernel_size=1)

  def forward(self, x, A):
    x = self.conv(x)
    n, kc, t, v = x.size()
    x = x.view(n, self.s_kernel_size, kc//self.s_kernel_size, t, v)
    x = torch.einsum('nkctv,kvw->nctw', (x, A))
    return x.contiguous()

class STGC_block(nn.Module):
  def __init__(self, in_channels, out_channels, stride, t_kernel_size, A_size, dropout=0.25):
    super().__init__()
    self.sgc = SpatialGraphConvolution(in_channels=in_channels,
                                       out_channels=out_channels,
                                       s_kernel_size=A_size[0])

    self.M = nn.Parameter(torch.ones(A_size))

    self.tgc = nn.Sequential(nn.BatchNorm2d(out_channels),
                            nn.ReLU(),
                            nn.Dropout(dropout),
                            nn.Conv2d(out_channels,
                                      out_channels,
                                      (t_kernel_size, 1),
                                      (stride, 1),
                                      ((t_kernel_size - 1) // 2, 0)),
                            nn.BatchNorm2d(out_channels),
                            nn.ReLU())

  def forward(self, x, A):
    x = self.tgc(self.sgc(x, A * self.M))
    return x
class ST_GCN(nn.Module):
  def __init__(self, num_classes, in_channels, t_kernel_size, hop_size):
    super().__init__()

    graph = Graph(hop_size)
    A = torch.tensor(graph.A, dtype=torch.float32, requires_grad=False)
    self.register_buffer('A', A)
    A_size = A.size()

    # Batch Normalization
    self.bn = nn.BatchNorm1d(in_channels * A_size[1])

    # STGC_blocks
    self.stgc1 = STGC_block(in_channels, 32, 1, t_kernel_size, A_size)
    self.stgc2 = STGC_block(32, 64, 2, t_kernel_size, A_size)
    self.stgc3 = STGC_block(64, 128, 2, t_kernel_size, A_size)
    self.stgc4 = STGC_block(128, 256, 1, t_kernel_size, A_size)
    # self.stgc5 = STGC_block(256, 256, 1, t_kernel_size, A_size)
    # self.stgc6 = STGC_block(64, 128, 1, t_kernel_size, A_size)
    # self.stgc7 = STGC_block(128, 128, 1, t_kernel_size, A_size)
    # self.stgc8 = STGC_block(128, 256, 1, t_kernel_size, A_size)
    # self.stgc9 = STGC_block(256, 256, 1, t_kernel_size, A_size)
    # self.stgc10 = STGC_block(256, 512, 1, t_kernel_size, A_size)
    # self.stgc11 = STGC_block(512, 512, 1, t_kernel_size, A_size)

    # Prediction
    # self.fc1 = nn.Conv2d(512, 256, kernel_size=1)
    # self.fc2 = nn.Conv2d(256, 128, kernel_size=1)
    self.fc3 = nn.Conv2d(256, num_classes, kernel_size=1)

  def forward(self, x):
    # Batch Normalization
    N, C, T, V = x.size() # batch, channel, frame, node
    x = x.permute(0, 3, 1, 2).contiguous().view(N, V * C, T)
    # x = self.bn(x)
    x = x.view(N, V, C, T).permute(0, 2, 3, 1).contiguous()

    # STGC_blocks
    x = self.stgc1(x, self.A)
    x = self.stgc2(x, self.A)
    x = self.stgc3(x, self.A)
    x = self.stgc4(x, self.A)
    # x = self.stgc5(x, self.A)
    # x = self.stgc6(x, self.A)
    # x = self.stgc7(x, self.A)
    # x = self.stgc8(x, self.A)
    # x = self.stgc9(x, self.A)
    # x = self.stgc10(x, self.A)
    # x = self.stgc11(x, self.A)

    # Prediction
    x = F.avg_pool2d(x, x.size()[2:])
    x = x.view(N, -1, 1, 1)
    # x = self.fc1(x)
    # x = self.fc2(x)
    x = self.fc3(x)
    x = x.view(x.size(0), -1)
    return x

def load_model():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Load model
    FILE = current_directory + './model_64.pth'
    loaded_model = torch.load(FILE)
    loaded_model = loaded_model.to(device)
    loaded_model.eval()

    return loaded_model, device

# model, device = load_model()
# print(f'device: {device}')
# print(f'model: {model}')


