class Packet:

  def __init__(self, data, seq_no):
    self.data = data
    self.seq_no = seq_no
    self.length = len(data)
    self.checksum = self.compute_checksum()

  def __str__(self):
    return 'Packet #' + str(self.seq_no) + "\nData: " + self.data

  def compute_checksum(self):
    return 0

  def encode(self):
    length_encoded = self.int_to_bytes(self.length, 2)
    checksum_encoded = self.int_to_bytes(self.checksum, 2)
    seq_no_encoded = self.int_to_bytes(self.seq_no, 4)
    return length_encoded + seq_no_encoded + checksum_encoded + self.data.encode()

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