import numpy as np
from pytesseract import *
import cv2
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import glob
import os

# tesseract executable path
pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
blankImg =Image.new('RGB', (512,512), (255,255,255))
fontSize = 70 #font size for data generation

#directory creation
if not os.path.exists("../Data/Templates"):
    os.mkdir("../Data/Templates")

#looping to create templates for all fonts
for fontStyle in glob.glob(r"..\Data\Fonts\*.ttf"):
    fontName = fontStyle.split("\\")[-1].split('.')[0]
    img = blankImg.copy()
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(fontStyle,fontSize)
    draw.text(( 50, 50),"Hello, World!",(0,0,0),font=font)
    matImg = np.array(img)
    rgb = cv2.cvtColor(matImg, cv2.COLOR_BGR2RGB)
    results = pytesseract.image_to_data(rgb, output_type=Output.DICT) #OCR for text detection

    for i in range(0, len(results["text"])):
        text = results["text"][i]
        conf = int(results["conf"][i])
        #the following module checks if Hello World is in order, and crops image only if this condition is satisfied
        if conf > 5:#confidence is maintained at 5%

            text = "".join(text)
            if text == "Hello,":
                savedText = text
                x = int(results["left"][i])
                y = int(results["top"][i])
                w = int(results["width"][i])
                h = int(results["height"][i])
                continue

            elif text == "World!":
                if savedText == "Hello,":
                    savedText = savedText + text
                    w = int(w + results["width"][i])

            crop_img = matImg[y - int(y / 3):y + h + int(h / 3), x - int(x / 3):x + int( w + w/3)]
            cv2.imwrite("../Data/Templates/"+fontName+".jpg",crop_img) #save cropped image






