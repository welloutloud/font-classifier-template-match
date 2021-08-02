from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import os
import random
#
# path to fonts ttf directory
fontspath = "..\Data\Fonts"

# create directory to save the test images
if not os.path.exists("../Data/TestImages"):
    os.mkdir("../Data/TestImages")


listSize = [30, 50, 20, 60, 15] #the different sizes of fonts to be created
X = [50, 100, 200, 20, 300] # x-coordinates of fonts
Y = [150,25,350,250,120] #y-coordinates of fonts

#loop to create 20 images of test fonts
for it in  range (20):
    blankImg = Image.new('RGB', (512, 512), (255, 255, 255))
    for i, l, x,y in zip(range(5),listSize,X,Y):
        random_file=random.choice(os.listdir(fontspath)) #randomly picks fonts from the set
        fontStyle = os.path.join(fontspath, random_file)
        draw = ImageDraw.Draw(blankImg)
        fontSize = l
        font = ImageFont.truetype(fontStyle, fontSize)
        draw.text((x, y), "Hello, World!", (0, 0, 0), font=font)
    blankImg.save("../Data/TestImages/"+str(it) +".jpg") #saves the font
