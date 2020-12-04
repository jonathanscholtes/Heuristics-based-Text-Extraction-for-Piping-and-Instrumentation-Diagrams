from diagramprep.PidImage import PidImage
from diagramprep.PidImageProcessor import PidImageProcessor
from diagramprep.TextBlockProcessor import TextBlockProcessor
import logging
import cv2 
from PIL import Image
from io import BytesIO
import numpy as np
import time
import json
import requests

#logging.basicConfig(level=logging.DEBUG)

params = {
    'hough_blurLevel': 9,
    'hough_maxRadius':30,
    'hough_minDist': 20
}

#f = open(r"C:\Users\joscholt\Downloads\testfile.txt",'r')
#image_bytes_str = f.read()

output_path = r"C:\Users\joscholt\Documents\image_processing_test\testfiles\test"

src = cv2.imread(r'C:\Users\joscholt\Downloads\test.jpg')
pidImage = PidImage(src)

imageProcessor = PidImageProcessor(pidImage, debug=True)
imageProcessor.process_image(**params,circle_index=1,ocr_image=False)

for i in range(0,len(pidImage.debugImages)):
    cv2.putText(pidImage.debugImages[i], "{}".format(params), (50, 150), cv2.FONT_HERSHEY_SIMPLEX ,2, (255, 0, 0), 2, cv2.LINE_AA)    
    pidImage.save_image(output_path+"_{}.jpg".format(i),debug_index=i)

pidImage.save_image(output_path+"_test2.jpg")

#for i in range(0,len(pidImage.diagramCircles)):
pidImage.diagramCircles[0].save_image(output_path+"circle_{}.jpg".format(0))

wait_limit = 5
wait_counter = 0

cognitive_service_uri = 'https://southcentralus.api.cognitive.microsoft.com/vision/v2.1/recognizeText?mode=Handwritten'
headers1 = {'Content-Type':'application/octet-stream',  'Ocp-Apim-Subscription-Key':''} 
resp1 = requests.post(cognitive_service_uri, data=open(r'C:\Users\joscholt\Downloads\test.jpg', 'rb'), headers=headers1)

time.sleep(2)

uri = resp1.headers['Operation-Location']
headers = {'Content-Type':'application/json',  'Ocp-Apim-Subscription-Key':''} 

while wait_counter < wait_limit:

    resp = requests.get(uri, headers=headers)
    results = json.loads(resp.text)

    if (results["status"] == 'Succeeded'):
        ocr_path = output_path + ".json"
        with open(ocr_path, 'w') as fp:
            json.dump(results['recognitionResult'], fp) 
        print('Write JSON')    

        break
    wait_counter +=1
    print("Waiting {}...".format(wait_counter))
    time.sleep(3)


tbp = TextBlockProcessor(results['recognitionResult'])
tbp.process_text()

print(tbp.get_tags())

print('DONE..')