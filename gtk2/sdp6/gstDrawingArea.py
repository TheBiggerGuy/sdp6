import cairo
import pygst
pygst.require("0.10")
import gst
import pygtk, gtk, gobject

import logging
from time import time

class GstDrawingArea(gtk.DrawingArea):
  
  def __init__(self):
    gtk.DrawingArea.__init__(self)
    
    self.pipeline = None
    
    self.log = logging.getLogger("GstDrawingArea")
    
    self.gc = None
    self.width  = 0
    self.heigth = 0
    
    self.connect('expose_event',  self.__on_expose_event)
    self.connect('size-allocate', self.__on_size_allocate)
    self.connect('realize',       self.__on_realize)
    
    #self.set_size_request(500, 400)
    
    self.log.debug("GstDrawingArea init ok")
    
    self.imageToShow = None

  
  def __on_realize(self, widget):
    self.log.debug("__on_realize")
    self.gc = widget.window.new_gc()
  
  def __on_size_allocate(self, widget, allocation):
    self.log.debug("__on_realize")
    self.width = allocation.width
    self.height = allocation.height
  
  def __on_expose_event(self, widget=None, data=None):
    self.log.debug("__on_expose_event")
    
    if self.pipeline != None:
      return
    drawable = self.window
    
    if self.imageToShow == None:
      pixbuf = gtk.gdk.pixbuf_new_from_file("logo.png")
    else:
      image = self.imageToShow
      pixbuf = gtk.gdk.pixbuf_new_from_data(image.imageData, gtk.gdk.COLORSPACE_RGB, False,
                image.depth, image.width, image.height, image.widthStep)
    
    #x, y = drawable.get_size()
    pixbuf = pixbuf.scale_simple(self.width, self.height, gtk.gdk.INTERP_NEAREST)
    
    ctx = drawable.cairo_create()
    ctx.set_source_pixbuf(pixbuf,0,0)
    ctx.paint()
    ctx.stroke()
  
  def show_img(self, img):
    self.log.debug("show_img")
    if self.is_playing():
      self.stop_video()
    
    self.imageToShow = img
    self.__on_expose_event()
  
  def get_frame(self, widget=None, data=None):
    drawable = self.window
    colormap = drawable.get_colormap()
    pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, 0, 8, *drawable.get_size())
    pixbuf = pixbuf.get_from_drawable(drawable, colormap, 0,0,0,0, *drawable.get_size())
    
    return pixbuf
  
  def save_frame_to_file(self, widget=None, data=None):
    pixbuf = self.get_frame(widget=widget, data=data)
    
    name = "frame_" + str( time() ).replace(".", "")+ ".png"
    pixbuf.save(name, 'png')
    self.log.info("Screen grab '" + name + "' made")
    
    return name
  
  def __gst_on_message(self, bus, message):
    t = message.type
    if t == gst.MESSAGE_EOS: # end of feed
      self.stop_feed()
    elif t == gst.MESSAGE_ERROR:
      err, debug = message.parse_error()
      self.log.error("Error: %s" % err, debug)
      self.stop_feed()
  
  def __gst_on_sync_message(self, bus, message):
    self.log.debug("__gst_on_sync_message")
    
    if message.structure is None:
      return
    message_name = message.structure.get_name()
    if message_name == "prepare-xwindow-id":
      imagesink = message.src
      imagesink.set_property("force-aspect-ratio", True)
      gtk.gdk.threads_enter()
      imagesink.set_xwindow_id(self.window.xid)
      gtk.gdk.threads_leave()
  
  def __build_pipeline(self, sourse, fixcolour=False, rotation="clockwise", text="%feed_type%"):
    
    # pare the text
    if sourse == "test":
      text = text.replace("%feed_type%", "Test Feed")
    else:
      text = text.replace("%feed_type%", "Real Feed")
    
    # make the gstreamer pipline
    self.pipeline = gst.Pipeline("webcam")
    
    # make the pipline elements
    if sourse == "test":
      source = gst.element_factory_make("videotestsrc", "webcam-source")
    else:
      source = gst.element_factory_make("v4l2src", "webcam-source")
    
    videorotate = gst.element_factory_make("videoflip", "rotate video")
    videorotate.set_property("method", rotation)
    
    textoverlay = gst.element_factory_make("textoverlay", "textoverlay")
    textoverlay.set_property("text", text)
    textoverlay.set_property("valign", "top")
    textoverlay.set_property("halign", "right")
    textoverlay.set_property("shaded-background", "yes")
    textoverlay.set_property("font-desc", "Sans Bold 18")
    
    videosink = gst.element_factory_make("autovideosink", "video-output")
    
    # add the elemnts to the pipline
    if fixcolour:
      colorspace1 = gst.element_factory_make("ffmpegcolorspace", "colorspace1")
      colorspace2 = gst.element_factory_make("ffmpegcolorspace", "colorspace2")
      self.pipeline.add(source, colorspace1, videorotate, colorspace2, textoverlay, videosink)
      gst.element_link_many(source, colorspace1, videorotate, colorspace2, textoverlay, videosink)
    else:
      self.pipeline.add(source, videorotate, textoverlay, videosink)
      gst.element_link_many(source, videorotate, textoverlay, videosink)
    
    # get accses to the pipline message bus
    bus = self.pipeline.get_bus()
    bus.add_signal_watch()
    bus.enable_sync_message_emission()
    bus.connect("message", self.__gst_on_message)
    bus.connect("sync-message::element", self.__gst_on_sync_message)
  
  def start_video(self, sourse="test", fixcolour=False, rotation=False):
    if self.pipeline == None:
      self.stop_video()
    if rotation:
      self.__build_pipeline(sourse=sourse, fixcolour=fixcolour, rotation="counterclockwise")
    else:
      self.__build_pipeline(sourse=sourse, fixcolour=fixcolour)
    self.pipeline.set_state(gst.STATE_PLAYING)
  
  def stop_video(self):
    if self.pipeline != None:
      self.pipeline.set_state(gst.STATE_NULL)
      self.pipeline = None
    self.__on_expose_event()
  
  def is_playing(self):
    return (self.pipeline != None)
  
  def __del__(self):
    self.log.debug("__del__")

if __name__ == "__main__":
  print "Canot be run as main"

