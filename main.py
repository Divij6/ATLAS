# import torch
# print(torch.__version__)           # should show +cu121
# print(torch.cuda.is_available())   # should be True
# print(torch.cuda.get_device_name(0))

import cv2
img_path = r"D:\DRDO\AggressivePosture\test\images\2_jpg.rf.a740882e5a4c0991724aa0225431d237.jpg"
img = cv2.imread(img_path)
print("Image loaded:", img )
