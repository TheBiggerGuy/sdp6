import pygtk, gtk, gobject
import cairo

import sys, os, math

class RobotDrawingArea(gtk.DrawingArea):
  
  def __init__(self):    
    gtk.DrawingArea.__init__(self)
    
    self.set_size_request(200, 200)
    self.connect('expose_event', self.__expose_event)
    
    print "GstDrawingArea init ok"
  
  def __expose_event(self, widget=None, data=None):    
    drawable = self.window # =widget
    width, height = drawable.get_size() # =data
    
    print "__expose_event {width}x{height} w={widget} d={data}".\
    format(width=width, height=height, widget=widget, data=data)
    
    context = drawable.cairo_create()
    
    context = self.__draw_clock(context)
    
    #ctx.set_source_pixbuf(pixbuf,0,0)
    context.paint()
    context.stroke()

  def __draw_clock(self, context):
    
    rect = self.get_allocation()
    x = rect.x + rect.width / 2
    y = rect.y + rect.height / 2
    
    radius = min(rect.width / 2, rect.height / 2) - 5
    
    # clock back
    context.arc(x, y, radius, 0, 2 * math.pi)
    context.set_source_rgb(1, 1, 1)
    context.fill_preserve()
    context.set_source_rgb(0, 0, 0)
    context.stroke()
    
    # clock ticks
    for i in xrange(12):
      context.save()
      
      if i % 3 == 0:
        inset = 0.2 * radius
      else:
        inset = 0.1 * radius
        context.set_line_width(0.5 * context.get_line_width())
        
        context.move_to(x + (radius - inset) * math.cos(i * math.pi / 6),
                        y + (radius - inset) * math.sin(i * math.pi / 6))
        context.line_to(x + radius * math.cos(i * math.pi / 6),
                        y + radius * math.sin(i * math.pi / 6))
        context.stroke()
        context.restore()
    return context

class GTK_Main(object):
    
  def __init__(self):
    # setup the window
    self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    self.window.set_title("Test")
    self.window.set_default_size(200, 200)
    
    self.window.connect("destroy", self.__clean_quit)
    
    self.robot = RobotDrawingArea()
    
    # add widget
    self.window.add(self.robot)
    self.window.show_all()
    
  def __clean_quit(self, widget=None, data=None):
    gtk.main_quit()

if __name__ == "__main__":
  #print "Canot be run as main"
  
  try:
    GTK_Main()
    gtk.gdk.threads_init()
    gtk.main()
  except KeyboardInterrupt:
    print "ctrl-c exit"

