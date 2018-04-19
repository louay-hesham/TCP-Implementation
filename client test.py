import socket
from packet import Ack_Packet

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 50001))

while 1: 
  data = s.recv(10)
  if not data: break
  print ('Received bytes: ', data)
  length = int.from_bytes(data[0:2], 'big')
  seq_no = int.from_bytes(data[2:6], 'big')
  checksum = int.from_bytes(data[6:8], 'big')
  string = data[8:].decode()
 # print(length)
  #print(seq_no)
  print("\n")
  #print(checksum)

  print(string)
  print("\n")
  p=Ack_Packet(0, seq_no)
  s.sendall(p.encode())
  
s.close()