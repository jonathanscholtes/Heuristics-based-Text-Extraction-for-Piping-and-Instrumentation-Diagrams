from diagramprep.TextBlockProcessor import TextBlockProcessor
import json
import logging
import cv2

logging.basicConfig(level=logging.DEBUG)


input_path = r"C:\Users\joscholt\Documents\image_processing_test\testfiles\test.json"
src = cv2.imread(r'C:\Users\joscholt\Downloads\test.jpg')

with open(input_path, 'r') as fp:
    text_layout= json.load( fp) 

tbp = TextBlockProcessor(text_layout)
tbp.process_text()

print(tbp.get_tags())


cp = src.copy()
color = (255, 0, 255)


for b in tbp.grouped_boxes:
  
  cv2.rectangle(cp, (b.topleft_x, b.topleft_y), (b.bottomright_x,b.bottomright_y), color, 3)
  #cv2.putText(img2, label, (x, (y-labelSize[1])+baseLine ), cv2.FONT_HERSHEY_SIMPLEX, float(1.5), color, 3)

cv2.imwrite(r"C:\Users\joscholt\Documents\image_processing_test\testfiles\textboxes.jpg",cp)
