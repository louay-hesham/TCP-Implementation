import json

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

data_size = 2048
TCP_IP = 'localhost'
TCP_PORT = 35000
window_size = 10
plp = 0
pcp = 0
timeout = 0.1

def to_str():
  return json.dumps({
    'algorithm': algorithm,
    'files': files,
    'TCP_IP': TCP_IP,
    'TCP_PORT': TCP_PORT,
    'window_size': window_size,
    'plp': plp,
    'pcp': pcp,
    'timeout': timeout,
    'data_size': data_size
  })