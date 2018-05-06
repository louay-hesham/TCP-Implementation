import time
from packet import Packet
from common_functions import *

def check_acks(ack_dict):
  for seq_no, ack in ack_dict.items():
    if not ack:
      return False
  return True

def send_packet(packet, seq_no, conn, config):
  try:
    if (decision(config.plp)):
      if (decision(config.pcp)):
        conn.sendall(packet.encode())
        print ('Sent #', seq_no)
      else:
        conn.sendall(packet.encode(True))
        print('Corrupted #', seq_no)
    else:
      print('Lost #', seq_no)
  except Exception as e :
    print(e)
    
def sr_sw(conn, file, window_size, config):
  timeout = config.timeout
  window_base = 0
  packet_num = 0
  timer_dict = {}
  packet_dict = {}
  ack_dict = {}
  while True:
    if packet_num >= window_base and packet_num < window_base + window_size:
      piece = file.read(config.data_size)
      if piece == "".encode():
        if check_acks(ack_dict):
          break # end of file
      else:
        packet = Packet(piece, packet_num)
        send_packet(packet, packet_num, conn, config)
        packet_dict[packet_num] = packet
        ack_dict[packet_num] = False
        timer_dict[packet_num] = time.time() + timeout      
        packet_num += 1

    try:
      ack = conn.recv(6)
      if ack:
        seq_no = int.from_bytes(ack[0:4], 'big')
        checksum = int.from_bytes(ack[4:], 'big')
        print('Acknowledged #' + str(seq_no))
        ack_dict[seq_no] = True
        timer_dict.pop(seq_no)
        if seq_no == window_base:
          packet_dict.pop(seq_no)
          try:
            while ack_dict[window_base]:
              window_base += 1
              print("Window base = ", window_base)
          except KeyError:
            pass        
    except (BlockingIOError, KeyError):
      pass

    for seq_no, timestamp in timer_dict.items():
      if timestamp < time.time():
        print('Timeout #', seq_no)
        send_packet(packet_dict[seq_no], seq_no, conn, config)
        timer_dict[seq_no] = time.time() + timeout

  print(conn)
  conn.close()

def selective_repeat(conn, file, config):
  sr_sw(conn, file, config.window_size, config)
  

def stop_and_wait(conn, file, config):
  sr_sw(conn, file, 1, config)

def go_back_n(conn, file, config):
  timeout = config.timeout
  window_base = 0
  window_size = config.window_size
  packet_num = 0
  timer_dict = {}
  packet_dict = {}
  ack_dict = {}
  while True:
    if packet_num >= window_base and packet_num < window_base + window_size:
      piece = file.read(config.data_size)
      if piece == "".encode():
        if check_acks(ack_dict):
          break # end of file
      else:
        packet = Packet(piece, packet_num)
        send_packet(packet, packet_num, conn, config)
        packet_dict[packet_num] = packet
        ack_dict[packet_num] = False
        timer_dict[packet_num] = time.time() + timeout      
        packet_num += 1

    try:
      ack = conn.recv(6)
      if ack:
        seq_no = int.from_bytes(ack[0:4], 'big')
        checksum = int.from_bytes(ack[4:], 'big')
        while window_base <= seq_no:
          print('Acknowledged #' + str(window_base))
          ack_dict[window_base] = True
          timer_dict.pop(window_base)
          packet_dict.pop(window_base)
          window_base += 1
          print("Window base = ", window_base)
    except (BlockingIOError, KeyError):
      pass

    for seq_no, timestamp in timer_dict.items():
      if timestamp < time.time():
        while seq_no < window_base + window_size:
          try:
            print('Timeout #', seq_no)
            send_packet(packet_dict[seq_no], seq_no, conn, config)
            timer_dict[seq_no] = time.time() + timeout      
          except KeyError:
            pass
          seq_no += 1
        break

  print(conn)
  conn.close()  
