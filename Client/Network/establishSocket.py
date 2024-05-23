import socket

class SocketClient:

  def __init__(self, host, port):
    """Hàm khởi tạo"""
    self.host = '192.168.1.6'
    self.port = 5678

  def connect(self):
    """Kết nối với Server"""
    try:
      self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.socket.connect((self.host, self.port))
      print(f"Kết nối thành công với Server {self.host} trên cổng {self.port}")
    except socket.error as e:
      print(f"Lỗi kết nối: {e}")

  def send(self, message):
    """Gửi dữ liệu đến Server"""
    try:
      self.socket.sendall(message.encode())
      print(f"Đã gửi dữ liệu: {message}")
    except socket.error as e:
      print(f"Lỗi gửi dữ liệu: {e}")

  def receive(self, buffer_size=1024):
    """Nhận dữ liệu từ Server"""
    try:
      data = self.socket.recv(buffer_size)
      if data:
        return data.decode()
      else:
        print("Kết nối đã bị đóng")
        return None
    except socket.error as e:
      print(f"Lỗi nhận dữ liệu: {e}")
      return None

  def close(self):
    if self.socket:
      self.socket.close()
      print("Đã đóng kết nối")

