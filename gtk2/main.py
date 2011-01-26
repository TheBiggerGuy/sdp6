#!/usr/bin/env python

import sys, os
import pygtk, gtk, gobject
import vte

from sdp6 import GstDrawingArea
from sdp6 import Robot
from sdp6 import RobotNotFoundError
from sdp6 import ImageProcess

from socket import gethostname

import logging

class GTK_Main(object):

  BT_ADDRESS = "00:16:53:08:A0:E6"
  
  def __init__(self):
    
    # get a logger
    self.log = logging.getLogger("GTK_Main")
    
    # save init values
    self.fullscreen = False # this is technicaly not consistant as it is not chnaged on system uests
    self.robot = Robot(self.BT_ADDRESS)
    self.feed_radio = "real"
    self.fix_colour = False
    self.half_time = False
    
    # do some jazz to see if we are on dice and or video pc
    self.hostname = gethostname()
    self.are_in_inf = False
    self.are_on_vision_pc = False
    if self.hostname.endswith("inf.ed.ac.uk"):
      self.are_in_inf = True
      if self.hostname.split(".")[0] in ["lappy", "mitsubishi", "lexus", "honda"]:
        self.are_on_vision_pc = True
    
    # setup the window
    builder = gtk.Builder()
    builder.add_from_file("main_ui.xml")
    
    self.window = builder.get_object("window_main")
    
    # change out the image with are video widget
    video_holder_box = builder.get_object("box_videoHolder") 
    video_holder_img = builder.get_object("image_videoHolder")
    self.gst = GstDrawingArea()
    video_holder_box.remove(video_holder_img)
    video_holder_box.add(self.gst)
    
    # connect to GUI events
    self.window.set_events(gtk.gdk.KEY_PRESS_MASK|gtk.gdk.KEY_RELEASE_MASK)
    self.window.connect("key_press_event", self.on_key_press)
    self.window.connect("key_release_event", self.on_key_release)
    self.window.connect("destroy", self.clean_quit)
    builder.connect_signals(self)
    
    # get all wigets that are needed later
    self.table_manualControl = builder.get_object("table_manualControl")
    
    # show the GUI
    self.gst.show()
    self.window.show()
        
    self.log.debug("GTK windows complete")
  
  def save_frame(self, widget=None, data=None):
    self.log.debug("_save_frame")
    if self.gst.is_playing():
      name = self.gst.save_frame_to_file(widget=widget, data=data)
    else:
      self.log.warning("No video to save frame")
  
  def background_remove(self, widget=None, data=None):
    self.log.debug("background_remove")
    if self.gst.is_playing():
      image = self.gst.get_frame(widget=widget, data=data)
      ImageProcess(image).save_png()   #TODO
      #image = ImageProcess(image).get_image()   
      #self.gst.show_img(image)
    else:
      self.log.warning("No video to remove background")
    
  def start_stop(self, widget=None, data=None):
    self.log.debug("__start_stop")
    if self.gst.is_playing():
      self.stop_feed()
    else:
      self.start_feed()
  
  def on_manual_robot_control(self, widget=None, data=None):
    self.log.debug("click")
    print data
  
  def on_key_press(self, widget, data=None):
    self.log.debug("click")
    
    if data.keyval == 65362: # up
      self.log.debug("Up")
      self.robot.up()
    elif data.keyval == 65364: # down
      self.log.debug("Down")
      self.robot.down()
    elif data.keyval == 65361: # left
      self.log.debug("Left")
      self.robot.left()
    elif data.keyval == 65363: # right
      self.log.debug("Right")
      self.robot.right()
    elif data.keyval == 32: # space
      self.log.debug("Kick")
      self.robot.kick()
    elif data.keyval == 65307: # Esc
      self.clean_quit()
    elif data.keyval == 65480: # F11
      if self.fullscreen:
        self.window.unfullscreen()
        self.fullscreen = False
      else:
        self.window.fullscreen()
        self.fullscreen = True
    elif data.string == "s":  # s
      self.log.debug("Stop!")
      self.robot.stop()
    else:
        self.log.debug("on_key_press:\n\tevent: '{event}'\n\tkeyval: '{keyval}'\n\tstring: '{str_}'"\
        .format(event="key_press_unknown_key", keyval=data.keyval, str_=data.string))
        return False # since we dont use the key let the rest of the GUI use it. ie enter and F1
    return True # stop the rest of the GUI reacting
  
  def on_key_release(self, widget, data=None):
    self.log.debug("un-click")
    self.robot.stop()
    return True
  
  def clean_quit(self, widget=None, data=None):
    self.log.debug("Clean Quit")
    self.robot = None
    gtk.main_quit()
    
  def start_feed(self):
    self.gst.start_video(self.feed_radio, fixcolour=self.fix_colour, rotation=self.half_time)
    # TODO
    #self.button.set_label("Stop")
    #self.button.set_active(True)
  
  def stop_feed(self):
    self.gst.stop_video()
    # TODO
    #self.button.set_label("Start Feed")
    #self.button.set_active(False)
  
  def fix_video_colour(self, widget=None, data=None):
    self.log.debug("fix_video_colour")
    self.fix_colour = not self.fix_colour
  
  def flip_video_feed(self, widget=None, data=None):
    self.log.debug("half_time")
    self.half_time = not self.half_time
  
  def connect_to_brick(self, widget=None, data=None):
    self.log.debug("connect_to_brick")
    if not widget.get_active():
      return False # ingnor button when not acctive

    try:
      # first try to find are know robot
      self.robot.connect()
      widget.set_label("Conected")
      widget.set_active(True)
    except Exception as error:
      self.log.error(error)
      widget.set_label("Connect")
      widget.set_active(False)
  
  def radio_feed_change_real(self, widget=None, data=None):
    self.log.debug("radio_feed_change real")
    if self.feed_radio != "real":
      self.feed_radio = "real"
      
  def radio_feed_change_test(self, widget=None, data=None):
    self.log.debug("radio_feed_change test")
    if self.feed_radio != "test":
      self.feed_radio = "test"
      
  def radio_feed_change_file(self, widget=None, data=None):
    self.log.debug("radio_feed_change file")
    if self.feed_radio != "file":
      self.feed_radio = "file"
  
  def change_manual_control(self, widget=None, data=None):
    self.log.debug("change_manual_control")
    if widget.get_active():
      self.log.warning("Request to chnage to manual")
      widget.set_label("Automatic")
      for child in self.table_manualControl.get_children():
        if child != widget:
          child.show()
          if type(child) == gtk.VScale():
            child.set_value( self.robot.get_power() )
    else:
      self.log.warning("Request to chnage to automatic")
      widget.set_label("Manual")
      for child in self.table_manualControl.get_children():
        if child != widget:
          child.hide()
  
  def manual_power_change(self, widget=None, data=None):
    self.log.debug("manual_power_change")
    self.robot.set_power( widget.get_value() )
  
  def on_manual_robot_control_up(self, widget=None, data=None):
    self.robot.up()
  def on_manual_robot_control_down(self, widget=None, data=None):
    self.robot.down()
  def on_manual_robot_control_stop(self, widget=None, data=None):
    self.robot.stop()
  def on_manual_robot_control_left(self, widget=None, data=None):
    self.robot.left()
  def on_manual_robot_control_right(self, widget=None, data=None):
    self.robot.right()
  def on_manual_robot_control_kick(self, widget=None, data=None):
    self.robot.kick()
  def on_manual_robot_control_buzz(self, widget=None, data=None):
    self.robot.buzz()
    
  def __del__(self):
    self.log.info("__del__")
    self.robot = None

if __name__ == '__main__':

  # log all to file
  logging.basicConfig(level=logging.DEBUG,
                      format='%(asctime)s %(name)-20s %(levelname)-8s %(message)s',
                      datefmt='%m-%d %H:%M',
                      filename="log/lastrun.all.log",
                      filemode='w')
  
  # log warnings to file
  handler = logging.FileHandler(filename="log/lastrun.warnings.log", mode="w")
  handler.setLevel(logging.WARNING)
  formatter = logging.Formatter('%(name)-20s: %(levelname)-8s %(message)s')
  handler.setFormatter(formatter)
  logging.getLogger('').addHandler(handler)
  
  # log all to concole
  handler = logging.StreamHandler(sys.stdout)
  handler.setLevel(logging.DEBUG)
  formatter = logging.Formatter('%(name)-15s: %(levelname)-8s: %(message)s')
  handler.setFormatter(formatter)
  logging.getLogger('').addHandler(handler)
  
  # log somthing
  logging.debug("logging started")
  
  try:
    GTK_Main()
    gtk.gdk.threads_init()
    gtk.main()
  except KeyboardInterrupt:
    logging.warn("ctrl-c exit")

