import socket
from packet import Packet

window_size = 5
window_base = 0

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 50001))
s.listen(1)
conn, addr = s.accept()
print('Connection established.')

with open("server_files/shark.jpg", "rb") as file:
  packet_num = 0
  # timer_dict = {}
  packet_dict = {}
  ack_dict = {}
  while True:
    if packet_num >= window_base and packet_num < window_base + window_size:
      piece = file.read(512)
      if piece == "".encode():
        break # end of file 
      packet = Packet(piece, packet_num)
      conn.sendall(packet.encode())
      print('Sending #' + str(packet_num))
      packet_dict[packet_num] = packet
      ack_dict[packet_num] = False
      # Start timer here
      packet_num +=1

    ack = conn.recv(10)
    if ack:
      seq_no = int.from_bytes(ack[0:4], 'big')
      checksum = int.from_bytes(ack[4:], 'big')
      print('Acknowledged #' + str(seq_no))
      ack_dict[seq_no] = True
      # Stop timer
      if seq_no == window_base:
        packet_dict.pop(seq_no)
        try:
          while ack_dict[window_base]:
            window_base += 1
            print("Window base = " + str(window_base))
        except KeyError:
          continue

    # Check timer here

  conn.close()
