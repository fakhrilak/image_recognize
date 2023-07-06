from ninja import Router
from ninja import NinjaAPI, File
from ninja.files import UploadedFile
from django.http import HttpResponse
from RECOGNIZE.text_reader import OCR_Reader
import io
import PIL.Image as Image
import cv2
import os
import time
import json
import uuid
import requests
router = Router()
path  = __file__
splited = path.split("/")
path=""
for i in splited[1:-1]:
    path += "/"+i

@router.post("/recognize")
def Recognize_Plate(request,file: UploadedFile = File(...)):
    try:
        # print(url)
        # experiment_id = str(time.strftime("%Y-%m-%d_%H-%M-%S"))
        # os.system("wget "+url+" -O /root/LACTURE/PLATNOMER_RECOGNIZE/RECOGNIZE/img/"+experiment_id+".jpg")
        # image = cv2.imread("/root/LACTURE/PLATNOMER_RECOGNIZE/RECOGNIZE/img/"+experiment_id+".jpg")
        data = file.read()
        image = Image.open(io.BytesIO(data))
        uuids = str(uuid.uuid4())
        image.save(path+"/img/"+uuids+".png")
        ############## SAVE #################
        
        img = Image.open(path+"/img/"+uuids+".png")
        box = (600, 300, 1100, 700)
        img2 = img.crop(box)
        img2.save(path+"/croping/"+uuids+".png")
        ############## CROP #################
        imageread = cv2.imread(path+"/croping/"+uuids+".png")
        reader = OCR_Reader(False)
        image, text, boxes = reader.read_text(imageread)
        return {
            "message":"success",
            "data" : text,
            "name" : uuids+".png"
        }
    except BaseException as err:
        print(str(err))
        return {
            "message" : "error"
        }

@router.get("/img/nocrop/{name}")
def ImgaeNoCrop(request,name:str):
    try:
        with open(path+"/img/"+name, 'rb') as image_file:
        # Read the image content
            image_data = image_file.read()

        # Set the content type header
        response = HttpResponse(content_type='image/jpeg')

        # Set the content of the response to the image data
        response.write(image_data)

        return response
    except BaseException as err:
        return {
            "message"  : "Internal server error"
        }

@router.get("/img/crop/{name}")
def ImgaeNoCrop(request,name:str):
    try:
        with open(path+"/croping/"+name, 'rb') as image_file:
        # Read the image content
            image_data = image_file.read()

        # Set the content type header
        response = HttpResponse(content_type='image/jpeg')

        # Set the content of the response to the image data
        response.write(image_data)

        return response
    except BaseException as err:
        return {
            "message"  : "Internal server error"
        }
