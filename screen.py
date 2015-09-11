import time
import tkinter as tk
import ping

pm = ping.PingManager()

while (True):
	print(time.strftime("%H"+":" + "%M" + ":" + "%S"))
	pm.nextPing()
	time.sleep(1)
