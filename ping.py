import socket
import time
import struct
import os
import select

#constants
ICMP = 1
ICMP_ECHO = 8
ICMP_TYPE = 0
S_TO_MS = 1000

class Address:
	def __init__(self, addr):
		self.address = addr
		self.online = True
		self.labelTxt = None
		self.labelStat = None
	def isOnline(self):
		return self.online


class PingManager:
	def __init__(self):
		self.current = 0
		self.toPoll = [Address('www.google.com'),Address('www.bing.com'), Address('www.yahoo.com'),
			Address('www.tumblr.com'), Address('www.reddit.com'), Address('www.neopets.com'), Address('www.room409.xyz')]

	def peakNext(self):
		return self.toPoll[self.current]

	def checksum(self,data):
		csum = 0
		for i in range(0, len(data),2):
			w = data[i] + (data[i+1] << 8)
			s = csum + w
			csum = (s & 0xffff) + (s >> 16)
		return ~csum & 0xffff	

	def prettyPrintTime(self, t):
		t = t * S_TO_MS
		t = float("{0:.2f}".format(t))
		return ("Ping took " + str(t) + " ms")

	def createPing(self,ID):
		dummyHead = struct.pack('BBHHH', ICMP_ECHO, ICMP_TYPE, 0, ID,1)
		data = struct.pack('f', time.time())
		csum = self.checksum(dummyHead+data)
		head = struct.pack('BBHHH', ICMP_ECHO, ICMP_TYPE, csum, ID, 1)
		return head +  data

	def sendPing(self,addr):
		try:
			sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, ICMP)	
		except socket.error:
			print("error")
		ping = self.createPing(os.getpid())
		sock.sendto(ping,(socket.gethostbyname(addr),1))
		return self.recvPing(sock)

	def recvPing(self,sock):
		toUpdate = self.toPoll[self.current].labelStat
		start = time.time()
		ready = select.select([sock],[],[], 5.0)
		if (ready[0]):
			data = sock.recv(2048)
			end = time.time()
			t = end - start
			print(self.prettyPrintTime(t))
			toUpdate.configure(text = self.prettyPrintTime(t), fg = 'green')
			return (t, data)	
		toUpdate.configure(text = "Ping timed out", fg = 'red')
		print("Ping timed out")
		return(999999999999, [])

	def nextPing(self):
		t, __ = self.sendPing(self.toPoll[self.current].address)
		self.current += 1
		self.current %= len(self.toPoll)
		return self.prettyPrintTime(t) 

	def runPings(self, timeOut):
		# runs pings forever
		while(True):
			for addr in self.toPoll:
				print('pinging ' + addr.address)
				self.sendPing(addr)
				time.sleep(5.5)
	def addAddr(self, newAddr):
		self.toPoll.append(newAddr)
