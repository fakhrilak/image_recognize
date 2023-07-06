# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--window-size=1420,1080')
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),chrome_options=chrome_options)
# driver.get("https://www.antaranews.com/search?q=jokowi")
# elem = driver.find_elements(by=By.TAG_NAME,value='a')
# for i in elem:
#     link = i.get_attribute("href").split("/")
#     if link[3] == "berita":
#         print(link)

# driver.close()

# from PIL import Image
# img = Image.open('/data/image-recognize/RECOGNIZE/img/2022-06-11_06-07-58.jpg')
# # img.show()
# box = (250, 250, 750, 750)
# img2 = img.crop(box)
# img2.save('myimage_cropped.jpg')
# img2.show()

# from yolov5 import detect

# img_url = 'https://github.com/ultralytics/yolov5/raw/master/data/images/zidane.jpg'

# result = detect.run(source=img_url, weights="/data/BACKEND/yolov5_ws/yolov5/yolov5l.pt", conf_thres=0.25, imgsz=640)
# print(result)


from PIL import Image, ImageDraw, ImageFont

# Define the text content and desired font size
text = "A"
font_size = 32

# Create a blank image with a white background
background_color = (255, 255, 255)
image_width = 35
image_height = 35
image = Image.new("RGB", (image_width, image_height), background_color)

# Specify the font and create a font object
font = ImageFont.truetype("font/HindSiliguri-Medium.ttf", font_size)

# Create a draw object
draw = ImageDraw.Draw(image)

# Calculate the text size
text_width, text_height = draw.textsize(text, font=font)

# Calculate the position to center the text
text_x = (image_width - text_width) // 2
text_y = (image_height - text_height) // 2

# Draw the text on the image
text_color = (255, 255, 255)  # Black
draw.text((text_x, text_y), text, font=font, fill=text_color)

# Save the image
image.save("letter_image.jpg")

# from PIL import Image

# import pytesseract
# # print("hello world")
# print(pytesseract.image_to_string(Image.open('a.png')))
# print("= Done")