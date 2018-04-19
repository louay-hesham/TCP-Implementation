import socket
from packet import Packet

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 50000))

while 1: 
  data = s.recv(1024)
  if not data: break
  print ('Received bytes: ', data)
  length = int.from_bytes(data[0:2], 'big')
  seq_no = int.from_bytes(data[2:6], 'big')
  checksum = int.from_bytes(data[6:8], 'big')
  string = data[8:].decode()
  print(length)
  print(seq_no)
  print(checksum)
  print(string)
  
s.close()