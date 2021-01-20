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


import re
import time
import pytesseract


class Ocr:

    def get_text_from_img(img,remove_special_chars:bool=True,hyphen_new_line:bool=True, tess_config:str='--psm 6') -> str:

        #--oem 1 --psm 3 -l eng --oem 1 ''
        txt = pytesseract.image_to_string(img,lang='eng',config=tess_config)

        
        ### old if re.search("^[a-zA-Z]+\\n[0-9_]+$",txt) != None:
        if hyphen_new_line == True:
            txt = txt.replace("\n","-").strip('-') ## set-up tags from instrument contours

        if remove_special_chars ==True:
            txt = txt.translate({ord(c): " " for c in "!@#$%^&*()[]{};:,./<>?\|`~=_+\"\\"})

        
        
        return txt