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

import logging 
from PIL import Image
from io import BytesIO
import cv2 
import base64


class ImageBase():

    image:[]=[]
    debugImages:[]=[]
    
    def __init__(self,image):
        self.image=image
    
    def get_stream(self,format='JPEG',debug_index:int=-1):

        """
        Convert CV2 Image to ByteIO Stream

        Parameters::
        (CV2 Image): img -- OpenCV Image
        (String) : format -- image format (Default JPEG)

        Returns:
        ByteIO Steam
        """
        img = self.image

        if debug_index > -1:
            img = self.debugImages[debug_index]

        logging.info("calling get_stream")
        pil_image2 = Image.fromarray(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
        buf = BytesIO()
        pil_image2.save(buf, format=format)
        buf.seek(0)
        return buf

    def get_image_byte_str(self,debug:bool=False) -> str:
        retval, buffer = cv2.imencode('.jpg', self.image)
        jpg_as_text = base64.b64encode(buffer)
        return jpg_as_text

    def save_image(self,filename:str,debug_index:int=-1):
        if debug_index >-1:
            cv2.imwrite(filename, self.debugImages[debug_index])
        else:
            cv2.imwrite(filename, self.image)
        