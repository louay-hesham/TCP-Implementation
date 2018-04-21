import random

algorithms = ['SR', 'GBN', 'S&W']
algorithm = algorithms[2]

TCP_IP = 'localhost'
TCP_PORT = 5000
window_size = 10
plp = 0.1
pcp = 0.1
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
