import json
 # this config file is just a general file to handle various parameters used in all files
algorithms = ['SR', 'GBN', 'S&W']  # our 3 types of algorithms
algorithm = algorithms[0]          # selective repeat chosen in this run

files = [                  # files to be transfered
   'السيف القاطع.mp3',
   'pirates_of_the_caribbean_theme.mp3',
   'Fullmetal Alchemist - Brotherhood OP 3 [720p] [English sub]_-gY4kmxphBU_youtube.mp3',
   'Fullmetal Alchemist - Brotherhood OP 2 [720p] [English sub]_cpRV6jFIvqQ_youtube.mp3',
   'Alesso - Heroes (We Could Be) feat. Tove Lo (Official Audio-Lyrics Video).mp3',
   'AWAKEN.mp3'
]

data_size = 512 #Data size in packet (bytes)
TCP_IP = 'localhost'
TCP_PORT = 30000
window_size = 10
plp = 0.01    # packet loss percentage
pcp = 0.01    # packet corruption percentage
timeout = 0.1 # Time till packet is deemed timeout if ack is not received

def to_str(): # Converts config file into a JSON string so it can be sent to different processes
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