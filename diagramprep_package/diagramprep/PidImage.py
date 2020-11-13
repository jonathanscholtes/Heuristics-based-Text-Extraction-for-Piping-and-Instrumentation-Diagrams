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

from .DiagramCircle import DiagramCircle
from .ImageBase import ImageBase
from typing import List
from PIL import Image
from io import BytesIO
import cv2
import time
import base64
import numpy as np
import logging 

class PidImage(ImageBase):
    
    diagramCircles: List[DiagramCircle] = []
    
    def __init__(self,image: []=[]):
        self.image = image
#

    def fromByteString(self,image_bytes_str: str,encoding:str='utf-8'):
        start_time = time.time()   
        image_string_b = image_bytes_str.encode(encoding)       
        image_bytes = base64.b64decode(image_string_b)
        logging.info("Image Bytes Len: " + str(len(image_bytes)))

        pil_image = Image.open(BytesIO(image_bytes))
        open_cv_image = np.array(pil_image)	        
        self.image = open_cv_image[:, :, ::-1].copy() 
        logging.info("Image Read--- %s seconds ---" % (time.time() - start_time)) 

    

    def createCircles(self,circles:[],buffer:int=0, size:int=110,resize:bool=True):
        
        for c1 in circles[0, :]:           
            dc = DiagramCircle(c1[2]+buffer,c1[0],c1[1])
            dc.image = self.image[dc.y:dc.y2, dc.x:dc.x2]
            if resize == True:
                dc.h_ratio = size/dc.image.shape[0]
                dc.w_ratio = size/dc.image.shape[1]
                dc.image = cv2.resize(dc.image,(int(dc.image.shape[1] * dc.w_ratio),int(dc.image.shape[0] * dc.h_ratio)))

            self.diagramCircles.append(dc)    

    #@property
    #def circles(self) -> List[DiagramCircle]:
    #    return this.circles