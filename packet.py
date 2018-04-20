class Packet:

  def __init__(self, data, seq_no):
    self.data = data
    self.seq_no = seq_no
    self.length = len(data)
    self.checksum = self.compute_checksum()

  def __str__(self):
    return 'Packet #' + str(self.seq_no)

  def compute_checksum(self):
    sum = 0
    for i in range(len(self.data)):
      split = int.from_bytes(self.data[i:i + 2], 'big')
      sum += split
      i += 1
    return sum % pow(2,16)

  def encode(self, corrupt):
    length_encoded = self.int_to_bytes(self.length, 2)
    checksum_encoded = self.int_to_bytes(self.checksum, 2)
    seq_no_encoded = self.int_to_bytes(self.seq_no, 4)
    data = "".encode() if corrupt else self.data
    return length_encoded + seq_no_encoded + checksum_encoded + data

  def int_to_bytes(self, n, size):
    return n.to_bytes(size, 'big')


class Ack_Packet:

  def __init__(self, checksum, seq_no):
    self.checksum = checksum
    self.seq_no = seq_no

  def encode(self):
    checksum_encoded = self.int_to_bytes(self.checksum, 2)
    seq_no_encoded = self.int_to_bytes(self.seq_no, 4)
    return  seq_no_encoded + checksum_encoded

  def int_to_bytes(self, n, size):
    return n.to_bytes(size, 'big')