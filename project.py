import zipfile
from zipfile import ZipFile

from PIL import Image, ImageDraw
import pytesseract
import cv2 as cv
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe "

# loading the face detection classifier
face_cascade = cv.CascadeClassifier('D:/Python/tesseract_final_project/haarcascade_frontalface_default.xml')
data={}

with ZipFile("D:/Python/tesseract_final_project/small_img.zip", "r") as files:
        for file in files.infolist():
            with files.open(file, "r") as image:
                img=Image.open(image).convert("RGB")
                data[file.filename]={"pillow":img}
                
for entry in data.keys():
    image=data[entry]['pillow']
    text=pytesseract.image_to_string(image)
    data[entry]['text']=text


for entry in data.keys():
    image=data[entry]["pillow"]

    img_array=np.array(image)
    gray=cv.cvtColor(img_array, cv.COLOR_BGR2GRAY)

    faces=face_cascade.detectMultiScale(gray)
    data[entry]["faces"]=[]

    for x,y,w,h in faces:
        face=image.crop((x,y, x+w, y+h))
        data[entry]["faces"].append(face)


for entry in data.keys():
    for image in data[entry]["faces"]:
        image.thumbnail((100, 100), Image.ANTIALIAS) 


def search(word):
    for entry in data.key():
        if word in data[entry]["text"]:
            if len(data[entry]["faces"] !=0):
                print("Result found in file {}".format(entry))
                row=round(len(data[entry]["faces"])/5,0)
                c_sheet=Image.new("RGB", (500, 100*row))

                x=0
                y=0

                for image in data[entry]["faces"]:
                    c_sheet.paste(image, (x,y))

                    if x+100==c_sheet.width:
                        x=0
                        y+=100
                    else:
                        x+=100

                    c_sheet.show()

            else:
                print("Result found in file {} \nBut there were no faces in that file\n\n".format(entry))               

    return

search("Christopher")
