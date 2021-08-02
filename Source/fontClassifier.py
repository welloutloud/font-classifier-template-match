import os
import cv2
import numpy as np
import glob
import imutils
import json

class fontClassify:
    def __init__(self):
        self.templatesPath = r"..\Data\Templates\*"
        self.imagesPath = r"..\Data\TestImages\*"
        self.threshold = 0.9
        self.flag = 0
        self.fontNameOK = ""
        self.jsonObj = {}

    # Create directory for results if not already present
    def createDirectory(self):
        if not os.path.exists("../Results"):
            os.mkdir("../Results")

    #writes images and json files in the output folder
    def output(self, main_image, imgnm, jsonObj):
        # cv2.imshow("Image", main_image)
        cv2.imwrite("../Results/" + imgnm + ".jpg", main_image)
        with open("../Results/" +imgnm +'.json', 'w') as jsonFile:
            json.dump(jsonObj, jsonFile)
            print(jsonObj)
        # cv2.waitKey(0)

    # function to classify the fonts based on multi-scale template matching
    def classify(self):

        for img in glob.glob(self.imagesPath):
            self.jsonObj['detectedFonts'] = []
            imgnm = img.split("\\")[-1].split(".")[0]
            main_image = cv2.imread(img)
            finalimg =main_image.copy()
            gray_image = cv2.cvtColor(main_image, cv2.COLOR_BGR2GRAY)

            for temp in glob.glob(self.templatesPath):

                found = None
                fontName = temp.split('\\')[-1].split('-')[0]
                template = cv2.imread(temp, 0)
                template_width, template_height = template.shape[::-1]
                self.flag = 0

                # looping to resize the template image in multiple scales to match fonts in the image
                for scale in np.linspace(0.2, 1.0)[::-1]:
                    if self.flag == 0:
                        resizedTemplate = imutils.resize(template, width=int(template.shape[1] * scale))
                        r = template.shape[1] / float(resizedTemplate.shape[1])
                        r_width, r_height = resizedTemplate.shape[::-1]
                        result = cv2.matchTemplate(gray_image, resizedTemplate, cv2.TM_CCOEFF_NORMED)
                        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

                        if found is None or max_val > found[0]:
                            found = (max_val, max_loc, r)

                        if max_val > self.threshold:
                            self.flag = 1

                            (_, max_loc, r) = found
                            (startX, startY) = (int(max_loc[0] ), int(max_loc[1] ))
                            (endX, endY) = (int((max_loc[0] + r_width)), int((max_loc[1] + r_height) ))

                            if fontName == self.fontNameOK:
                                break
                            #     draw bounding box and write the font name and confidence
                            cv2.rectangle(main_image, (startX, startY), (endX, endY), (0, 0, 255), 2)
                            cv2.putText(main_image, fontName +" :  " + str(max_val*100), (startX, startY), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1)
                            self.fontNameOK = fontName

                            # write results in json format
                            self.jsonObj['detectedFonts'].append({
                                'boundingBox' : {
                                "x": startX,
                                "y": startY,
                                "width": r_width,
                                "height": r_height
                            },
                                'font' : fontName,
                                'confidence' : max_val * 100

                            })


            # function call to write output images and jsons
            self.output(main_image, imgnm, self.jsonObj)


if __name__ =='__main__':
    obj = fontClassify() #object creation of the class
    obj.classify()