from Tkinter import *

class Application(Frame):
  
  def __init__(self, master=None):
    Frame.__init__(self, master)
    self.pack()
    self.createWidgets()
    self.bind_all('<Key>', self.keypress)
  
  def say_hi(self):
    print "hi there, everyone!"

  def createWidgets(self):
    self.QUIT = Button(self)
    self.QUIT["text"] = "QUIT"
    self.QUIT["fg"]   = "red"
    self.QUIT["command"] =  self.quit

    self.QUIT.pack({"side": "bottom"})
    
    self.button_up = Button(self)
    self.button_up["text"] = "Up",
    self.button_up["command"] = self.say_hi
    
    self.button_dn = Button(self)
    self.button_dn["text"] = "Down",
    self.button_dn["command"] = self.say_hi
    
    self.button_le = Button(self)
    self.button_le["text"] = "Left",
    self.button_le["command"] = self.say_hi
    
    self.button_ri = Button(self)
    self.button_ri["text"] = "Right",
    self.button_ri["command"] = self.say_hi

    self.button_up.pack({"side": "top"})
    self.button_dn.pack({"side": "bottom"})
    self.button_le.pack({"side": "left"})
    self.button_ri.pack({"side": "right"})

  def keypress(self, event):
    
    if event.keysym == 'Escape':
      root.destroy()
      
    elif event.keysym == 'Up':
      print "up"
      
    elif event.keysym == 'Down':
      print "down"
      
    elif event.keysym == 'Left':
      print "left"
      
    elif event.keysym == 'Right':
      print "right"

if __name__ == '__main__':
  root = Tk()
  app = Application(master=root)
  app.mainloop()
