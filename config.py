import random

algorithms = ['SR', 'GBN', 'S&W']
algorithm = algorithms[1]

files = ['13. Push buttons.mp3']

TCP_IP = 'localhost'
TCP_PORT = 50000
#Client_address = ('',)
window_size = 500
plp = 0.1
pcp = 0.1
timeout = 0.1

def checksum(data):
  s = 0
  for i in range(len(data)):
    w = int.from_bytes(data[i:i + 2], 'big')
    s = s + w
    s = (s>>16) + (s & 0xffff);
    s = s + (s>>16);
    i += 1
  s = ~s & 0xffff
  return s

def decision(p):
  return random.random() < 1 - p
