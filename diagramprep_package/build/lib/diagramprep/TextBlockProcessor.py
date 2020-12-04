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
import time
import json
from .TextBlock import TextBlock


class TextBlockProcessor():

    original_textblocks: [] = []
    grouped_boxes: []= []
    singles: {} ={}
    matches: {} = {}

    def __init__(self,text_layout:dict):
        self.grouped_boxes = []
        self.singles = {}
        self.matches = {}
        self.original_textblocks = self.__get_textblocks(text_layout)

    def process_text(self, maxSegment:int=95,
                    leftAlignSensitivity:int=5,
                    rightAlignSensitivity:int=5,
                    centerAlignSensitivty:int=15):
        
        if len(self.original_textblocks) > 0:
            start_time = time.time()
            self.__match_boxes(maxSegment,leftAlignSensitivity,rightAlignSensitivity,centerAlignSensitivty)
            #self.__match_singles()
            logging.info("Group Text--- %s seconds ---" % (time.time() - start_time))

        for b in self.grouped_boxes:
            b.text = self._clean_tags(b.text)

    def _clean_tags(self,text:str):
        text = text.replace("\n","-") 
        text = text.replace("- ","-") 
        text = text.replace(" -","-")

        return text.strip('-')

    def get_tags(self):
        return [ x.text for x in self.grouped_boxes if "-"  in x.text]


    def get_text(self):
        """
        Merge text from boxes (Textblock)

        Parameters::
        (TextBlock[]): boxes -- OCR boundingbox grouping to retreive test from 

        Returns:
            TextS (String): concat textblock text
        """
        text = ""
        for b in self.grouped_boxes:
            text = text + " " +  b.text 
        return text


    def __get_textblocks(self,text_layout:[]):

        textblocks = []
        start_time = time.time()

        for line in text_layout["lines"]:
            if len(line) >0:
                textblocks.append(TextBlock(line['text'],line['boundingBox']))

        logging.info("Load Bounding Boxes--- %s seconds ---" % (time.time() - start_time))
        logging.info("%s textblocks" % str(len(textblocks)))
        return textblocks


    def __match_boxes(self,maxSegment:int=95,leftAlignSensitivity:int=5,rightAlignSensitivity:int=5,centerAlignSensitivty:int=15):
        self.grouped_boxes = []
        self.matches = {}
        ids=[]
        self.singles = {}   
        textblocks = self.original_textblocks
    
        for i in range(len(textblocks)):
            tb = textblocks[i].copy()
            count=0
            for j in range(len(textblocks)):
                if (i != j) and (i not in ids) and (len(textblocks[j].text) < maxSegment and len(tb.text) < maxSegment) and (tb.dist_y(textblocks[j]) <= 18):
                    if tb.dist_left_x(textblocks[j]) <= leftAlignSensitivity:  
                        ids.append(j)
                        tb = tb.merge(textblocks[j])
                        count = count + 1  
                    else:
                        if tb.dist_right_x(textblocks[j]) <= rightAlignSensitivity:
                            ids.append(j)
                            tb = tb.merge(textblocks[j])
                            count = count + 1
                        else:
                            if tb.dist_mean_x(textblocks[j]) <= centerAlignSensitivty:
                                ids.append(j)
                                tb = tb.merge(textblocks[j])
                                count = count + 1
            if(count > 0):
                self.matches.update({i:tb})
            else:
                self.singles.update({i:tb})

        self.grouped_boxes = list(self.matches.values())




    def __match_singles(self):
       
        for s in self.singles:
            cnt = 0
            for m in self.matches:
                if(self.matches[m].intersect(self.singles[s]) == True):
                    cnt = 0
                    break
                else:
                    cnt = 1
            
            if cnt >0:
                self.grouped_boxes.append(self.singles[s])