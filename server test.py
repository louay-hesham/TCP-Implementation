import socket
import config
from server_functions import *

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((config.TCP_IP, config.TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print(conn,addr)
conn.setblocking(0)
print('Connection established.')

while 1:
  try:
    data = conn.recv(512)
    if data:
      length = int.from_bytes(data[0:2], 'big')
      seq_no = int.from_bytes(data[2:6], 'big')
      checksum = int.from_bytes(data[6:8], 'big')
      filename = data[8:].decode()
      break
  except (BlockingIOError, KeyError):
      pass

print('Request received of', filename)
with open("server_files/" + filename, "rb") as file:
  if config.algorithm == 'SR':
    selective_repeat(conn, file)
  elif config.algorithm == 'S&W':
    stop_and_wait(conn, file)
  elif config.algorithm == 'GBN':
    go_back_n(conn, file)