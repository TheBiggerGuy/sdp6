from Tkinter import *
from sdp6 import Robot
from sdp6 import RobotNotFoundError

class Application(Frame):
  
  MAX_MOTOR_POWER = 127
  BT_ADDRESS = "00:16:53:08:A0:E6"
  
  def __init__(self, master=None):
    Frame.__init__(self, master)
    self.pack()
    self.__createWidgets()
    self.bind_all('<Key>', self.__keypress)
    self.robot = None
  
  def __send_command_up(self):
    if self.robot != None:
      self.robot.up()
  def __send_command_down(self):
    if self.robot != None:
      self.robot.down()
  def __send_command_left(self):
    if self.robot != None:
      self.robot.left()
  def __send_command_right(self):
    if self.robot != None:
      self.robot.right()
  def __send_command_stop(self):
    if self.robot != None:
      self.robot.stop()
  def __send_command_kick(self):
    if self.robot != None:
      self.robot.kick()
  def __send_command_buzz(self):
    if self.robot != None:
      self.robot.buzz()
  def __send_command_power(self, value):
    if self.robot != None:
      self.robot.set_power(value)
  
  def __connect(self):
    self.button_connect["text"] = "Connecting"
    try:
      # first try to find are know robot
      self.robot = Robot(host=self.BT_ADDRESS)
    except RobotNotFoundError: # TODO
      # try to find any robot
      self.robot = Robot()
    except Exception as error:
      print "Robot Error" # + str(error)
      self.button_connect["text"] = "Connect"
      self.button_connect["state"] = "active"
      raise error
    
    self.scale_power.set(self.robot.get_power())
    self.button_up["state"] = "active"
    self.button_dn["state"] = "active"
    self.button_le["state"] = "active"
    self.button_ri["state"] = "active"
    self.button_st["state"] = "active"
    self.button_bz["state"] = "active"
    self.scale_power["state"] = "active"
    self.button_connect["state"] = "disabled"
    self.button_connect["text"] = "Connected"

  def __createWidgets(self):
    self.QUIT = Button(self)
    self.QUIT["text"] = "QUIT"
    self.QUIT["command"] =  self.quit

    self.QUIT.pack({"side": "bottom"})
    
    self.button_up = Button(self)
    self.button_up["text"] = "Up"
    self.button_up["command"] = self.__send_command_up
    self.button_up["state"] = "disabled"
    
    self.button_dn = Button(self)
    self.button_dn["text"] = "Down"
    self.button_dn["command"] = self.__send_command_down
    self.button_dn["state"] = "disabled"
    
    self.button_le = Button(self)
    self.button_le["text"] = "Left"
    self.button_le["command"] = self.__send_command_left
    self.button_le["state"] = "disabled"
    
    self.button_ri = Button(self)
    self.button_ri["text"] = "Right"
    self.button_ri["command"] = self.__send_command_right
    self.button_ri["state"] = "disabled"
    
    self.button_st = Button(self)
    self.button_st["text"] = "Stop"
    self.button_st["command"] = self.__send_command_stop
    self.button_st["state"] = "disabled"
    
    self.button_bz = Button(self)
    self.button_bz["text"] = "Buzz"
    self.button_bz["command"] = self.__send_command_buzz
    self.button_bz["state"] = "disabled"
    
    self.button_connect = Button(self)
    self.button_connect["text"] = "Connect"
    self.button_connect["command"] = self.__connect
    
    self.scale_power = Scale(self)
    self.scale_power["from_"] = -self.MAX_MOTOR_POWER
    self.scale_power["to"] = self.MAX_MOTOR_POWER
    self.scale_power["orient"] = "horizontal"
    self.scale_power["command"] = self.__send_command_power
    self.scale_power["state"] = "disabled"
    
    self.button_connect.pack({"side": "bottom"})
    self.scale_power.pack({"side": "bottom"})
    self.button_bz.pack({"side": "bottom"})
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
    elif event.keysym == 'space':
      self.__send_command_kick()
    elif event.keysym == 's':
      self.__send_command_stop()
    elif event.keysym == 'b':
      self.__send_command_buzz()
    elif event.keysym == 'c':
      self.__connect()

if __name__ == '__main__':
  print "This should work but havent tested it it yet\nTry the last commit if it does not\nguy"
  root = Tk()
  app = Application(master=root)
  try:
    app.mainloop()
  except KeyboardInterrupt:
    print "bye bye"
