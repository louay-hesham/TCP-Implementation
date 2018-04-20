import socket
from packet import Packet
import time
import config

def check_acks(ack_dict):
  for seq_no, ack in ack_dict.items():
    if not ack:
      return False
  return True

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((config.TCP_IP, config.TCP_PORT))
s.listen(1)

conn, addr = s.accept()
conn.setblocking(0)
print('Connection established.')

with open("server_files/shark.jpg", "rb") as file:
  window_size = config.window_size
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
          conn.sendall(packet.encode())
          print('Sent #' + str(packet_num))
        else:
          print('Lost #' + str(packet_num))
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
              print("Window base = " + str(window_base))
          except KeyError:
            pass        
    except BlockingIOError:
      pass

    for seq_no, timestamp in timer_dict.items():
      if timestamp < time.time():
        print('Timeout #' + str(seq_no))
        conn.sendall(packet_dict[seq_no].encode())
        timer_dict[seq_no] = time.time() + timeout

  conn.close()
