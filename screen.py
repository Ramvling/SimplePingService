import time
from tkinter import *
import ping
import threading

pm = ping.PingManager()

def clockTick():
	timeString = time.strftime("%H"+":" + "%M" + ":" + "%S")
	clock.configure(text = timeString)
	root.update()
	root.after(1000, clockTick)

def pingNext():
	while(True):
		print("async?")
		status = pm.nextPing()
		pingLabel.configure(text = status)
		root.update()
		time.sleep(5)

root = Tk()
pingThread = threading.Thread(target=pingNext)
clock = Label(root, text= "", font=("Ariel", 100))
clock.pack()
clockTick()
pingLabel = Label(root, text="THIS IS A TEST")
pingLabel.pack()
pingThread.start()
root.mainloop()

