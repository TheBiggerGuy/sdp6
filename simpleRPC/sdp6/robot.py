import nxt
from bluetooth import BluetoothError

class RobotNotFoundError(Exception):
    pass

class RobotConnectionError(Exception):
    pass

class Robot(object):
  
  def __init__(self, host=None):  
    print "Connecting ..."
    
    try:
      if host == None:
        self.brick = nxt.find_one_brick().connect()
      else:
        self.brick = BlueSock(host).connect()
    except nxt.locator.BrickNotFoundError:
      raise RobotNotFoundError
    except BluetoothError as error:
      raise RobotConnectionError
    
    
    print "Conected"
  
  def up(self):
    print "go up"
  
  def down(self):
    print "go down"
  
  def left(self):
    print "go left"
  
  def right(self):
    print "go right"
  
  def stop(self):
    print "go stop"
