#!/usr/bin/env python

import sys, os
import pygtk, gtk, gobject
import pygst
pygst.require("0.10")
import gst

class GTK_Main(object):
  
  def __init__(self, debug=False):
    # save init values
    self.debug=debug
    self.fullscreen = False # this is technicaly not consistant as it is not chnaged on system uests
    
    # setup the window
    self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    self.window.set_title("SDP 6")
    self.window.set_default_size(600, 400)
        
    self.window.set_events(gtk.gdk.KEY_PRESS_MASK|gtk.gdk.KEY_RELEASE_MASK)
    self.window.connect("key_press_event", self.on_key_press)
    self.window.connect("key_release_event", self.on_key_release)
    self.window.connect("destroy", self.clean_quit)
    
    # add widgets
    vbox_leftpanel = gtk.VBox()
    self.window.add(vbox_leftpanel)
    
    vbox_rightpanel = gtk.VBox()
    self.window.add(vbox_rightpanel)
    
    hbox_rightpanel_top = gtk.HBox()
    vbox_rightpanel.add(hbox_rightpanel_top)
    
    hbox_rightpanel_bottom = gtk.HBox()
    vbox_rightpanel.add(hbox_rightpanel_bottom)
    
    self.button = gtk.Button("Start")
    self.button.connect("clicked", self.start_stop)
    vbox.add(self.button)
    
    self.movie_window = gtk.DrawingArea()
    hbox_rightpanel_top.add(self.movie_window)

    self.window.show_all()
    
    # make the gstreamer pipline
    self.pipeline = gst.Pipeline("webcam")
    source = gst.element_factory_make("videotestsrc", "webcam-source")
    colorspace = gst.element_factory_make("ffmpegcolorspace", "colorspace")
    videosink = gst.element_factory_make("autovideosink", "video-output")
    
    self.pipeline.add(source, colorspace, videosink)
    gst.element_link_many(source, colorspace, videosink)

    bus = self.pipeline.get_bus()
    bus.add_signal_watch()
    bus.enable_sync_message_emission()
    bus.connect("message", self.on_message)
    bus.connect("sync-message::element", self.on_sync_message)
  
  def on_key_press(self, widget, data=None):
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
    elif data.string == "s":
        print "Stop!"
    elif data.string == "f":
      if self.fullscreen:
        self.window.unfullscreen()
        self.fullscreen = False
      else:
        self.window.fullscreen()
        self.fullscreen = True
    else:
        if self.debug:
            print "DEBUG:\n\tevent: '{event}'\n\tkeyval: '{keyval}'\n\tstring: '{str_}'"\
            .format(event="key_press_unknown_key", keyval=data.keyval, str_=data.string)
  
  def on_key_release(self, widget, data=None):
    print "un-click"
  
  def clean_quit(self, widget):
    print "Clean Quit"
    gtk.main_quit()
    
  def start_stop(self, w):
    if self.button.get_label() == "Start":
        self.button.set_label("Stop")
        #self.player.get_by_name("file-source").set_property("location", filepath)
        self.pipeline.set_state(gst.STATE_PLAYING)
    else:
      self.pipeline.set_state(gst.STATE_NULL)
      self.button.set_label("Start")
            
  def on_message(self, bus, message):
    t = message.type
    if t == gst.MESSAGE_EOS:
      self.pipeline.set_state(gst.STATE_NULL)
      self.button.set_label("Start")
    elif t == gst.MESSAGE_ERROR:
      err, debug = message.parse_error()
      print "Error: %s" % err, debug
      self.pipeline.set_state(gst.STATE_NULL)
      self.button.set_label("Start")
  
  def on_sync_message(self, bus, message):
    if message.structure is None:
      return
    message_name = message.structure.get_name()
    if message_name == "prepare-xwindow-id":
      imagesink = message.src
      imagesink.set_property("force-aspect-ratio", True)
      gtk.gdk.threads_enter()
      imagesink.set_xwindow_id(self.movie_window.window.xid)
      gtk.gdk.threads_leave()

if __name__ == '__main__':
    GTK_Main(debug=True)
    gtk.gdk.threads_init()
    gtk.main()

