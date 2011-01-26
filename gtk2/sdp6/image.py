from opencv.cv import *
from opencv.highgui import *

class ImageProcess(object):
  
  def __init__(self, src):
    self.fg_image = cvLoadImage(src)
    self.bg_image = cvLoadImage("image_bg.png")
  
  def do_jazz(self):
    result = self.fg_image - self.bg_image
    cvSaveImage("jazz.png", result)
    return "jazz.png"
