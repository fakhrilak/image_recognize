import easyocr
import cv2 

class OCR_Reader():
    def __init__(self, gpu=True, languages=['en', 'it']):
        self.reader = easyocr.Reader(languages, gpu=gpu)
        pass

    def read_text(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # adapted = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 85, 11)
        result = self.reader.readtext(gray)
        text = []
        boxes = []
        for detection in result:
            top_left = tuple(detection[0][1])
            bottom_right = tuple(detection[0][3])
            text.append(detection[1])
            boxes.append(f"Box: {top_left + bottom_right}")
            try:
                image = cv2.rectangle(image,top_left,bottom_right,(0,255,0),2)
            except:
                continue
        return image, text, boxes

    def read_video(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        return self.reader.readtext(gray)