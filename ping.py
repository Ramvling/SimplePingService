import socket
import time
import struct
import os

#constants
ICMP = 1
ICMP_ECHO = 8
ICMP_TYPE = 0

class PingCanidate:
	def _init_(self, addr):
		self.addr = addr
		self.ip = socket.gethostbyname(addr)





def checksum(data):
	csum = 0
	for i in range(0, len(data),2):
		w = data[i] + (data[i+1] << 8)
		s = csum + w
		csum = (s & 0xffff) + (s >> 16)
	return ~csum & 0xffff
		

def createPing(ID):
	dummyHead = struct.pack('BBHHH', ICMP_ECHO, ICMP_TYPE, 0, ID,1)
	data = struct.pack('f', time.time())
	csum = checksum(dummyHead+data)
	head = struct.pack('BBHHH', ICMP_ECHO, ICMP_TYPE, csum, ID, 1)
	return head +  data

try:
	sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, ICMP)	
except socket.error:
	print("error")
ping = createPing(os.getpid())
print(ping)
sock.sendto(ping,(socket.gethostbyname('www.google.com'),1))
while(True):
	data = sock.recv(2048)
	print("Data received")
	print(data)
	print('oo')
