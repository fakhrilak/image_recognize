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

router = Router()
# model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
model = torch.hub.load('ultralytics/yolov5', 'custom', path='YOLOV5/weights/exp50/weights/best.pt')

path  = __file__
splited = path.split("/")
path=""
for i in splited[1:-1]:
    path += "/"+i
    
@router.post("/yolo/recognize")
def Recognize_Plate_yolo(request,file: UploadedFile = File(...)):
    try:
        
        # img = 'YOLOV5/exampledata/1.png'  # or file, Path, PIL, OpenCV, numpy, list
        font_size = 32

        image_width = 35
        image_height = 35
        data = file.read()
        merged_image = Image.new("RGB", (500, 650))
        font = ImageFont.truetype("/data/BACKEND/image-recognize/font/HindSiliguri-Medium.ttf", font_size)
        image = Image.open(io.BytesIO(data))
        image1 = image.resize((500, 300))
        merged_image.paste(image1, (0, 0))
        # uuids = str(uuid.uuid4())
        # image.save(path+"/img/"+uuids+".png")
        
        results = model(image)
        df = results.pandas().xyxy[0]
        json_boxes = df.to_json(orient='records')

        # Print the JSON boxes
        # print(json_boxes)
        os.system("rm -rf "+path+"/img/*")
        for count,i in enumerate(json.loads(json_boxes)):
            # if i['confidence'] > 0.5:
            box = (i["xmin"],i["ymin"],i["xmax"],i["ymax"])
            img2 = image.crop(box)
            img2.save(path+"/img/"+str(i["class"])+".png")
            if i["class"] == 0:
                merged_image.paste(img2, (0, 350))
            else:
                merged_image.paste(img2, ((count-1)*100, 450))
            
        sorted_data = sorted(json.loads(json_boxes), key=lambda x: x["xmin"])
        result_analys = ""
        for count,i in enumerate(sorted_data):
            print(i)
            if i["class"] != 0:
                result_analys+=str(i["name"])
                image = Image.open(path+"/img/"+str(i["class"])+".png")
                merged_image.paste(image, ((count-1)*100, 550))
        
        # Define the text content and desired font size
        draw = ImageDraw.Draw(merged_image)

        # Draw the text on the image
        text_color = (255, 255, 255)  # Black
        draw.text((0, 600),"Result RECOGNIZE = " + result_analys, font=font, fill=text_color)
        merged_image.save(path+"/img/"+"merged_image.jpg")
        return{
            "message" : "success",
            "result" : result_analys,
            "result_coordinat" : json.loads(json_boxes)
        }
    except BaseException as err:
        print(str(err))
        return {
            "message" : "Internal server error"
        }