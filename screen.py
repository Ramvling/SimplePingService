import time
from tkinter import *
import ping
import threading

pm = ping.PingManager()

CLOCKBG = '#457484'
CLOCKTXT = '#FAE9D5'
ADDRBG = '#4B271C'
ADDRTXT = '#E8FFF9'
STATBG = '#A65831'
SELECTED = '#51ABFF'

def clockTick():
	timeString = time.strftime("%H"+":" + "%M" + ":" + "%S")
	clock.configure(text = timeString)
	root.update()
	root.after(1000, clockTick)

def pingNext():
	while(True):
		print("async?")
		curTextLabel = pm.peakNext().labelTxt
		curTextLabel.configure(fg = SELECTED)
		pm.peakNext().labelStat.configure(text = "")
		root.update()
		status = pm.nextPing()
		curTextLabel.configure(fg = SELECTED)
		root.update()
		time.sleep(5)
		curTextLabel.configure(fg = ADDRTXT)
class PingDisplayManager:
	def __init__(self, pm):
		self.pingManager = pm
		self.labels = []
	def generateLabels(self):
		labels = []
		curx, cury = 0, 1
		xpad,ypad = 20, 30
		fontSize = int(w*0.02)
		for addr in self.pingManager.toPoll:
			new = Label(root,bg = ADDRBG,fg=ADDRTXT, text = addr.address,font=("Ariel",fontSize))
			newStat = Label(root, bg=STATBG,text = "not pinged yet", font=("Ariel", fontSize))
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
root.configure(background='blue')
bg_image = PhotoImage(file="bg.gif")
bg = Label(image = bg_image)
bg.place(x = 0, y = 0)
pDM = PingDisplayManager(pm)
w,h = root.winfo_screenwidth(),root.winfo_screenheight()
#root.overrideredirect(1)
root.geometry("%dx%d+0+0" % (w,h))
root.focus_set()
root.bind("<Escape>", lambda e: e.widget.quit())
pingThread = threading.Thread(target=pingNext)
clock = Label(root, text= "",font = ("Helvetica",int(w*0.14) ),width = 10, background = CLOCKBG,fg=CLOCKTXT)
clock.grid(row=0,columnspan = 1000,sticky=N+W+E)
clockTick()
pDM.generateLabels()
pingThread.start()
root.mainloop()

