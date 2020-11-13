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
    
    def get_stream(self,format='JPEG'):

        """
        Convert CV2 Image to ByteIO Stream

        Parameters::
        (CV2 Image): img -- OpenCV Image
        (String) : format -- image format (Default JPEG)

        Returns:
        ByteIO Steam
        """
        logging.info("calling get_stream")
        pil_image2 = Image.fromarray(cv2.cvtColor(self.image,cv2.COLOR_BGR2RGB))
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
        