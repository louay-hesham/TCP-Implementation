import time
from packet import Packet
from common_functions import *

def check_acks(ack_dict):          # a method to check if the acknolegment is recieved before
  for seq_no, ack in ack_dict.items():
    if not ack:
      return False
  return True

def send_packet(packet, seq_no, conn, config):  # method to send packet
  try:
    if (decision(config.plp)):            # decision to send or not based on package loss probability
      if (decision(config.pcp)):          # decidion to send it corrupted or not based on corruption probability
        conn.sendall(packet.encode())
        print ('Sent #', seq_no)
      else:
        conn.sendall(packet.encode(True))
        print('Corrupted #', seq_no)
    else:
      print('Lost #', seq_no)
  except Exception as e :
    print(e)
    
def sr_sw(conn, file, window_size, config):  # method that handles both stop and wait and selective repeat
  timeout = config.timeout
  window_base = 0
  packet_num = 0
  timer_dict = {}
  packet_dict = {}
  ack_dict = {}
  while True:
    if packet_num >= window_base and packet_num < window_base + window_size:  # check if packet within window range
      piece = file.read(config.data_size)     # read a part of file to be encoded in packet
      if piece == "".encode():
        if check_acks(ack_dict):               # if file is all read and all acknowlegment recieved break
          break # end of file
      else:
        packet = Packet(piece, packet_num)     # if file isnt ended create a packer and send it
        send_packet(packet, packet_num, conn, config)
        packet_dict[packet_num] = packet
        ack_dict[packet_num] = False          # mark ack false as its ot confirmed yet
        timer_dict[packet_num] = time.time() + timeout    # add the timeout for this packet in a dict
        packet_num += 1

    try:
      ack = conn.recv(6)                     # try to recieve a ACk packet
      if ack:
        seq_no = int.from_bytes(ack[0:4], 'big')
        checksum = int.from_bytes(ack[4:], 'big')
        print('Acknowledged #' + str(seq_no))
        ack_dict[seq_no] = True     #mark ackowlegemnt of specific packet number  true
        timer_dict.pop(seq_no)      # remove the timeout time in dict of the specific packet number
        if seq_no == window_base:    # update window base if packet is the first of the window
          packet_dict.pop(seq_no)
          try:
            while ack_dict[window_base]:
              window_base += 1
              print("Window base = ", window_base)
          except KeyError:
            pass        
    except (BlockingIOError, KeyError):
      pass

    for seq_no, timestamp in timer_dict.items():    # check if we reached the timeout of any packet in the dict
      if timestamp < time.time():
        print('Timeout #', seq_no)
        send_packet(packet_dict[seq_no], seq_no, conn, config)   # resend packet
        timer_dict[seq_no] = time.time() + timeout               # readd the timeout time

  print(conn)
  conn.close()

def selective_repeat(conn, file, config):
  sr_sw(conn, file, config.window_size, config)
  

def stop_and_wait(conn, file, config):
  sr_sw(conn, file, 1, config)

def go_back_n(conn, file, config):   # method to handle go back N algorithm
  timeout = config.timeout
  window_base = 0
  window_size = config.window_size
  packet_num = 0
  timer_dict = {}
  packet_dict = {}
  ack_dict = {}
  while True:
    if packet_num >= window_base and packet_num < window_base + window_size: # check if packet within window range
      piece = file.read(config.data_size)   # read part of file to encode
      if piece == "".encode():
        if check_acks(ack_dict):            # if file is all read and all acknowlegment recieved break
          break # end of file
      else:
        packet = Packet(piece, packet_num)        # if file isnt ended create a packer and send it
        send_packet(packet, packet_num, conn, config)
        packet_dict[packet_num] = packet
        ack_dict[packet_num] = False          # mark ack false as its ot confirmed yet
        timer_dict[packet_num] = time.time() + timeout      # add the timeout for this packet in a dict
        packet_num += 1

    try:
      ack = conn.recv(6)                 # try to recieve a ACk packet
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

    for seq_no, timestamp in timer_dict.items():   # when there is a timeout
      if timestamp < time.time():
        while seq_no < window_base + window_size:     # from the window base to the seq_no keep sending all packets
          try:
            print('Timeout #', seq_no)
            send_packet(packet_dict[seq_no], seq_no, conn, config) # packets resend
            timer_dict[seq_no] = time.time() + timeout             # readding timeout
          except KeyError:
            pass
          seq_no += 1
        break

  print(conn)
  conn.close()  
