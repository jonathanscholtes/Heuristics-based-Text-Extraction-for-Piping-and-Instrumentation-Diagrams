import logging 
from PIL import Image
from io import BytesIO
import cv2 
import base64

class Processor():

    def get_stream(self,img,format='JPEG'):

        """
        Convert CV2 Image to ByteIO Stream

        Parameters::
        (CV2 Image): img -- OpenCV Image
        (String) : format -- image format (Default JPEG)

        Returns:
        ByteIO Steam
        """
        logging.info("calling get_stream")
        pil_image2 = Image.fromarray(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
        buf = BytesIO()
        pil_image2.save(buf, format=format)
        buf.seek(0)
        return buf

    def get_image_byte_str(self,img) -> str:
        retval, buffer = cv2.imencode('.jpg', img)
        jpg_as_text = base64.b64encode(buffer)
        return jpg_as_text