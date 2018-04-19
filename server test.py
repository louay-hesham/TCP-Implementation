import socket
from packet import Packet

p = [Packet('he', 1)] + [Packet('h', 2)] +[Packet('he', 3)]
print(p)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 50001))
s.listen(1)
conn, addr = s.accept()
for i in range (len(p)):
  conn.sendall(p[i].encode())
  data = conn.recv(10)
  if not data: break
  print('Received bytes: ', data)
  seq_no = int.from_bytes(data[0:4], 'big')
  checksum = int.from_bytes(data[4:], 'big')
  if i+1==seq_no:
    print("tamam")
  else :
    print("msh tamam")


  print(str(p[i].seq_no) + ' is sent')


# while 1:
#   conn, addr = s.accept()
#   conn.sendall(data)
#   # while 1:
#     # data = conn.recv(1024)
#     # if not data:
#     #   break
#   conn.sendall(data)

conn.close()

