# 🤟 Vietnamese Sign Language Recognition using ST-GCN

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/PyTorch-2.0+-EE4C2C?logo=pytorch&logoColor=white" alt="PyTorch"/>
  <img src="https://img.shields.io/badge/CUDA-Enabled-76B900?logo=nvidia&logoColor=white" alt="CUDA"/>
  <img src="https://img.shields.io/badge/Accuracy-81%25-brightgreen" alt="Accuracy"/>
</p>

## 📖 Overview

A deep learning-based **Vietnamese Sign Language Recognition (SLR)** system that processes real-time video input to detect and translate sign language gestures. The project leverages **Spatial-Temporal Graph Convolutional Networks (ST-GCN)** for skeleton-based action recognition, achieving **81% test accuracy** on 64 sign language classes.

> **PBL5 Project (2024)** - Danang University of Science and Technology

## 🌟 Key Features

- 🎥 **Real-time Recognition**: Live camera-based sign language detection
- 🦴 **Skeleton-based Approach**: Uses MoveNet for 17-point body pose estimation
- 🧠 **ST-GCN Architecture**: State-of-the-art spatial-temporal graph convolutions
- 📱 **Client-Server Architecture**: Scalable deployment with separate frontend/backend
- 🔤 **64 Sign Classes**: Comprehensive vocabulary for basic communication

## 🏗️ System Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│    Camera       │────▶│   MoveNet        │────▶│    ST-GCN       │
│  (Video Input)  │     │ (Pose Estimation)│     │   (Recognition) │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                                                         │
                                                         ▼
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   User Display  │◀────│   Text/Speech    │◀────│  Classification │
│   (Result)      │     │   Conversion     │     │  (64 classes)   │
└─────────────────┘     └──────────────────┘     └─────────────────┘
```

## 🧠 Model Details

### ST-GCN (Spatial-Temporal Graph Convolutional Network)

The model treats human skeleton as a graph structure where:
- **Nodes**: 17 body keypoints (joints)
- **Edges**: Natural connections between joints (18 edges)
- **Temporal Dimension**: 58 frames per sequence

| Parameter | Value |
|-----------|-------|
| Input Shape | `(batch, 58, 17, 3)` |
| Output Classes | 64 |
| Total Parameters | 1,709,682 |
| Temporal Kernel Size | 9 |
| Hop Size | 2 |
| ST-GCN Blocks | 5 |

### Body Keypoints (MoveNet)

```
        0: Nose
      /   \
   1-2: Eyes      3-4: Ears
      \   /
     5-6: Shoulders
      |   |
    7-8: Elbows
      |   |
   9-10: Wrists
      \ /
   11-12: Hips
      |   |
  13-14: Knees
      |   |
  15-16: Ankles
```

## 📊 Training Results

### Hyperparameters

| Parameter | Value |
|-----------|-------|
| Batch Size | 64 |
| Epochs | 30 |
| Learning Rate | 1e-4 |
| Optimizer | AdamW |
| β₁, β₂ | 0.9, 0.999 |
| Weight Decay | 1e-5 |
| Device | CUDA |

### Performance Metrics

| Dataset | Accuracy | Loss |
|---------|----------|------|
| Train | **92%** | 0.25 |
| Validation | 72% | 1.11 |
| **Test** | **81%** | 0.62 |

> 🎯 **Real-world performance**: 85-90% recognition accuracy at 20-25 FPS

## 🛠️ Tech Stack

- **Deep Learning**: PyTorch, CUDA
- **Pose Estimation**: TensorFlow Lite (MoveNet)
- **Frontend**: React / React Native
- **Backend**: FastAPI / Flask
- **Computer Vision**: OpenCV, MediaPipe

## 🚀 Getting Started

### Prerequisites

```bash
# Python 3.8+
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install opencv-python numpy tensorflow-lite
```

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/sign-language-recognition.git
cd sign-language-recognition

# Install dependencies
pip install -r requirements.txt
```

### Usage

```bash
# Start the recognition server
python server/main.py

# Run real-time recognition
python client/camera.py
```

## 📁 Project Structure

```
sign-language-recognition/
├── 📂 models/
│   ├── st_gcn.py           # ST-GCN model architecture
│   ├── movenet.py          # Pose estimation module
│   └── checkpoints/        # Trained weights
├── 📂 data/
│   ├── train/              # Training dataset
│   ├── valid/              # Validation dataset
│   └── test/               # Test dataset
├── 📂 client/
│   ├── camera.py           # Camera capture module
│   └── ui/                 # User interface
├── 📂 server/
│   ├── main.py             # API server
│   └── inference.py        # Model inference
├── 📂 utils/
│   ├── preprocessing.py    # Data preprocessing
│   └── visualization.py    # Result visualization
├── train.py                # Training script
├── evaluate.py             # Evaluation script
└── requirements.txt
```

## 🔬 Technical Details

### Loss Function: CrossEntropyLoss

```math
L = -\sum_{c=1}^{64} y_c \log(p_c)
```

Where `y` is the ground truth distribution and `p` is the predicted probability.

### Optimizer: AdamW

AdamW decouples weight decay from gradient updates, providing:
- Better regularization control
- Improved training stability
- Superior performance on large models

## 🎯 Use Cases

1. **Communication Aid**: Real-time translation for deaf/hearing-impaired individuals
2. **Education**: Sign language learning and practice tool
3. **Smart Home Control**: Gesture-based device control
4. **Accessibility**: Integration with video conferencing platforms

## 📈 Future Improvements

- [ ] Expand vocabulary to 200+ sign classes
- [ ] Add support for continuous sentence recognition
- [ ] Implement attention mechanisms for improved accuracy
- [ ] Deploy on mobile devices with TensorFlow Lite
- [ ] Add support for multiple sign languages

## 📚 References

1. Yan, S., Xiong, Y., & Lin, D. (2018). *Spatial Temporal Graph Convolutional Networks for Skeleton-Based Action Recognition*. AAAI.
2. Loshchilov, I., & Hutter, F. (2019). *Decoupled Weight Decay Regularization*. ICLR.
3. Google MoveNet: Ultra fast and accurate pose detection model.

## 👥 Authors

**PBL5 Team - ĐHBK Đà Nẵng (2024)**

---

<p align="center">
  Made with ❤️ for the Deaf Community
</p>
