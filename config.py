import random

algorithms = ['SR', 'GBN', 'S&W']
algorithm = algorithms[1]

files = ['shark.jpg','Mewtwo.jpg', '13. Push buttons.mp3']

TCP_IP = 'localhost'
TCP_PORT = 50001
#Client_address = ('',)
window_size = 10
plp = 0.2
pcp = 0.2
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
