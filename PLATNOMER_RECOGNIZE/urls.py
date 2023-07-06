from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI
# from RECOGNIZE.index import router as RECOGNIZE
# from DARKNET.index import router as DARKNET
# from YOLOV5.index import router as YOLOV5
from crnn_plate_recognition.index import router as CRNN
api = NinjaAPI()
# api.add_router("/v1", RECOGNIZE)
# api.add_router("/v2",DARKNET)
# api.add_router("/v3",YOLOV5)
api.add_router("/v4",CRNN)
urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", api.urls),
]
