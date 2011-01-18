#!/usr/bin/env python

import sys, os
import pygtk, gtk, gobject
import pygst
pygst.require("0.10")
import gst
import vte
import cairo


from time import time

class GTK_Main(object):
  
  def __init__(self, debug=False):
    # save init values
    self.debug=debug
    self.fullscreen = False # this is technicaly not consistant as it is not chnaged on system uests
    self.pipeline = None
    
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
    
    self.movie_window = gtk.DrawingArea()
    self.movie_window.set_size_request(500, 400)
    self.movie_window.connect('expose_event', self.expose_moviewindow)
    hbox_rightpanel_top.add(self.movie_window)
    
    self.vte = vte.Terminal()
    self.vte.connect ("child-exited", self.respawn_vte)
    self.vte.fork_command()
    hbox_rightpanel_bottom.add(self.vte)
    
    self.window.show_all()
  
  def expose_moviewindow(self, widget=None, data=None):
    if self.pipeline != None:
      return
    drawable = self.movie_window.window
    pixbuf = gtk.gdk.pixbuf_new_from_file("default.png")
    ctx = drawable.cairo_create()
    ctx.set_source_pixbuf(pixbuf,0,0)
    x, y = drawable.get_size()
    ctx.scale(x, y)
    ctx.paint()
    ctx.stroke()

  def respawn_vte(self, widget):
    self.vte.fork_command()
  
  def save_frame(self, widget=None, data=None):
    drawable = self.movie_window.window
    colormap = drawable.get_colormap()
    pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, 0, 8, *drawable.get_size())
    pixbuf = pixbuf.get_from_drawable(drawable, colormap, 0,0,0,0, *drawable.get_size())
    name = "frame_" + str( time() ).replace(".", "")
    pixbuf.save(name + ".png", 'png')
    pixbuf.save(name + ".jpeg", 'jpeg')

  
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
    elif data.keyval == 65307: # Esc65480
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
    if self.pipeline == None:
      self.start_feed()
    else:
      self.stop_feed()
            
  def on_message(self, bus, message):
    t = message.type
    if t == gst.MESSAGE_EOS: # end of feed
      self.stop_feed()
    elif t == gst.MESSAGE_ERROR:
      err, debug = message.parse_error()
      print "Error: %s" % err, debug
      self.stop_feed()
  
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
  
  def start_feed(self):
    self.build_pipeline()
    self.pipeline.set_state(gst.STATE_PLAYING)
    self.button.set_label("Stop")
    self.button.set_active(True)
  
  def stop_feed(self):
    self.pipeline.set_state(gst.STATE_NULL)
    self.pipeline = None
    self.button.set_label("Start Feed")
    self.button.set_active(False)
    self.expose_moviewindow()
  
  def build_pipeline(self):
    # make the gstreamer pipline
    self.pipeline = gst.Pipeline("webcam")
    
    if self.feed_radio == "test":
      source = gst.element_factory_make("videotestsrc", "webcam-source")
    else:
      source = gst.element_factory_make("v4l2src", "webcam-source")
    
    videosink = gst.element_factory_make("autovideosink", "video-output")
    
    if self.button_fixcolour.get_active():
      colorspace = gst.element_factory_make("ffmpegcolorspace", "colorspace")
      self.pipeline.add(source, colorspace, videosink)
      gst.element_link_many(source, colorspace, videosink)
    else:
      self.pipeline.add(source, videosink)
      gst.element_link_many(source, videosink)

    bus = self.pipeline.get_bus()
    bus.add_signal_watch()
    bus.enable_sync_message_emission()
    bus.connect("message", self.on_message)
    bus.connect("sync-message::element", self.on_sync_message)
  
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

