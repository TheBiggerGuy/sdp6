from Tkinter import *

class Application(Frame):
  
  UP    = 0
  DOWN  = 1
  LEFT  = 2
  RIGHT = 3
  STOP  = 4
  
  def __init__(self, master=None):
    Frame.__init__(self, master)
    self.pack()
    self.__createWidgets()
    self.bind_all('<Key>', self.__keypress)
  
  def __send_command_up(self):
    self.__send_command(self.UP)
  def __send_command_down(self):
    self.__send_command(self.DOWN)
  def __send_command_left(self):
    self.__send_command(self.LEFT)
  def __send_command_right(self):
    self.__send_command(self.RIGHT)
  def __send_command_stop(self):
    self.__send_command(self.STOP)
  
  def __send_command(self, command):
    if command == self.UP:
      print "up"
    elif command == self.DOWN:
      print "down"
    elif command == self.LEFT:
      print "left"
    elif command == self.RIGHT:
      print "right"
    elif command == self.STOP:
      print "stop"
    else:
      print "bad command"

  def __createWidgets(self):
    self.QUIT = Button(self)
    self.QUIT["text"] = "QUIT"
    self.QUIT["command"] =  self.quit

    self.QUIT.pack({"side": "bottom"})
    
    self.button_up = Button(self)
    self.button_up["text"] = "Up",
    self.button_up["command"] = self.__send_command_up
    
    self.button_dn = Button(self)
    self.button_dn["text"] = "Down",
    self.button_dn["command"] = self.__send_command_down
    
    self.button_le = Button(self)
    self.button_le["text"] = "Left",
    self.button_le["command"] = self.__send_command_left
    
    self.button_ri = Button(self)
    self.button_ri["text"] = "Right",
    self.button_ri["command"] = self.__send_command_right
    
    self.button_st = Button(self)
    self.button_st["text"] = "Stop",
    self.button_st["command"] = self.__send_command_stop

    self.button_up.pack({"side": "top"})
    self.button_dn.pack({"side": "bottom"})
    self.button_le.pack({"side": "left"})
    self.button_ri.pack({"side": "right"})
    self.button_st.pack({"side": "top"})

  def __keypress(self, event):
    
    if event.keysym == 'Escape':
      root.destroy()
    elif event.keysym == 'Up':
      self.__send_command(self.UP)
    elif event.keysym == 'Down':
      self.__send_command(self.DOWN)      
    elif event.keysym == 'Left':
      self.__send_command(self.LEFT)
    elif event.keysym == 'Right':
      self.__send_command(self.RIGHT)
    elif event.keysym == 's':
      self.__send_command(self.STOP)

if __name__ == '__main__':
  root = Tk()
  app = Application(master=root)
  app.mainloop()
