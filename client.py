import socket, random, math, os, time, json, sys
import traceback
from packet import *
from common_functions import *

def start_client(config_str):
  try:
    config_dict = json.loads(config_str)
    config_obj = type('Dummy', (object,), config_dict)
    client(config_obj)
  except Exception as e:
    print(e)
    print(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2])
    print(traceback.format_exc())
    input('')

def client(config):
  import time 

  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((config.TCP_IP, config.TCP_PORT))
  data = s.recv(264)
  print(data)
  conn_port = int.from_bytes(data[8:], 'big')
  print(conn_port)
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((config.TCP_IP, conn_port))

  start = time.time()
  file = config.files[int(math.floor(random.random()*len(config.files)))]
  print('requesting', file)
  packet = Packet(file.encode(), 0)
  s.sendall(packet.encode())

  if config.algorithm == 'SR':
    window_size = config.window_size
  else:
    window_size = 1

  window_base = 0
  file_data = bytes([])
  my_dict={}
  prev_seq_num = -1

  while 1:
    data = s.recv(264)
    if not data: break
    # print('Received bytes: ', data)
    length = int.from_bytes(data[0:2], 'big')
    seq_no = int.from_bytes(data[2:6], 'big')
    chcksum = int.from_bytes(data[6:8], 'big')
    string = data[8:]

    if seq_no >= window_base and seq_no < (window_base + window_size):
      print('Received #',seq_no)
      if chcksum == checksum(string):
        prev_seq_num = seq_no
        if decision(config.plp):
          p = Ack_Packet(chcksum , seq_no)
          s.sendall(p.encode())
          print('Acknowledged #', seq_no)
        else:
          print ('Ack lost #', seq_no)

        my_dict[seq_no]= string
        if seq_no==window_base:
          while 1:
            if my_dict.get(window_base)== None:
              break
            else:
              print('window_base', window_base)
              file_data += my_dict[window_base]
              window_base += 1
      else:
        print('#', seq_no, ' is corrupted!')
        if config.algorithm == 'GBN':
          try:
            p = Ack_Packet(checksum(my_dict[prev_seq_num]), prev_seq_num)
            print('GBN sending ACk #', prev_seq_num)
            s.sendall(p.encode())
          except:
            pass




    elif seq_no < window_base:
      if config.algorithm == 'GBN':
        current_sq_num = prev_seq_num
      else:
        current_sq_num = seq_no
      p = Ack_Packet(checksum(my_dict[current_sq_num ]), current_sq_num )
      print('Received already acked #', current_sq_num)
      s.sendall(p.encode())


  out_folder = 'Client_instances/' + str(int(time.time()))
  os.makedirs(out_folder)
  print('Received file:', file)
  size = len(file_data);
  print('File size =', size)
  with open(out_folder + "/" + file, "wb") as out_file:
    out_file.write(file_data)

  end = time.time()
  s.close()
  time = end - start
  print('Time elapsed:', time)
  throughput = size / time
  print('Throughput =', throughput, 'bytes/second')
  input('Press enter to close..')
  return throughput