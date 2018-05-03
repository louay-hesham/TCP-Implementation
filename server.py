import socket
from server_functions import *
import sys
from _thread import *
import json
import time

def server(config):
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind((config.TCP_IP, config.TCP_PORT))
  s.listen(1)

  while 1:
    conn, addr = s.accept()
    start_new_thread(client_thread, (conn, addr, config))

def client_thread(conn, addr, config):
  print(conn, addr)
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

def start_server(config_str):
  try:
    config_dict = json.loads(config_str)
    config_obj = type('Dummy', (object,), config_dict)
    server(config_obj)
  except Exception as e:
    print(e)
    input('of a7')