import glob
import re
import matplotlib.pyplot as plt

def main():
  file_paths = glob.glob("../data/iperf*.out")
  data_sets = []

  for file_path in file_paths:
    data_sets.append({
        'data': parse_data(read_file(file_path)),
        'info': extract_info_from_file_path(file_path)
    })

  # print data_sets
  plot_data_sets(data_sets)

def plot_data_sets(data_sets):
  labels = []
  data = []

  for data_set in data_sets:
    data.append(data_set['data'])
    labels.append("UDP Size %s B, TH: %s" % (data_set['info']['udp_size'], data_set['info']['threshold']))

  plt.boxplot(data, notch=True, labels=labels)
  plt.title('CTS/RTS Threshold vs Frame Size')
  plt.ylabel('Throughput [Mbps]')
  plt.show()


# parses the lists items and returns only the transfered kbytes per sec
# array has 10 items. if some are missing it fills them
def parse_data(file_content):
  results = filter(lambda line: 'bits/sec' in line,file_content)

  reg = re.compile(r"(\d+\.){0,1}\d+ (KBytes|MBytes|Bytes)")
  results_mapped = map(lambda x: re.search(reg, x).group(0), results)
  del results

  results_normalized = map(lambda x: parse_and_convert_to_mbps(x),results_mapped)
  del results_mapped

  # append 0 if missing items
  for i in range(len(results_normalized), 10):
    results_normalized.append(0.0)
  
  return results_normalized

# extracts the number and normalizes the values according to 
# the unit. all values are now kbits/s
def parse_and_convert_to_mbps(result):
  value, unit = result.split(' ')
  value = float(value)

  if unit in 'MBytes':
    return value * 8 / 30

  if unit in 'KBytes':
    return value * 8 / 1000 / 30

  if unit in 'Bytes':
    return value / 10**6 * 8 / 30

  raise ValueError('Result string must have an unit of MBytes, KBytes or Bytes got', unit)


# extract meta information from the file path name
def extract_info_from_file_path(file_path):
  file_name_partials = file_path.split('/')[-1].rstrip('.out').split('-')

  return {
    'threshold': file_name_partials[4],
    'udp_size': file_name_partials[2]
  }

# reads file. each line -> one list item
def read_file(file_path):
  with open(file_path, 'r') as file:
     read_data = file.readlines()
     return read_data

main()
