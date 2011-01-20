#!/usr/bin/env python

import sys, os
import pygtk, gtk, gobject
import vte

from gst_widget import GstDrawingArea

from time import time
from socket import gethostname

import logging

class GTK_Main(object):
  
  def __init__(self):
    # save init values
    self.fullscreen = False # this is technicaly not consistant as it is not chnaged on system uests
    self.robot = None
    
    self.log = logging.getLogger("GTK_Main")
    
    # do some jazz to see if we are on dice and or video pc
    self.hostname = gethostname()
    self.are_in_inf = False
    self.are_on_vision_pc = False
    if self.hostname.endswith("inf.ed.ac.uk"):
      self.are_in_inf = True
      if self.hostname.split(".")[0] in ["lappy", "mitsubishi", "lexus", "honda"]:
        self.are_on_vision_pc = True
    
    # setup the window
    self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    self.window.set_title("SDP 6")
    self.window.set_default_size(850, 400)
        
    self.window.set_events(gtk.gdk.KEY_PRESS_MASK|gtk.gdk.KEY_RELEASE_MASK)
    self.window.connect("key_press_event", self.on_key_press)
    self.window.connect("key_release_event", self.on_key_release)
    self.window.connect("destroy", self.clean_quit)
    
    # add widgets
    root_widget = gtk.HBox()
    self.window.add(root_widget)
    
    vbox_rightpanel = gtk.VBox()
    root_widget.add(vbox_rightpanel)
    
    vbox_leftpanel = gtk.VBox()
    vbox_leftpanel.set_size_request(150, 0)
    root_widget.add(vbox_leftpanel)
    
    hbox_rightpanel_top = gtk.HBox()
    vbox_rightpanel.add(hbox_rightpanel_top)
    
    hbox_rightpanel_bottom = gtk.HBox()
    hbox_rightpanel_bottom.set_size_request(0, 100)
    vbox_rightpanel.add(hbox_rightpanel_bottom)
    
    hbox_leftpanel_feed = gtk.HBox()
    hbox_leftpanel_feed.set_size_request(150, 0)
    vbox_leftpanel.add(hbox_leftpanel_feed)
    
    self.button = gtk.ToggleButton("Start Feed")
    self.button.connect("clicked", self.start_stop)
    hbox_leftpanel_feed.add(self.button)
    
    vbox_leftpanel_feed_radio = gtk.VBox()
    hbox_leftpanel_feed.add(vbox_leftpanel_feed_radio)
    
    radio1 = gtk.RadioButton(group=None, label="Real")
    radio1.set_active(True)
    radio1.connect("toggled", self.radio_feed_change)
    vbox_leftpanel_feed_radio.add(radio1)
    
    self.feed_radio = "real"
    
    radio2 = gtk.RadioButton(group=radio1, label="Test")
    vbox_leftpanel_feed_radio.add(radio2)
    
    self.button_fixcolour = gtk.ToggleButton("Fix Colour")
    hbox_leftpanel_feed.add(self.button_fixcolour)
    
    button = gtk.Button("Save Frame")
    button.connect("clicked", self.save_frame)
    vbox_leftpanel.add(button)
    
    self.button_connect = gtk.ToggleButton("Connect")
    self.button_connect.connect("clicked", self.__connect)
    vbox_leftpanel.add(self.button_connect)
    
    for i in range(0, 5):
      button = gtk.Button("test "+str(i))
      vbox_leftpanel.add(button)
    
    self.gst = GstDrawingArea()
    hbox_rightpanel_top.add(self.gst)
    
    #self.vte = vte.Terminal()
    #self.vte.connect ("child-exited", self.respawn_vte)
    #self.vte.fork_command()
    #hbox_rightpanel_bottom.add(self.vte)
    
    self.window.show_all()
    self.log.debug("GTK windows complete")

  #def respawn_vte(self, widget):
  #  self.log.info("VTE respawn")
  #  self.vte.fork_command()
  
  def save_frame(self, widget=None, data=None):
    self.gst.save_frame(widget=widget, data=data)

  
  def on_key_press(self, widget, data=None):
    #if widget == self.vte:
    #  return
    self.log.debug("click")
    if data.keyval == 65362: # up
        self.log.debug("Up")
        if self.robot != None:
          self.robot.up()
    elif data.keyval == 65364: # down
        self.log.debug("Down")
        if self.robot != None:
          self.robot.down()
    elif data.keyval == 65361: # left
        self.log.debug("Left")
        if self.robot != None:
          self.robot.left()
    elif data.keyval == 65363: # right
        self.log.debug("Right")
        if self.robot != None:
          self.robot.right()
    elif data.keyval == 65307: # Esc
        self.clean_quit()
    elif data.keyval == 65480: # F11
      if self.fullscreen:
        self.window.unfullscreen()
        self.fullscreen = False
      else:
        self.window.fullscreen()
        self.fullscreen = True
    elif data.string == "s":
        self.log.debug("Stop!")
    else:
        self.log.debug("on_key_press:\n\tevent: '{event}'\n\tkeyval: '{keyval}'\n\tstring: '{str_}'"\
        .format(event="key_press_unknown_key", keyval=data.keyval, str_=data.string))
  
  def on_key_release(self, widget, data=None):
    self.log.debug("un-click")
  
  def clean_quit(self, widget=None, data=None):
    self.log.debug("Clean Quit")
    gtk.main_quit()
    
  def start_stop(self, widget, data=None):
    if self.gst.is_playing():
      self.stop_feed()
    else:
      self.start_feed()
    
  def start_feed(self):
    fixcolour = self.button_fixcolour.get_active()
    self.gst.start_video(self.feed_radio, fixcolour=fixcolour)
    self.button.set_label("Stop")
    self.button.set_active(True)
  
  def stop_feed(self):
    self.gst.stop_video()
    self.button.set_label("Start Feed")
    self.button.set_active(False)
  
  def radio_feed_change(self, widget, data=None):
    if self.feed_radio == "real":
      self.feed_radio = "test"
    else:
      self.feed_radio = "real"
  
  def __connect(self, widget=None, data=None):
    self.button_connect.set_label("Connecting")
    try:
      # first try to find are know robot
      self.robot = Robot(host=self.BT_ADDRESS)
      self.button_connect.set_label("Conected")
      self.button_connect.set_active(False)
    except Exception as error:
      self.log.error("Robot Error")
      self.button_connect.set_label("Connect")
      self.button_connect.set_active(True)
  

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

