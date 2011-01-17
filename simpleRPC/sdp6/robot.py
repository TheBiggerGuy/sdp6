import nxt
from nxt.bluesock import BlueSock
from nxt.motor import Motor
from bluetooth import BluetoothError

class RobotNotFoundError(Exception):
    pass

class RobotConnectionError(Exception):
    def __init__(self, error=None):
      self.error = error
    
    def __str__(self):
      return str(self.error)

class Robot(object):
  
  LEFT_WHEEL  = 0x00
  RIGHT_WHEEL = 0x01
  
  BUZZER = 164*10
  
  POWER = 80
    
  def __init__(self, host=None):
    print "Connecting ..."
    
    try:
      if host == None:
        self.brick = nxt.find_one_brick().connect()
      else:
        self.brick = BlueSock(host).connect()
      
      self.name, self.host, self.signal_strength, self.user_flash = self.brick.get_device_info()
    except nxt.locator.BrickNotFoundError:
      raise RobotNotFoundError
    except BluetoothError as error:
      raise RobotConnectionError(error)

    print "Conected to {name}".format(name=self.name)
    
    self.leftWhell = Motor(self.brick, self.LEFT_WHEEL)
    self.rightWhell = Motor(self.brick, self.RIGHT_WHEEL) 
    print "Set up Motors"
  
  def up(self):
    print "go up"
    self.leftWhell.run(power=self.POWER)
    self.rightWhell.run(power=self.POWER)
  
  def down(self):
    print "go down"
    self.brick.play_tone_and_wait(self.BUZZER, 1000)
    self.leftWhell.run(power=-self.POWER)
    self.rightWhell.run(power=-self.POWER)
  
  def right(self, withBrake=False):
    print "go right"
    self.leftWhell.run(power=self.POWER)
    if withBrake:
      self.rightWhell.brake()
    else:
      self.rightWhell.run(power=-self.POWER)
  
  def left(self, withBrake=False):
    print "go left"
    if withBrake:
      self.leftWhell.brake()
    else:
      self.leftWhell.run(power=-self.POWER)
    self.rightWhell.run(power=self.POWER)
  
  def stop(self):
    print "go stop"
    self.leftWhell.brake()
    self.rightWhell.brake()
  
  def buzz(self):
    print "buzz"
    self.brick.play_tone_and_wait(self.BUZZER, 1000)
