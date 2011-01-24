import nxt
from nxt.bluesock import BlueSock
from nxt.motor import Motor, SynchronizedMotors
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
  
  LEFT_WHEEL  = 0x00 # port C
  RIGHT_WHEEL = 0x02 # port A
  KICKER      = 0x01 # port B
    
  DEFAULT_POWER = 90
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
    self.synchronised = SynchronizedMotors(self.leftWhell, self.rightWhell, 0)
    
   # try:
   #   self.kicker.turn(100, 100, brake=True)
   # except Exception as error:
   #   self.log.error("kicker reset error: " + str(error))
  
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
 #   self.synchronised.run(power=self.power)
    self.leftWhell.run(power=self.power)
    self.rightWhell.run(power=self.power+2.4)

  def up1(self):
    self.log.debug("go up1")
    #self.leftWhell.run(power=self.power)
    #self.rightWhell.run(power=self.power)
    #sleep(1)
    #self.stop()
    self.synchronised.turn(self.power, 360, brake=True)

  def up2(self):
    self.log.debug("go up")
 #   self.synchronised.run(power=self.power)
    self.leftWhell.run(power=self.power)
    self.rightWhell.run(power=self.power+2.4)
    sleep(1)
    self.stop()	
#    self.leftWhell.turn(self.power, 360, brake=False)
 #   self.rightWhell.turn(self.power, 360, brake=False)
    
  def down(self):
    # TODO: print "go down"
    self.leftWhell.run(power=-self.power)
    self.rightWhell.run(power=-self.power)

  def down1(self):
    # TODO: print "go down"
    self.synchronised.turn(-self.power, 360, brake=True)
    self.stop()
  
  def right(self, withBrake=False):
    # TODO: print "go right"
    self.leftWhell.run(power=self.power*self.TURN_POWER)
    if withBrake:
      self.rightWhell.brake()
    else:
      self.rightWhell.run(power=-self.power*self.TURN_POWER)
    sleep(1)
    self.stop()

  def right1(self, withBrake=False):
    # TODO: print "go right"
    self.leftWhell.turn(self.power*self.TURN_POWER, 360, brake=True)
    #if withBrake:
    #  self.rightWhell.brake()
    #else:
    self.rightWhell.turn(-self.power*self.TURN_POWER, 360, brake=True)
 
  
  def left(self, withBrake=False):
    # TODO: print "go left"
    if withBrake:
      self.leftWhell.brake()
    else:
      self.leftWhell.run(power=-self.power*self.TURN_POWER)
    self.rightWhell.run(power=self.power*self.TURN_POWER)

  def left1(self, withBrake=False):
    # TODO: print "go left"
    self.rightWhell.turn(self.power*self.TURN_POWER, 360, brake=True)
   # if withBrake:
   #   self.leftWhell.brake()
   # else:
    self.leftWhell.turn(-self.power*self.TURN_POWER, 360, brake=True)

  def stop(self):
    # TODO: print "go stop"
    self.leftWhell.brake()
    self.rightWhell.brake()
    self.kicker.brake()
  
  def buzz(self):
    # TODO: print "buzz"
    self.brick.play_tone_and_wait(self.BUZZER, 1000)
  
  def kick(self):
    #print "kick"
    self.kicker.turn(127, 340, brake=True )
    #sleep(1.5)
    #print "testing"
    #self.kicker.turn(127, 71, brake=True)
  
  def __del__(self):
    if self.brick != None:
      self.disconnect()


