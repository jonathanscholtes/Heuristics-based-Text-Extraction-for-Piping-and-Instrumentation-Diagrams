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

from diagramprep.PidImage import PidImage
from diagramprep.PidImageProcessor import PidImageProcessor
import logging
import itertools
#from skimage.measure import compare_ssim, compare_mse
import cv2 
import sys
from skimage.metrics import structural_similarity as ssim


#logging.basicConfig(level=logging.DEBUG)


params = {
    'hough_blurLevel': range(7,15,2),
    'hough_minDist': range(20,100,5),
    'hough_param2': range(90,120,2),
    'hough_param1': range(30,80,2),
    'hough_maxRadius': range(10,30),
    'hough_minRadius':range(5,15)
}


def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush() 

min_circles = 20
max_circles = 45


f = open(r"C:\Users\joscholt\Downloads\testfile.txt",'r')
image_bytes_str = f.read()

pidImage = PidImage()
pidImage.fromByteString(image_bytes_str)
imageProcessor = PidImageProcessor(pidImage,max_hough_circles=max_circles,min_hough_circles=min_circles, debug=True)

filename = r"C:\Users\joscholt\Documents\image_processing_test\tune\test"
testing_files = r"C:\Users\joscholt\Documents\image_processing_test\baseline.jpg"
orig_img =  cv2.imread(testing_files)
scores = []

keys = list(params)
prd = itertools.product(*map(params.get, keys))
total = len(list(prd))
count = 0
match = 0
max_ssim = 0.0

print("")
print("Total Tests: {}".format(total))
print("")
for values in itertools.product(*map(params.get, keys)):
    progress(count,total, "Matched {}, Max SSIM: {}".format(match,round(max_ssim,5)))
    count+=1
    imageProcessor.process_image(**dict(zip(keys, values)),ocr_image=False, circle_index=0)
    if len(pidImage.diagramCircles) >= min_circles and len(pidImage.diagramCircles) <= max_circles:
        score = ssim(orig_img, pidImage.debugImages[0], full=False,multichannel=True)
        ######print("SSIM Score: {}".format(score))
        scores.append(score)
        max_ssim = max(round(score,5),max_ssim)
        if score > .9918:
            match += 1
           #### print(dict(zip(keys, values)))
            cv2.putText(pidImage.debugImages[0], "{} {} {}\n{} {} {}".format(*dict(zip(keys, values))), (50, 150), cv2.FONT_HERSHEY_SIMPLEX ,2, (255, 0, 0), 2, cv2.LINE_AA) 
            pidImage.save_image(filename+"_{}.jpg".format(str(round(score,5))),debug_index=0)
            #cv2.putText(pidImage.debugImages[0], "SSIM Score: {}".format(score), (50, 150), cv2.FONT_HERSHEY_SIMPLEX ,  
            #       2, (255, 0, 0), 2, cv2.LINE_AA) 
            #pidImage.save_image(filename+"_{}_{}_{}_{}.jpg".format(*values),debug_index=0)
            

print("Max score {} Min score {} Scores {}".format(max(scores),min(scores),len(scores)))

print('DONE..')

