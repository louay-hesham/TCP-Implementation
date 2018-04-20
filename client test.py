import socket
from packet import Ack_Packet
import config
import random

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((config.TCP_IP, config.TCP_PORT))

window_size = config.window_size
window_base = 0
file_data = bytes([])
my_dict={}

while 1:
  data = s.recv(520)
  if not data: break
  # print('Received bytes: ', data)
  length = int.from_bytes(data[0:2], 'big')
  seq_no = int.from_bytes(data[2:6], 'big')
  checksum = int.from_bytes(data[6:8], 'big')
  string = data[8:]
  if seq_no >= window_base and seq_no < (window_base + window_size):
    print('Received #',seq_no)
    if config.decision(config.plp):
      if checksum == config.checksum(string):
        p = Ack_Packet(checksum , seq_no)
        s.sendall(p.encode())
        print('Acknowledged #', seq_no)
    else:
      print ('Ack lost #', seq_no)
      
    my_dict[seq_no]= string
    if seq_no==window_base:
      while 1:
        if my_dict.get(window_base)== None:
          break
        else:
          print('window_base', window_base)
          file_data += my_dict[window_base]
          window_base += 1
  elif seq_no < window_base:
    p = Ack_Packet(config.checksum(my_dict[seq_no]), seq_no)
    print('Received already acked #', seq_no)
    s.sendall(p.encode())

with open("out-file.jpg", "wb") as out_file:
  out_file.write(file_data)

s.close()
