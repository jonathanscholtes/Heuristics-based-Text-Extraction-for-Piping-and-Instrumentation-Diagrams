from diagramprep.PidImage import PidImage
from diagramprep.PidImageProcessor import PidImageProcessor
import logging
import cv2 
from PIL import Image
from io import BytesIO
import numpy as np

#logging.basicConfig(level=logging.DEBUG)

params = {
    'hough_blurLevel': 9,
    'hough_maxRadius':30,
    'hough_minDist': 20
}

f = open(r"C:\Users\joscholt\Downloads\testfile.txt",'r')
image_bytes_str = f.read()

output_path = r"C:\Users\joscholt\Documents\image_processing_test\testfiles\test"

pidImage = PidImage()
pidImage
imageProcessor = PidImageProcessor(pidImage, debug=True)
imageProcessor.process_image(**params,circle_index=1,ocr_image=False)

for i in range(0,len(pidImage.debugImages)):
    cv2.putText(pidImage.debugImages[i], "{}".format(params), (50, 150), cv2.FONT_HERSHEY_SIMPLEX ,2, (255, 0, 0), 2, cv2.LINE_AA)    
    pidImage.save_image(output_path+"_{}.jpg".format(i),debug_index=i)

pidImage.save_image(output_path+"_test2.jpg")

#for i in range(0,len(pidImage.diagramCircles)):
pidImage.diagramCircles[0].save_image(output_path+"circle_{}.jpg".format(0))


print('DONE..')