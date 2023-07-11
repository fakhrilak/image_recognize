import os
from demo import init_model,cv_imread,get_plate_result
import torch
import cv2
from datetime import datetime
device =torch.device("cpu")
for i in os.listdir("/data/BACKEND/LPR_IMG/true"):
    print(i)
    crnn = init_model(device,"/data/image_recognize/crnn_plate_recognition/saved_model/learn2.pth")
    img = cv_imread("/data/BACKEND/LPR_IMG/true/"+i)
    img = cv2.cvtColor(img,cv2.COLOR_BGRA2BGR)
    plate=get_plate_result(img, device,crnn, (48,168))
    dt = datetime.now()
    dt_str = dt.strftime('%Y-%m-%d-%H:%M:%S')
    os.system("mv /data/BACKEND/LPR_IMG/true/"+i+\
    "  /data/BACKEND/LPR_IMG/true/"+plate+"_"+dt_str+".png")
    print("======== ",plate)