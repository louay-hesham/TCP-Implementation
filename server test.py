import socket
import config
from server_functions import *

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((config.TCP_IP, config.TCP_PORT))
s.listen(1)

conn, addr = s.accept()
conn.setblocking(0)
print('Connection established.')

with open("server_files/shark.jpg", "rb") as file:
  if config.algorithm == 'SR':
    selective_repeat(conn, file)
  elif config.algorithm == 'S&W':
    stop_and_wait(conn, file)