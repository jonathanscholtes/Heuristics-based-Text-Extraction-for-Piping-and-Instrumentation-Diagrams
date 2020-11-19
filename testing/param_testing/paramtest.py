import os
import argparse
from diagramprep.PidImage import PidImage
from diagramprep.PidImageProcessor import PidImageProcessor
import logging
import cv2 
import sys
from skimage.metrics import structural_similarity as ssim
import base64
from azure.storage.blob import BlobServiceClient
from azure.storage.blob import BlobClient
import json 
from PIL import Image
from io import BytesIO
import numpy as np


blob_connection_str = os.environ['BLOB_CONNECTION_STRING']
blob_container = os.environ['BLOB_CONTAINER']


def image_from_blob_bytes(blob):
        buf = BytesIO()
        blob_data = blob.download_blob()
        blob_data.readinto(buf)
        buf.seek(0)

        image_bytes = buf.read()

        pil_image = Image.open(BytesIO(image_bytes))
        open_cv_image = np.array(pil_image)	        
        return open_cv_image[:, :, ::-1].copy() 


def string_to_image(image_bytes_str:str,encoding:str='utf-8')->[]:
    
    image_string_b = image_bytes_str.encode(encoding)       
    image_bytes = base64.b64decode(image_string_b)
    logging.info("Image Bytes Len: " + str(len(image_bytes)))

    pil_image = Image.open(BytesIO(image_bytes))
    open_cv_image = np.array(pil_image)	        
    self.image = open_cv_image[:, :, ::-1].copy() 


def get_parser():
    """
    Creates a new argument parser.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--params' ,help='dict of parms to use in test')
    parser.add_argument('--min_circles', help='lower cutoff for circles to process' )
    parser.add_argument('--max_circles', help='upper cutoff for circles to process' )
    parser.add_argument('--ssim_test', help='structural similarity test value' )
    parser.add_argument('--source_file_name', help='Image to process' )
    parser.add_argument('--validation_file_name', help='Image to compare results' )
    parser.add_argument('--destination', help='destination folder to store run results' )

    return parser


def download_file(file_str:str):

    blob = BlobClient.from_connection_string(conn_str=blob_connection_str, container_name="input", blob_name=file_str)

    with open(file_str, "wb") as my_blob:
        blob_data = blob.download_blob()
        blob_data.readinto(my_blob)


def main(args=None):
    #logging.basicConfig(level=logging.DEBUG)

    parser = get_parser()
    args = parser.parse_args(args)
    params = json.loads(args.params)
    print(params)

    min_circles = int(args.min_circles)
    max_circles = int(args.max_circles)


    blob = BlobClient.from_connection_string(conn_str=blob_connection_str, container_name="input", blob_name=args.source_file_name)

    test_image = image_from_blob_bytes(blob)

    blob = BlobClient.from_connection_string(conn_str=blob_connection_str, container_name="input", blob_name=args.validation_file_name)

    orig_img = image_from_blob_bytes(blob)

    # Code to detect symbols in diagrams
    pidImage = PidImage(test_image)
    imageProcessor = PidImageProcessor(pidImage,max_hough_circles=max_circles,min_hough_circles=min_circles, debug=True)

    imageProcessor.process_image(**params,ocr_image=False, circle_index=0)
    
    if len(pidImage.diagramCircles) >= min_circles and len(pidImage.diagramCircles) <= max_circles:
        score = ssim(orig_img, pidImage.debugImages[0], full=False,multichannel=True)
        print(score)
        if score > float(args.ssim_test):
            print("Writing Files")
            meta = {}
            for k in params.keys():
                meta[k] = str(params[k])

            stream = pidImage.get_stream(debug_index=0)  
            file_name = "{}/images/tuneresult_{}.jpg".format(args.destination,str(round(score,5)))
            blob_client = BlobClient.from_connection_string(conn_str=blob_connection_str, container_name=blob_container, blob_name=file_name)    
            blob_client.upload_blob(stream.read(),overwrite=True)
            blob_client.set_blob_metadata(metadata=meta)

    print('DONE..')





if __name__ == '__main__':
    main()