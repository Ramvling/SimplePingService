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

class PingCanidate:
	def _init_(self, addr):
		self.addr = addr
		self.ip = socket.gethostbyname(addr)

class PingManager:
	def __init__(self):
		self.toPoll = ['www.google.com', 'www.room409.xyz']

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
		print("Ping took " + str(t) + " ms")

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
		print(ping)
		sock.sendto(ping,(socket.gethostbyname(addr),1))
		self.recvPing(sock)

	def recvPing(self,sock):
		start = time.time()
		ready = select.select([sock],[],[], 5.5)
		if (ready[0]):
			data = sock.recv(2048)
			end = time.time()
			t = end - start
			self.prettyPrintTime(t)
			return (t, data)	
		print("Ping timed out")
		return(999999999999, [])

	def runPings(self, timeOut):
		while(True):
			for addr in self.toPoll:
				print('pinging ' + addr)
				self.sendPing(addr)
				time.sleep(5.5)
	def addAddr(self, newAddr):
		self.toPoll.append(newAddr)		

pm = PingManager()
pm.runPings(2)
