# parses a spectrum output from ath9k cards
import struct

samples = []

class FFT_sample_ht20:

  def __init__(self):
    self.length        = None    # int16
    self.max_exp       = None    # unit8
    self.freq          = None    # int16
    self.rssi          = None    # int8
    self.noise         = None    # int8
    self.max_magnitude = None    # uint16
    self.max_index     = None    # uint8
    self.bitmap_weight = None    # uint8
    self.tsf           = None    # uint64
    self.data          = []      # uint8


def parse_sample(binary_data, offset):
  new_sample = FFT_sample_ht20()

  p_read = offset
  read_format = ''

  read_format = '>B'
  sample_type = struct.unpack_from(read_format, binary_data, p_read)[0]
  p_read += struct.calcsize(read_format)

  if sample_type is not 1:
    raise StandardError("Only supporting sample type 1 (HT20_20")


  read_format = '>h'
  new_sample.length = struct.unpack_from(read_format, binary_data, p_read)[0]
  p_read += struct.calcsize(read_format)

  read_format = '>B'
  new_sample.max_exp = struct.unpack_from(read_format, binary_data, p_read)[0]
  p_read += struct.calcsize(read_format)

  read_format = '>h'
  new_sample.freq = struct.unpack_from(read_format, binary_data, p_read)[0]
  p_read += struct.calcsize(read_format)

  read_format = '>b'
  new_sample.rssi = struct.unpack_from(read_format, binary_data, p_read)[0]
  p_read += struct.calcsize(read_format)

  read_format = '>b'
  new_sample.noise = struct.unpack_from(read_format, binary_data, p_read)[0]
  p_read += struct.calcsize(read_format)

  read_format = '>H'
  new_sample.max_magnitude = struct.unpack_from(read_format, binary_data, p_read)[0]
  p_read += struct.calcsize(read_format)

  read_format = '>B'
  new_sample.max_index = struct.unpack_from(read_format, binary_data, p_read)[0]
  p_read += struct.calcsize(read_format)

  read_format = '>B'
  new_sample.bitmap_weight = struct.unpack_from(read_format, binary_data, p_read)[0]
  p_read += struct.calcsize(read_format)

  read_format = '>Q'
  new_sample.tsf = struct.unpack_from(read_format, binary_data, p_read)[0]
  p_read += struct.calcsize(read_format)

  read_format = '>B'
  while p_read < (offset + new_sample.length + 3):
    new_sample.data.append(
      struct.unpack_from(read_format, binary_data, p_read)[0]
    )
    p_read += struct.calcsize(read_format)

  return new_sample


def parse_file(file_path):

  file_content = read_file(file_path)
  samples = []

  pos = 0

  while pos < len(file_content):
    curr_sample = parse_sample(file_content, pos)
    samples.append(curr_sample)
    pos += curr_sample.length + 3 # type + length + payload

  return samples

def read_file(file_path):
  with open(file_path, 'r') as data_file:
    return data_file.read()