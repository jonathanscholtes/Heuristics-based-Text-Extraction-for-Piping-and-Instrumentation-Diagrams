############################################################################################
#Permission is hereby granted, free of charge, to any person obtaining a copy of
#this software and associated documentation files (the "Software"), to deal in
#the Software without restriction, including without limitation the rights to
#use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
#of the Software, and to permit persons to whom the Software is furnished to do
#so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.
###########################################################################################


from .PidImage import PidImage
from .Processor import Processor
from .PidOcr import Ocr as ocr
import time
import base64
import numpy as np
import logging 
from PIL import Image
from io import BytesIO
import cv2 


class PidImageProcessor():

    pidImage: PidImage = None

    def __init__(self, pidImage: PidImage,max_hough_circles:int=500,min_hough_circles:int=1,              
                debug:bool=False):
        self.pidImage = pidImage
        self.debug = debug
        self.max_hough_circles = max_hough_circles
        self.min_hough_circles = min_hough_circles


         
    def process_image(self,
                hough_dp:int = 3,
                hough_minDist:int = 10,
                hough_param1:int = 50,
                hough_param2:int=90,
                hough_minRadius:int=10,
                hough_maxRadius:int=20,
                hough_imageSize:int=110,
                hough_blurLevel:int=5,
                hough_dilate_iter=5,
                circle_index:int=-1,
                ocr_image:bool=True):
      
        self.hough_dp = hough_dp
        self.hough_minDist = hough_minDist
        self.hough_param1 = hough_param1
        self.hough_param2 = hough_param2
        self.hough_minRadius = hough_minRadius
        self.hough_maxRadius = hough_maxRadius
        self.hough_imageSize = hough_imageSize
        self.hough_blurLevel=hough_blurLevel
        self.hough_dilate_iter = hough_dilate_iter

        self.pidImage.debugImages = []
        self.pidImage.diagramCircles = []
        self.ocr_image = ocr_image


        if len(self.pidImage.image) > 0:

            start_time = time.time()
            self.__contour_match() # Retrieve Hough Circles    
            logging.info("Contour Match--- %s seconds ---" % (time.time() - start_time))
            print("Contour Match--- %s seconds ---" % (time.time() - start_time))
            print("Circles: %s" % len(self.pidImage.diagramCircles))

            if len(self.pidImage.diagramCircles) >0:
                _start_time = time.time()
                self.__prep_circles()    
                logging.info("Matched Circle Prep--- %s seconds ---" % (time.time() - start_time))
                print("Matched Circle Prep--- %s seconds ---" % (time.time() - start_time))

                if self.ocr_image ==True:
                    self.__ocr_circles(circle_index)
        else:
            raise RuntimeError('PidImage has no Image set')
            

        
    def __contour_match(self):    
        orig = self.pidImage.image.copy()   
        img2 = orig.copy() 
        kernel = np.ones((2,2), np.uint8) 

        img2 = cv2.GaussianBlur(img2, (self.hough_blurLevel,self.hough_blurLevel), 3)
        #img2 = cv2.erode(img2, kernel, iterations=5)
        img2 = cv2.dilate(img2, kernel, iterations=self.hough_dilate_iter)
        ret, img2 = cv2.threshold(img2, 220, 255, cv2.THRESH_TOZERO)
        gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=self.hough_dp, minDist=self.hough_minDist,
                                param1=self.hough_param1, param2=self.hough_param2,
                                minRadius=self.hough_minRadius, maxRadius=self.hough_maxRadius)

        if circles is not None:
            circles = np.uint16(np.around(circles))

            if len(circles[0, :]) < self.max_hough_circles and len(circles[0, :]) >= self.min_hough_circles:
                self.pidImage.createCircles(circles,size=self.hough_imageSize)

                if self.debug == True:                
                    for i in circles[0, :]:
                            center = (i[0], i[1])                        
                            radius = i[2]
                            cv2.circle(orig, center, radius, (255, 0, 255), 3)
                    self.pidImage.debugImages.append(orig)

                    self.pidImage.debugImages.append(img2)
                    self.pidImage.debugImages.append(gray) 
            else:
                logging.info("Contour match {} is outside of min/max {}/{}".format(len(circles[0, :]),self.min_hough_circles,self.max_hough_circles))
                print("Contour match {} is outside of min/max {}/{}".format(len(circles[0, :]),self.min_hough_circles,self.max_hough_circles))
    
   

    def __prep_circles(self):

        kernel = np.ones((3,3), np.uint8) 
        kernel_sharpening=np.array([[-1,-1,-1], [-1, 15,-1],[-1,-1,-1]])

        logging.info("Prep-ing: {} circles".format(len(self.pidImage.diagramCircles)))
        print("Prep-ing: {} circles".format(len(self.pidImage.diagramCircles)))
        
        for dc in self.pidImage.diagramCircles:
            dc.image = self.__remove_circle_line(dc.image)
            dc.image = cv2.dilate(dc.image, kernel, iterations=1)

            ret, dc.image = cv2.threshold(dc.image, 210, 255, cv2.THRESH_TOZERO)
            dc.image = cv2.fastNlMeansDenoisingColored(dc.image,None,6,6,7,21)
            sharpened=cv2.filter2D(dc.image,-1,kernel_sharpening)
            sharpened = self.__remove_horizontal_lines(sharpened)


    def __remove_circle_line(self,img):
        kernel = np.ones((2,2), np.uint8) 

        src_cp2 = img.copy()

        src_cp2 = cv2.GaussianBlur(src_cp2, (5, 5), 5)

        src_cp2 = cv2.dilate(src_cp2, kernel, iterations=2)
        ret, src_cp2 = cv2.threshold(src_cp2, 220, 255, cv2.THRESH_TOZERO)
        gray = cv2.cvtColor(src_cp2, cv2.COLOR_BGR2GRAY)


        c = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=3, minDist=50,
                    param1=80, param2=90,
                    minRadius=40, maxRadius=56) 
        
        ret,src_cp2 = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY_INV+ cv2.THRESH_OTSU)

        mask= np.zeros(src_cp2.shape[:2], dtype="uint8") 

        if c is not None:
            c = np.uint16(np.around(c))
            for i in c[0, :]:
                center = (i[0], i[1])
                # circle outline
                radius = i[2]
                cv2.circle(mask, center, radius-2, (255,255,255), -1)

        img = cv2.bitwise_and(img,img,mask=mask)
        img = img * 255
        img = cv2.bitwise_not(img)
        img = cv2.erode(img, kernel, iterations=1) 
        img = cv2.dilate(img, kernel, iterations=2) 
        
        return img


    def __remove_horizontal_lines(self,img):
        
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40,1))
        remove_horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
        cnts = cv2.findContours(remove_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        for c in cnts:
            cv2.drawContours(img, [c], -1, (255,255,255), 5)
        return img

    def __ocr_circles(self, circle_index=-1):
        if circle_index == -1:
            for dc in self.pidImage.diagramCircles:
                dc.text = ocr.get_text_from_img(dc.image)
        else:
            dc = self.pidImage.diagramCircles[circle_index]
            dc.text = ocr.get_text_from_img(dc.image)