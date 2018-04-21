import config
import time

from packet import Packet

def check_acks(ack_dict):
  for seq_no, ack in ack_dict.items():
    if not ack:
      return False
  return True

def sr_sw(conn, file, window_size):
  timeout = config.timeout
  window_base = 0
  packet_num = 0
  timer_dict = {}
  packet_dict = {}
  ack_dict = {}
  while True:
    if packet_num >= window_base and packet_num < window_base + window_size:
      piece = file.read(512)
      if piece == "".encode():
        if check_acks(ack_dict):
          break # end of file
      else:
        packet = Packet(piece, packet_num)
        if (config.decision(config.plp)):
          if (config.decision(config.pcp)):
            conn.sendall(packet.encode(False))
            print ('Sent #', packet_num)
          else:
            conn.sendall(packet.encode(True))
            print('Corrupted #', packet_num)
        else:
          print('Lost #', packet_num)
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
    except BlockingIOError:
      pass

    for seq_no, timestamp in timer_dict.items():
      if timestamp < time.time():
        print('Timeout #', seq_no)
        conn.sendall(packet_dict[seq_no].encode(False))
        timer_dict[seq_no] = time.time() + timeout

  conn.close()

def selective_repeat(conn, file):
  sr_sw(conn, file, config.window_size)
  

def stop_and_wait(conn, file):
  sr_sw(conn, file, 1)
