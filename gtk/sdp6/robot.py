import nxt
from nxt.bluesock import BlueSock
from nxt.motor import Motor
from bluetooth import BluetoothError
#import threading
from time import sleep
import gc
import logging

class RobotNotFoundError(Exception):
    pass

class RobotConnectionError(Exception):
    def __init__(self, error=None):
      self.error = error
    
    def __str__(self):
      return str(self.error)

class Robot(object):
  
  LEFT_WHEEL  = 0x02 # port C
  RIGHT_WHEEL = 0x00 # port A
  KICKER      = 0x01 # port B
    
  DEFAULT_POWER = 80
  TURN_POWER    = 0.8
  
  BUZZER = 769
  
  #NAME = "BrickAshley"
  NAME = "BrickAsh"
    
  def __init__(self, host=None):
    
    self.power = self.DEFAULT_POWER
    self.address = host   
    
    self.log = logging.getLogger("Robot")
    
    self.connect()
    
    self.leftWhell = Motor(self.brick, self.LEFT_WHEEL)
    self.rightWhell = Motor(self.brick, self.RIGHT_WHEEL)
    self.kicker = Motor(self.brick, self.KICKER)
    self.log.info("Set up Motors")
    
    try:
      self.kicker.turn(100, 100, brake=True)
    except Exception as error:
      self.log.error("kicker reset error: " + str(error))
  
  def connect(self):
    self.log.info("Connecting ...")
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
    self.log.info("Conected to {name}".format(name=self.name))
  
  def disconnect(self):
    try:
      self.brick = None
      #self.get_info_thread.stop()
      gc.collect()
    except:
      # TODO: print "Unsafe disconect"
      pass
  
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
    #self.get_info_thread = threading.Timer(30, self.__get_info)
    #self.get_info_thread.start()
    self.name, self.host, self.signal_strength, self.user_flash = self.brick.get_device_info()
    self.battery = self.brick.get_battery_level()
    self.log.info(
          "Info: \n\tName: {name}" \
          "\n\tBT MAC: {host}\n\tBT signal: {signal}\n\t" \
          "Memory: {memory}\n\tBattery: {voltage}mV".format(name=self.name, host=self.host, \
          signal=self.signal_strength, memory=self.user_flash, voltage=self.battery)
          )
  
  def up(self):
    self.log.debug("go up")
    self.leftWhell.run(power=self.power)
    self.rightWhell.run(power=self.power)
  
  def down(self):
    # TODO: print "go down"
    self.brick.play_tone_and_wait(self.BUZZER, 1000)
    self.leftWhell.run(power=-self.power)
    self.rightWhell.run(power=-self.power)
  
  def right(self, withBrake=False):
    # TODO: print "go right"
    self.leftWhell.run(power=self.power*self.TURN_POWER)
    if withBrake:
      self.rightWhell.brake()
    else:
      self.rightWhell.run(power=-self.power*self.TURN_POWER)
  
  def left(self, withBrake=False):
    # TODO: print "go left"
    if withBrake:
      self.leftWhell.brake()
    else:
      self.leftWhell.run(power=-self.power*self.TURN_POWER)
    self.rightWhell.run(power=self.power*self.TURN_POWER)
  
  def stop(self):
    # TODO: print "go stop"
    self.leftWhell.brake()
    self.rightWhell.brake()
    self.kicker.brake()
  
  def buzz(self):
    # TODO: print "buzz"
    self.brick.play_tone_and_wait(self.BUZZER, 1000)
  
  def kick(self):
    # TODO: print "kick"
    self.kicker.turn(-127, 85, brake=True)
    sleep(1.5)
    self.kicker.turn(127, 90, brake=True)
  
  def __del__(self):
    if self.brick != None:
      self.disconnect()


