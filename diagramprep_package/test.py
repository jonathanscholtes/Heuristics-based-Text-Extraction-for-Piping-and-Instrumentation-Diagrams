from diagramprep.PidImage import PidImage
from diagramprep.PidImageProcessor import PidImageProcessor
import logging

logging.basicConfig(level=logging.DEBUG)

params = {
    'hough_blurLevel': 9,
    'hough_maxRadius':30,
    'hough_minDist': 20
}

f = open(r"C:\Users\joscholt\Downloads\testfile.txt",'r')
image_bytes_str = f.read()

pidImage = PidImage()
pidImage.fromByteString(image_bytes_str)
imageProcessor = PidImageProcessor(pidImage, debug=True)
imageProcessor.process_image(**params,circle_index=1,ocr_image=False)

filename = r"C:\Users\joscholt\Documents\image_processing_test\testfiles\test"

for i in range(0,len(pidImage.debugImages)):
    pidImage.save_image(filename+"_{}.jpg".format(i),debug_index=i)

pidImage.save_image(filename+".jpg")


for i in range(0,len(pidImage.diagramCircles)):
    pidImage.diagramCircles[i].save_image(filename+"circle_{}.jpg".format(i))


print('DONE..')