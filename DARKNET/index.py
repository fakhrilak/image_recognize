from ninja import Router
from ninja import NinjaAPI, File
from ninja.files import UploadedFile
from django.http import HttpResponse
import PIL.Image as Image
import requests
import uuid
from darknetpy.detector import Detector
import json
import io
detector = Detector('/data/darknet/cfg/coco.data','/data/darknet/cfg/yolov3.cfg','/data/darknet/yolov3.weights')

router = Router()

path  = __file__
splited = path.split("/")
path=""
for i in splited[1:-1]:
    path += "/"+i
    
@router.post("/recognize")
def DarknetRecognize(request,file: UploadedFile = File(...)):
    try:
        data = file.read()
        image = Image.open(io.BytesIO(data))
        uuids = str(uuid.uuid4())
        image.save(path+"/img/"+uuids+".png")
        results = detector.detect(path+"/img/"+uuids+".png")
        return {
            "message" : "Success",
            "data" : results
        }
    except BaseException as err:
        print(str(err))
        return {
            "message" : "error"
        }