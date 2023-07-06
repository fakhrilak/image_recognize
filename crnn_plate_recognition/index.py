import torch
import pandas as pd
import requests
from ninja import Router
from ninja import NinjaAPI, File
from ninja.files import UploadedFile
from django.http import HttpResponse
import io
import os
# import PIL.Image as Image
from PIL import Image, ImageDraw, ImageFont
import json
import uuid
import cv2
import time
from crnn_plate_recognition.demo import init_model,cv_imread,get_plate_result
from crnn_plate_recognition.filtered import filter

router = Router()


# model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
model = torch.hub.load('ultralytics/yolov5', 'custom', path='YOLOV5/weights/exp41/weights/best.pt')

device =torch.device("cpu")
img_size = (48,168)


path  = __file__
splited = path.split("/")
path=""
for i in splited[1:-1]:
    path += "/"+i

crnn = init_model(device,path+"/saved_model/best.pth")
@router.post("/crnn/recognize")
def Recognize_Plate_CRNN(request,file: UploadedFile = File(...)):
    try:
        data = file.read()
        image = Image.open(io.BytesIO(data))
        image.save(path+"/demo/full.png")
        results = model(image)
        df = results.pandas().xyxy[0]
        json_boxes = df.to_json(orient='records')
        print(json_boxes)
        for count,i in enumerate(json.loads(json_boxes)):
            if i["class"] == 0:
                box = (i["xmin"],i["ymin"],i["xmax"],i["ymax"])
                img2 = image.crop(box)
                img2.save(path+"/demo/plat.png")
        img = cv_imread(path+"/demo/plat.png")
        img = cv2.cvtColor(img,cv2.COLOR_BGRA2BGR)
        plate=get_plate_result(img, device,crnn,img_size)
        return {
            "message" : "success",
            # "detail_plat": analys(filter(plate)),
            "data" : filter(plate),
            "plat_detect": json_boxes
        }
    except BaseException as err:
        return {
            "message" : str(err)
        }