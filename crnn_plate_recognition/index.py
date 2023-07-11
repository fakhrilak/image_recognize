import torch
import pandas as pd
import requests
from ninja import Router
from ninja import NinjaAPI, File
from ninja.files import UploadedFile
from django.http import HttpResponse
from django.http import JsonResponse
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
from crnn_plate_recognition.body_schema import CorrectImg,MyCommand,DemoPredict as BodyDemo
from datetime import datetime
import subprocess
router = Router()


# model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
model = torch.hub.load('ultralytics/yolov5', 'custom', path='YOLOV5/weights/exp50/weights/best.pt')

device =torch.device("cpu")
img_size = (48,168)


path  = __file__
splited = path.split("/")
path=""
for i in splited[1:-1]:
    path += "/"+i

crnn = init_model(device,path+"/saved_model/learn3.pth")
@router.post("/crnn/recognize")
def Recognize_Plate_CRNN(request,file: UploadedFile = File(...)):
    try:
        # print(request)
        data = file.read()
        image = Image.open(io.BytesIO(data))
        #save to no crop
        # image.save("/data/BACKEND/LPR_IMG/v1/IMG_PREDICT/no_crop/"+file.name)
        results = model(image)
        df = results.pandas().xyxy[0]
        json_boxes = df.to_json(orient='records')
        print(json_boxes)
        for count,i in enumerate(json.loads(json_boxes)):
            if i["class"] == 0:
                box = (i["xmin"],i["ymin"],i["xmax"],i["ymax"])
                img2 = image.crop(box)
                #save to crop
                img2.save("/data/BACKEND/LPR_IMG/true/"+file.name)
                img = cv_imread("/data/BACKEND/LPR_IMG/true/"+file.name)
                img = cv2.cvtColor(img,cv2.COLOR_BGRA2BGR)
                plate=get_plate_result(img, device,crnn,img_size)
                
                return JsonResponse({
                    "message" : "success",
                    # "detail_plat": analys(filter(plate)),
                    "data" : filter(plate),
                    "name" : file.name,
                    "path" : "true/",
                    "plat_detect": json_boxes
                })
    except BaseException as err:
        return JsonResponse({
            "message" : str(err)
        })

@router.get("/img/plat/{trueorfalse}/{name}")
def ImageCrop(request,name:str,trueorfalse:str):
    try:
        with open("/data/BACKEND/LPR_IMG/"+trueorfalse+"/"+name, 'rb') as image_file:
            image_data = image_file.read()
        response = HttpResponse(content_type='image/jpeg')
        response.write(image_data)

        return response
    except BaseException as err:
        print(str(err),"== ERROR DI ENDPOINT GET CROP PLAT NOMER")
        return {
            "message"  : "Internal server error"
        }
    
@router.patch("/crnn/correct")
def CorectValue(request,data:CorrectImg):
    try:
        dt = datetime.now()
        dt_str = dt.strftime('%Y-%m-%d-%H:%M:%S')
        # "/data/BACKEND/LPR_IMG/v1/IMG_PREDICT/no_crop/"+file.name
        # MOVE NO CROP
        # os.system("mv /data/BACKEND/LPR_IMG/v1/IMG_PREDICT/no_crop/"+data.name+\
        #           " /data/BACKEND/LPR_IMG/v1/IMG_WRONG/no_crop/"+data.name)
        # MOVE CROP
        os.system("mv /data/BACKEND/LPR_IMG/true/"+data.name+\
                  "  /data/BACKEND/LPR_IMG/false/"+data.correct+"_"+dt_str+".png")
        return JsonResponse({
            "message" : "success",
            "command"  : "mv true/"+data.name+\
                  "  false/"+data.correct+"_"+dt_str+".png"
        })
    except BaseException as err:
        print(str(err),"== ERROR DI ENDPOINT CORRECT")
        return JsonResponse({
            "message" : "Internal Server Error"
        })

@router.get("/img/list/{trueorfalse}")
def getListImageFolder(request,trueorfalse:str):
    try:
        data = os.listdir("/data/BACKEND/LPR_IMG/"+trueorfalse)
        return JsonResponse({
            "message" : "success",
            "data" : data
        })
    except BaseException as err:
        print(str(err))
        return JsonResponse({
            "message" : "Internal Server Error"
        })

@router.post("/mycmd")
def CommandLine(request,command:MyCommand):
    try:
        commands = command.command.split(" ")
        process = subprocess.Popen(commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()

        # Print the output
        # print(out.decode("utf-8").split("\n"),"ini")
        return JsonResponse({
            "message" : "success",
            "data" : out.decode("utf-8").split("\n")
        })
    except BaseException as err:
        return JsonResponse({
            "message" : "Internal Server Error",
            "data" : str(err)
        })

@router.post("/demo")
def DemoPrediction(request,data:BodyDemo):
    try:
        crnn = init_model(device,path+"/"+data.model)
        img = cv_imread("/data/BACKEND/LPR_IMG/"+data.img)
        img = cv2.cvtColor(img,cv2.COLOR_BGRA2BGR)
        plate=get_plate_result(img, device,crnn, (48,168))
        return JsonResponse({
            "message" : "success",
            "data" : plate
        })
    except BaseException as err:
        print(str(err))
        return JsonResponse({
            "message" : "Internal Server Error",
            "data" : str(err)
        })