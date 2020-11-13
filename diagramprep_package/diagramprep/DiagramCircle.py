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

