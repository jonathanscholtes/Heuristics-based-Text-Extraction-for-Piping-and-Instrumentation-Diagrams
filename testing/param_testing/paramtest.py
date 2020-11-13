import os
import argparse
from diagramprep.PidImage import PidImage
from diagramprep.PidImageProcessor import PidImageProcessor
import logging
import cv2 
import sys
from skimage.metrics import structural_similarity as ssim
from PIL import Image
import base64
import numpy as np
from azure.storage.blob import BlobServiceClient

blob_connection_str = os.environ['BLOB_CONNECTION_STRING']
blob_container = os.environ['BLOB_CONTAINER']


def get_parser():
    """
    Creates a new argument parser.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('params' ,help='dict of parms to use in test')
    parser.add_argument('min_circles', help='lower cutoff for circles to process',type=int )
    parser.add_argument('max_circles', help='upper cutoff for circles to process',type=int )
    parser.add_argument('ssim_test', help='structural similarity test value',type=float )
    #parser.add_argument('source_image_bytes', help='Image to process',type=str )
    #parser.add_argument('test_image_bytes', help='Image to compare results',type=str )
    parser.add_argument('destination', help='destination folder to store run results',type=str )

    return parser


def main(args=None):

    parser = get_parser()
    args = parser.parse_args(args)

    min_circles = args.min_circles
    max_circles = args.max_circles

    pidImage = PidImage()
    pidImage.fromByteString(args.source_image_bytes)
    imageProcessor = PidImageProcessor(pidImage,max_hough_circles=max_circles,min_hough_circles=min_circles, debug=True)

    orig_img = string_to_image(args.test_image_bytes)


    imageProcessor.process_image(*args.params,ocr_image=False, circle_index=0)
    
    if len(pidImage.diagramCircles) >= min_circles and len(pidImage.diagramCircles) <= max_circles:
        score = ssim(orig_img, pidImage.debugImages[0], full=False,multichannel=True)

        if score > args.ssim_test:
            cv2.putText(pidImage.debugImages[0], "{} {} {}\n{} {} {}".format(*args.params), (50, 150), cv2.FONT_HERSHEY_SIMPLEX ,2, (255, 0, 0), 2, cv2.LINE_AA) 
            #pidImage.save_image(filename+"_{}.jpg".format(str(round(score,5))),debug_index=0)
            stream = pidImage.get_stream()
            blob_service_client = BlobServiceClient.from_connection_string(blob_connection_str)
            container_client = blob_service_client.get_container_client(blob_container)
            blob_client = container_client.get_blob_client("{}/images/tuneresult_{}.jpg".format(args.destination,str(round(score,5))))
            blob_client.upload_blob(stream.read(),overwrite=True)

    print('DONE..')


def string_to_image(image_bytes_str:str,encoding:str='utf-8')->[]:
    image_string_b = image_bytes_str.encode(encoding)       
    image_bytes = base64.b64decode(image_string_b)
    logging.info("Image Bytes Len: " + str(len(image_bytes)))

    pil_image = Image.open(BytesIO(image_bytes))
    open_cv_image = np.array(pil_image)	        
    self.image = open_cv_image[:, :, ::-1].copy() 



if __name__ == '__main__':
    main()