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
		curTextLabel = pm.peakNext().labelTxt
		curTextLabel.configure(fg = 'blue')
		root.update()
		status = pm.nextPing()
		curTextLabel.configure(fg = 'yellow')
		root.update()
		time.sleep(5)
		curTextLabel.configure(fg = 'black')
class PingDisplayManager:
	def __init__(self, pm):
		self.pingManager = pm
		self.labels = []
	def generateLabels(self):
		labels = []
		curx, cury = 0, 1
		xpad,ypad = 50, 30
		fontSize = int(w*0.015)
		for addr in self.pingManager.toPoll:
			new = Label(root, text = addr.address,font=("Ariel",fontSize))
			newStat = Label(root, text = "not pinged yet", font=("Ariel", fontSize))
			new.grid(row = cury, column = curx,padx = xpad,pady = ypad)
			xLength = len(addr.address) * ((int(w*0.03)))
			newStat.grid(row = cury, column = curx + 1,padx = xpad,pady = ypad)
			labels.append(new)
			addr.labelTxt = new
			addr.labelStat = newStat
			cury += 1
			if (cury > 5):
				cury = 1
				curx += 2
root = Tk()
pDM = PingDisplayManager(pm)
w,h = root.winfo_screenwidth(),root.winfo_screenheight()
#root.overrideredirect(1)
root.geometry("%dx%d+0+0" % (w,h))
root.focus_set()
root.bind("<Escape>", lambda e: e.widget.quit())
pingThread = threading.Thread(target=pingNext)
clock = Label(root, text= "",font = ("Ariel",int(w*0.13) ))
clock.grid(row=0,columnspan = 40,sticky=N+W)
clockTick()
pDM.generateLabels()
pingThread.start()
root.mainloop()

