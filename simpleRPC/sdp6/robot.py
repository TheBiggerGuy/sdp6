import nxt
from nxt.bluesock import BlueSock
from nxt.motor import Motor
from bluetooth import BluetoothError
import threading

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
    
  POWER = 80
  BUZZER = 769
  
  NAME = "BrickAshley"
    
  def __init__(self, host=None):
    
    self.power = self.POWER
    self.address = host   
    
    self.connect()    
    
    self.leftWhell = Motor(self.brick, self.LEFT_WHEEL)
    self.rightWhell = Motor(self.brick, self.RIGHT_WHEEL) 
    print "Set up Motors"
  
  def connect(self):
    print "Connecting ..."
    try:
      if self.address == None:
        self.brick = nxt.find_one_brick().connect()
      else:
        self.brick = BlueSock(self.address).connect()      
    except nxt.locator.BrickNotFoundError:
      raise RobotNotFoundError
    except BluetoothError as error:
      raise RobotConnectionError(error)
    
    self.__get_info()
    print "Conected to {name}".format(name=self.name)
    threading.Timer(60, self.__get_info).start()
  
  def disconnect(self):
    try:
      self.brick = None
    except:
      print "Unsafe disconect"
      
  def get_name(self):
    self.__get_info()
    return self.name
  
  def set_name(self, name):
    self.brick.set_brick_name(name)
    self.disconnect()
    self.connect()
    self.__get_info()
  
  def set_power(self, value):
    value=int(value)
    if value < -128 or value > 128:
      pass
      # TODO
    self.power = value
  
  def get_power(self):
    return self.power
  
  def __get_info(self):
    self.name, self.host, self.signal_strength, self.user_flash = self.brick.get_device_info()
    self.battery = self.brick.get_battery_level()
    print "Info: \n\tName: {name}" \
          "\n\tBT MAC: {host}\n\tBT signal: {signal}\n\t" \
          "Memory: {memory}\n\tBattery: {voltage}mV".format(name=self.name, host=self.host, \
          signal=self.signal_strength, memory=self.user_flash, voltage=self.battery)
  
  def up(self):
    print "go up"
    self.leftWhell.run(power=self.power)
    self.rightWhell.run(power=self.power)
  
  def down(self):
    print "go down"
    self.brick.play_tone_and_wait(self.BUZZER, 1000)
    self.leftWhell.run(power=-self.power)
    self.rightWhell.run(power=-self.power)
  
  def right(self, withBrake=False):
    print "go right"
    self.leftWhell.run(power=self.power)
    if withBrake:
      self.rightWhell.brake()
    else:
      self.rightWhell.run(power=-self.power)
  
  def left(self, withBrake=False):
    print "go left"
    if withBrake:
      self.leftWhell.brake()
    else:
      self.leftWhell.run(power=-self.power)
    self.rightWhell.run(power=self.power)
  
  def stop(self):
    print "go stop"
    self.leftWhell.brake()
    self.rightWhell.brake()
  
  def buzz(self):
    print "buzz"
    self.brick.play_tone_and_wait(self.BUZZER, 1000)


