import socket, random, math, os, time, json, sys
import traceback
from packet import *
from common_functions import *

def start_client(config_str):    #  this function help initiate a new terminal which
                                 #   the client will run on
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

  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # creating client socket
  s.connect((config.TCP_IP, config.TCP_PORT))           # connecting to server ip and port
  data = s.recv(config.data_size + 8)                   # recieved new server port for this client
  print(data)
  conn_port = int.from_bytes(data[8:], 'big')          # new port to connect to
  print(conn_port)
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((config.TCP_IP, conn_port))                #connect to new server port

  start = time.time()
  file = config.files[int(math.floor(random.random()*len(config.files)))] # randomly choose a file name to be requested
  print('requesting', file)
  packet = Packet(file.encode(), 0)
  s.sendall(packet.encode())          # encoding packet with file name and send it to server

  if config.algorithm == 'SR':   #select desired in from config file if selective repeat
    window_size = config.window_size
  else:                          # if GBN or Stop and wait for the client the window size is 1
    window_size = 1

  window_base = 0              # init position if window
  file_data = bytes([])
  my_dict={}
  prev_seq_num = -1

  while 1:
    data = s.recv(config.data_size + 8)    #recieve packet of data + header
    if not data: break
    # print('Received bytes: ', data)
    length = int.from_bytes(data[0:2], 'big')     # decoding header
    seq_no = int.from_bytes(data[2:6], 'big')
    chcksum = int.from_bytes(data[6:8], 'big')
    string = data[8:]

    if seq_no >= window_base and seq_no < (window_base + window_size): # check if packet num  is within window range
      print('Received #',seq_no)
      if chcksum == checksum(string): # calculating checksum and checking if its the same as the one in the header
        prev_seq_num = seq_no
        if decision(config.plp):    #based on percentage of packet loss we send acknolwegment or no
          p = Ack_Packet(chcksum , seq_no)
          s.sendall(p.encode())
          print('Acknowledged #', seq_no)
        else:
          print ('Ack lost #', seq_no)

        my_dict[seq_no]= string
        if seq_no==window_base:   #updating window base is
          while 1:
            if my_dict.get(window_base)== None:
              break
            else:
              print('window_base', window_base)
              file_data += my_dict[window_base]
              window_base += 1
      else:
        print('#', seq_no, ' is corrupted!')  # if checksum is false then data corrupted
        if config.algorithm == 'GBN':            # only send the last acknoleweged package in GBN algorithm
          try:
            p = Ack_Packet(checksum(my_dict[prev_seq_num]), prev_seq_num)
            print('GBN sending ACk #', prev_seq_num)
            s.sendall(p.encode())
          except:
            pass




    elif seq_no < window_base:  #if packet is recieved before
      if config.algorithm == 'GBN':
        current_sq_num = prev_seq_num
      else:
        current_sq_num = seq_no
      p = Ack_Packet(checksum(my_dict[current_sq_num ]), current_sq_num )
      print('Received already acked #', current_sq_num)
      s.sendall(p.encode())


  out_folder = 'Client_instances/' + str(int(time.time()))   # where we put the recieved file, folder name is the time recieved
  os.makedirs(out_folder)
  print('Received file:', file)
  size = len(file_data);
  print('File size =', size)
  with open(out_folder + "/" + file, "wb") as out_file:
    out_file.write(file_data)

  end = time.time()
  s.close()
  time = end - start         # time for all transfers
  print('Time elapsed:', time)
  throughput = size / time   # calculating throughput
  print('Throughput =', throughput, 'bytes/second')
  input('Press enter to close..')
  return throughput