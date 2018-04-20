TCP_IP = 'localhost'
TCP_PORT = 50001
window_size = 5


def checksum(data):
  sum = 0
  for i in range(len(data)):
    split = int.from_bytes(data[i:i + 2], 'big')
    sum += split
    i += 1
  return sum
