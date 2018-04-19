import socket
from packet import Ack_Packet

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 50001))
window_size = 5
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
  if seq_no>= window_base and seq_no<(window_base+window_size):
    p = Ack_Packet(0, seq_no)
    print('sequence number',seq_no)
    s.sendall(p.encode())
    my_dict[seq_no]= string
    if seq_no==window_base:
      while 1:
        if my_dict.get(window_base)== None:
          break
        else:
          print('window_base', window_base)
          file_data += my_dict[window_base]
          window_base += 1


with open("out-file.jpg", "wb") as out_file:
  out_file.write(file_data)

s.close()
