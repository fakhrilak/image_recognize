import torch
from PIL import Image, ImageDraw, ImageFont
import os
import io
import json

model = torch.hub.load('ultralytics/yolov5', 'custom', path='weights/exp50/weights/best.pt')
for i in os.listdir("images_wh/"):
    # print(i)
    image_path = os.path.join("images_wh", i)
    image = Image.open(image_path)
    results = model(image)
    df = results.pandas().xyxy[0]
    json_boxes = df.to_json(orient='records')
    # image = Image.open(io.BytesIO("img/"+i))
    for count,k in enumerate(json.loads(json_boxes)):
        if k["class"] == 0:
            box = (k["xmin"],k["ymin"],k["xmax"],k["ymax"])
            img2 = image.crop(box)
            img2.save("img/"+i)