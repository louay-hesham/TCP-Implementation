import random

algorithms = ['SR', 'GBN', 'S&W']
algorithm = algorithms[0]

files = [ 
  '13. Push buttons.mp3',
  # '_150_mewtwo__sfm__by_kensukenl-d8tcj4z.png',
  # 'gadwal 1.png',
  # 'gadwal 2.png',
  # 'Legendary-Pokemon-Wallpaper.jpg',
  # 'Mewtwo.jpg',
  # 'mewtwo-wallpaper-1920x1080.jpg',
  # 'new wallpaper.jpg',
  # 'Screenshot from 2018-02-12 23-39-06.png',
  # 'Screenshot from 2018-05-01 11-36-22.png',
  # 'shark.jpg',
  # 'soso.png',
  # 'wp-image-142649597.jpg'
]

TCP_IP = 'localhost'
TCP_PORT = 20000
#Client_address = ('',)
window_size = 100
plp = 0
pcp = 0
timeout = 0.2

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
