from ninja import Schema

class CorrectImg(Schema):
    name :str
    correct : str

class MyCommand(Schema):
    command :str

class DemoPredict(Schema):
    model :str
    img : str
    
class Comparation2Models(Schema):
    newModel :str
    lastModel : str