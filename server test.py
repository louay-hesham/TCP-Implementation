import socket
from packet import Packet

p = Packet('hello world', 5)
print(p)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 50000))
s.listen(1)
conn, addr = s.accept()
conn.sendall(p.encode())
print(str(p.seq_no) + 'is sent')


# while 1:
#   conn, addr = s.accept()
#   conn.sendall(data)
#   # while 1:
#     # data = conn.recv(1024)
#     # if not data:
#     #   break
#   conn.sendall(data)

conn.close()

