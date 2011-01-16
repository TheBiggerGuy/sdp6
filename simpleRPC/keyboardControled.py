from Tkinter import *
from sdp6 import Robot

class Application(Frame):
  
  def __init__(self, master=None):
    Frame.__init__(self, master)
    self.pack()
    self.__createWidgets()
    self.bind_all('<Key>', self.__keypress)
    self.robot = Robot()
  
  def __send_command_up(self):
    self.robot.up()
  def __send_command_down(self):
    self.robot.down()
  def __send_command_left(self):
    self.robot.left()
  def __send_command_right(self):
    self.robot.right()
  def __send_command_stop(self):
    self.robot.stop()

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
      self.__send_command_up()
    elif event.keysym == 'Down':
      self.__send_command_down()      
    elif event.keysym == 'Left':
      self.__send_command_left()
    elif event.keysym == 'Right':
      self.__send_command_right()
    elif event.keysym == 's':
      self.__send_command_stop()

if __name__ == '__main__':
  root = Tk()
  app = Application(master=root)
  app.mainloop()
