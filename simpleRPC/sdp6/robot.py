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
  
  LEFT_WHEEL  = Motor.PORT_A
  RIGHT_WHEEL = Motor.PORT_B
  
  BUZZER = 440
  
  POWER = 128
    
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
    self.brick.play_tone_and_wait(self.BUZZER, 10)
    self.leftWhell.run(power=self.POWER)
    self.rightWhell.run(power=self.POWER)
  
  def down(self):
    print "go down"
    self.brick.play_tone_and_wait(self.BUZZER, 10)
    self.leftWhell.run(power=-self.POWER)
    self.rightWhell.run(power=-self.POWER)
  
  def left(self):
    print "go left"
    self.brick.play_tone_and_wait(self.BUZZER, 10)
    self.leftWhell.run(power=self.POWER)
    self.rightWhell.brake()
  
  def right(self):
    print "go right"
    self.brick.play_tone_and_wait(self.BUZZER, 10)
    self.leftWhell.brake()
    self.rightWhell.run(power=self.POWER)
  
  def stop(self):
    print "go stop"
    self.brick.play_tone_and_wait(self.BUZZER, 10)
    self.leftWhell.brake()
    self.rightWhell.brake()
