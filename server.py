import socket, random, math, os, time, json, sys
import traceback
from server_functions import *
from _thread import *

def start_server(config_str):
  try:
    config_dict = json.loads(config_str)
    config_obj = type('Dummy', (object,), config_dict)
    server(config_obj)
  except Exception as e:
    print(e)
    print(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2])
    print(traceback.format_exc())
    input('')

def server(config):
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind((config.TCP_IP, config.TCP_PORT))
  s.listen(1)
  port_offset = 1
  while 1:
    conn, addr = s.accept()
    new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    new_port = config.TCP_PORT + port_offset
    new_socket.bind((config.TCP_IP, new_port))
    new_socket.listen(1)
    connection_packet = Packet(new_port.to_bytes(4, 'big'), 0)
    port_offset += 1
    conn.sendall(connection_packet.encode())
    conn2, addr2 = new_socket.accept()

    start_new_thread(client_thread, (conn2, addr2, config))

def client_thread(conn, addr, config):
  print(conn, addr)
  conn.setblocking(0)
  print('Connection established.')

  while 1:
    try:
      data = conn.recv(config.data_size + 8)
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
      selective_repeat(conn, file, config)
    elif config.algorithm == 'S&W':
      stop_and_wait(conn, file, config)
    elif config.algorithm == 'GBN':
      go_back_n(conn, file, config)
