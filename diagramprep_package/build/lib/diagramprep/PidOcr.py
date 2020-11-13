import re
import time
import pytesseract


class Ocr:

    def get_text_from_img(img,remove_special_chars:bool=True,hyphen_new_line:bool=True) -> str:

        #--oem 1 --psm 3 -l eng --oem 1 ''
        txt = pytesseract.image_to_string(img,lang='eng',config='--psm 6')

        ### old if re.search("^[a-zA-Z]+\\n[0-9_]+$",txt) != None:
        if hyphen_new_line == True:
            txt = txt.replace("\n","-") ## set-up tags from instrument contours
        
        if remove_special_chars ==True:
            txt = txt.translate({ord(c): " " for c in "!@#$%^&*()[]{};:,./<>?\|`~=_+\"\\"})

        return txt