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

from .ImageBase import ImageBase

class DiagramCircle(ImageBase):

    radius:float=0
    x:float=0
    y:float=0
    x2:float=0
    y2:float=0
    text:str=""
    h_ratio:float = 0.0
    w_ratio:float = 0.0

    def __init__(self, radius,x,y):
        self.img = None
        self.radius = radius
        self.x = x-radius
        self.y = y-radius
        self.x2 = x+radius
        self.y2 = y+radius        
        self.text = ""

    def get_scale(self)->float:
        return max(self.h_ratio,w_ratio)

