import nxt
from nxt.bluesock import BlueSock
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
      print error
      raise RobotConnectionError

    print "Conected"
    
    self.leftWhell = Motor(self.brick, 1)
    self.rightWhell = Motor(self.brick, 2) 
    print "Set up Motors"
  
  def up(self):
    print "go up"
    self.play_tone_and_wait(10000, 10)
    self.leftWhell.run(power=64)
    self.rightWhell.run(power=64)
  
  def down(self):
    print "go down"
    self.play_tone_and_wait(10000, 10)
    self.leftWhell.run(power=-64)
    self.rightWhell.run(power=-64)
  
  def left(self):
    print "go left"
        self.play_tone_and_wait(10000, 10)
    self.leftWhell.run(power=64)
    self.rightWhell.brake()
  
  def right(self):
    print "go right"
    self.play_tone_and_wait(10000, 10)
    self.leftWhell.brake()
    self.rightWhell.run(power=64)
  
  def stop(self):
    print "go stop"
    self.play_tone_and_wait(10000, 10)
    self.leftWhell.brake()
    self.rightWhell.brake()
