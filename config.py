import random

TCP_IP = 'localhost'
TCP_PORT = 50001
window_size = 5
plp = 0.01
timeout = 0.1

def checksum(data):
  sum = 0
  for i in range(len(data)):
    split = int.from_bytes(data[i:i + 2], 'big')
    sum += split
    i += 1
  return sum % pow(2,16)

def decision(p):
  return random.random() < 1 - p
