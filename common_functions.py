import random

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