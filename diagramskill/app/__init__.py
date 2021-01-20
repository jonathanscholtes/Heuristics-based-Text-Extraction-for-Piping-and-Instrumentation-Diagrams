
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
from diagramprep.PidImage import PidImage
from diagramprep.PidImageProcessor import PidImageProcessor
from diagramprep.TextBlockProcessor import TextBlockProcessor
import azure.functions as func
import cv2 
from PIL import Image
import numpy as np
import json
import requests
from io import BytesIO
#from azure.storage.blob import BlobServiceClient
import re
import time
import os
import base64
from datetime import datetime


#blob_connection =  os.environ['BLOB_CONNECTION_STRING']
#container = os.environ['CONTAINER']

## Function Entry Point
def main(req: func.HttpRequest) -> func.HttpResponse:
    version = "0.0.8"
    logging.info("Version: %s" % version)
    
    start_time_total = time.time()
    debug = False
    max_circle_ocr = 500

    if 'debug' in req.params:
        debug = (req.params.get('debug')=="True")

    if 'max_circles' in req.params:
        max_circle_ocr = int(req.params.get('max_circles'))

    logging.info("Debug: %s" % str(debug))
    logging.info("Circle Param: %s" % str(max_circle_ocr))

    jsn = req.get_json()

    # Build Function Response
    results = {}
    results["values"] = []

    values = jsn['values']

    logging.info("Values: " + str(len(values)))

    for value in values:
        process_normalized_image(value,results,debug,max_circle_ocr)


    jsn = json.dumps(results,ensure_ascii=False)    

    logging.info("All Processes --- %s seconds ---" % (time.time() - start_time_total))

    return func.HttpResponse(jsn, mimetype="application/json")



def process_normalized_image(value,results,debug,max_circle_ocr):
    """
    Process Values from request JSON

    Parameters::
      a(JSON): value -- Value record containing normalized image and bounding box
      b(JSON): results -- Return Values to append
      c(bool) debug -- Flag used to indicate debug (true,false)
      d(max_circels) -- Maximun number of Hough Circles to OCR (workaround for compact tabular documents)

    Returns:
        Prcess results (JSON): results for processes Value records
    """

    params = {
    'hough_dp':2,
    'hough_blurLevel':11,
    'hough_minDist':10,
    'hough_param2':80,
    'hough_param1':10,
    'hough_maxRadius':40,
    'hough_minRadius':10,
    'hough_dilate_iter':4
    }

    try:

        recordId = value['recordId']
        textlayout = value['data']['layoutText']

        # Capture  PDF Bytes
        start_time = time.time()
        image_string = value['data']['file_data']['data']    

        contour_tags = process_contours(image_string,params,max_circle_ocr,1,False)
        logging.info("Process Contours --- %s seconds ---" % (time.time() - start_time) )

        start_time = time.time()
        text_tags = process_boundingboxes(textlayout)
        logging.info("Process Bounding Boxes --- %s seconds ---" % (time.time() - start_time) )

       

        if False:
            if len(blob_connection) >0 and len(container) > 0:
                logging.info("Writing Debug Image...")

                now  = datetime.now()
                lst = list(map(str,[now.day,now.hour,now.minute,now.second]))

                file_name =  'debug_' + '_'.join(lst)
                logging.info("Calling get_stream(img)")    
                stream = get_stream(img)

                try:
                    blob_service_client = BlobServiceClient.from_connection_string(blob_connection)
                    container_client = blob_service_client.get_container_client(container)
                    blob_client = container_client.get_blob_client(file_name+"/img.jpeg")
                    blob_client.upload_blob(stream.read(),overwrite=True)

                    blob_service_client = BlobServiceClient.from_connection_string(blob_connection)
                    container_client = blob_service_client.get_container_client(container)
                    blob_client = container_client.get_blob_client(file_name+"/text.json")
                    blob_client.upload_blob(json.dumps(textlayout),overwrite=True)

                except Exception as ex:
                    template = "Debug Exception - An exception of type {0} occurred. Arguments:\n{1!r}"
                    message = template.format(type(ex).__name__, ex.args)
                    logging.error(message)
        

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        logging.error(message)


    results['values'].append({"recordId": recordId,"data": {"tags":contour_tags + text_tags} })
    
    

def process_contours(image_string,params,max_circles,min_circles,debug_mode):

    pidImage = PidImage(src)
    pidImage.fromByteString(image_string)

    imageProcessor = PidImageProcessor(pidImage,max_hough_circles=max_circles,
                                        min_hough_circles=min_circles,
                                        debug=debug_mode)
    imageProcessor.process_image(**params)
    return ' '.join([x.text for x in pidImage.diagramCircles])


def process_boundingboxes(bounding_boxes):  

  tbp = TextBlockProcessor(bounding_boxes)
  tbp.process_text()

  return ' '.join(tbp.get_tags())


def get_stream(img,format='JPEG'):

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