#!/usr/bin/env python

import sys, os
import pygtk, gtk, gobject
import vte

from gst_widget import GstDrawingArea

from time import time

class GTK_Main(object):
  
  def __init__(self, debug=False):
    # save init values
    self.debug=debug
    self.fullscreen = False # this is technicaly not consistant as it is not chnaged on system uests
    
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
    
    for i in range(0, 5):
      button = gtk.Button("test "+str(i))
      vbox_leftpanel.add(button)
    
    # TODO
    self.gst = GstDrawingArea()
    hbox_rightpanel_top.add(self.gst)
    
    self.vte = vte.Terminal()
    self.vte.connect ("child-exited", self.respawn_vte)
    self.vte.fork_command()
    hbox_rightpanel_bottom.add(self.vte)
    
    self.window.show_all()

  def respawn_vte(self, widget):
    self.vte.fork_command()
  
  def save_frame(self, widget=None, data=None):
    self.gst.save_frame(widget=widget, data=data)

  
  def on_key_press(self, widget, data=None):
    if widget == self.vte:
      return
    print "click"
    if data.keyval == 65362: # up
        print "Up"
    elif data.keyval == 65364: # down
        print "Down"
    elif data.keyval == 65361: # left
        print "Left"
    elif data.keyval == 65363: # right
        print "Right"
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
        print "Stop!"
    else:
        if self.debug:
            print "DEBUG:\n\tevent: '{event}'\n\tkeyval: '{keyval}'\n\tstring: '{str_}'"\
            .format(event="key_press_unknown_key", keyval=data.keyval, str_=data.string)
  
  def on_key_release(self, widget, data=None):
    print "un-click"
  
  def clean_quit(self, widget=None, data=None):
    print "Clean Quit"
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
  

if __name__ == '__main__':
  try:
    GTK_Main(debug=True)
    gtk.gdk.threads_init()
    gtk.main()
  except KeyboardInterrupt:
    print "bye bye"

