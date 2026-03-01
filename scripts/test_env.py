import torch
import cv2
import numpy as np

print("Torch OK :", torch.__version__)
print("CUDA disponible :", torch.cuda.is_available())
print("OpenCV OK :", cv2.__version__)

img = np.zeros((224,224,3))
print("Image test shape :", img.shape)