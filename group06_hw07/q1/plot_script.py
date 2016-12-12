import glob
import re
from datetime import datetime
import subprocess as sp
from math import ceil
import matplotlib.pyplot as plt


def main():
  iperf_file_paths = glob.glob("data/iperf-*.out")
  trace_file_paths = glob.glob("data/trace-*.cap")
  
  boxplot(iperf_file_paths)
  #barplot(trace_file_paths)


def boxplot(iperf_file_paths):
  iperf_data_sets = []
  for file_path in iperf_file_paths:
    iperf_data_sets.append({
        'data': parse_iperf_data(read_file(file_path)),
        'info': extract_info_from_file_path(file_path)
    })
  plot_boxplot_sets(iperf_data_sets)

def barplot(trace_file_paths):
  trace_data_sets = []
  for file_path in trace_file_paths:
    trace_data_sets.append({
        'data': parse_tcpdump_data(read_tcpdump_file(file_path)),
        'info': extract_info_from_file_path(file_path)
    })
  plot_barplot_sets(trace_data_sets)

def plot_barplot_sets(data_sets):
  bar_width = 0.75


  fig, axes = plt.subplots(int(ceil(len(data_sets)/2.0)),2)

  for data_set_i in range(0, len(data_sets)):
    data = data_sets[data_set_i]['data']
    info = data_sets[data_set_i]['info']
    keys_num_sorted = sorted(data, key=lambda key: float(key))
    bar_num = len(keys_num_sorted)

    values = []
    count_sum = float(reduce(lambda x,y: x + y, data.values()))

    for key in keys_num_sorted:
      values.append((data[key] / count_sum) * 100)

    axis = axes[data_set_i / 2, data_set_i % 2]

    axis.bar(range(0, bar_num), values, bar_width)
    axis.set_xticks(map(lambda x: x + bar_width/2,range(0, bar_num)))
    axis.set_xticklabels(keys_num_sorted)
    axis.set_title("CH %s, TX PWR %s, ANT %s" % (info['channel'], info['txpower'], info['antenna']))
    axis.set_ylabel('Frame count in %')
    axis.set_xlabel('Transmission Rates in Mb/s')
  
  plt.show()


def plot_boxplot_sets(data_sets):
  labels = []
  data = []

  for data_set in data_sets:
    data.append(data_set['data'])
    labels.append("CH %s\n TX PWR: %s\n ANT: %s" % (
      data_set['info']['channel'],
      data_set['info']['txpower'],
      data_set['info']['antenna']
    ))

  plt.boxplot(data, notch=True, labels=labels)
  plt.title('Minstrel Performance based on txpower and antenna')
  plt.ylabel('Throughput [Mbps]')
  plt.show()


def read_tcpdump_file(file_path):
  # call to be executed
  tcpdump_call = ["tcpdump", "-r", file_path, "udp and src 172.17.5.11 and dst 172.17.5.10"]

  # call tcpdump and save output
  tcp_out = sp.check_output(tcpdump_call)

  # remove new line char within frame captures
  lines = tcp_out.split("\n")

  return filter(lambda line: not line.startswith(' '), lines)

def parse_tcpdump_data(file_contents):
  data_rates = {}

  for line in file_contents:
    # sometimes short and preamble sneak in before the datarate. remove em!
    partials = filter(lambda x: x not in ["short", "preamble"], line.split(" "))[0:5]

    # identifies a frame that doesnt hold our type of information
    if len(partials) < 5: continue 

    # make sure we got the right field. fail otherwise
    if partials[4] != "Mb/s": raise ValueError("Expected Mb/s as unit. got ", partials[4])

    key = partials[3]
    if key not in data_rates:
      data_rates[key] = 0

    data_rates[key] += 1

  return data_rates




# extract meta information from the file path name
def extract_info_from_file_path(file_path):
  file_name_partials = ( 
    file_path
      .split('/')[-1] # remove other paths only taking the filename
      .split(".")[0] # remove file name appendix
      .split("-")[1:] # remove prefix
  )

  return {
    'channel': int(file_name_partials[0].lstrip("ch")),
    'txpower': int(file_name_partials[1].rstrip("dbm")),
    'antenna': int(file_name_partials[2].lstrip("ant")),
    'timestamp': datetime.fromtimestamp(int(file_name_partials[3]))
  }



# reads file. each line -> one list item
def read_file(file_path):
  with open(file_path, 'r') as file:
     read_data = file.readlines()
     return read_data



# parses the lists items and returns only the transfered kbytes per sec
# array has 10 items. if some are missing it fills them
def parse_iperf_data(file_content):
  results = filter(lambda line: 'bits/sec' in line,file_content)

  reg = re.compile(r"(\d+\.){0,1}\d+ (KBytes|MBytes|Bytes)")
  results_mapped = map(lambda x: re.search(reg, x).group(0), results)
  del results

  results_normalized = map(lambda x: parse_iperf_line_and_convert_to_mbps(x),results_mapped)
  del results_mapped

  # append 0 if missing items
  for i in range(len(results_normalized), 10):
    results_normalized.append(0.0)
  
  return results_normalized



# extracts the number and normalizes the values according to 
# the unit. all values are now mbits/s
def parse_iperf_line_and_convert_to_mbps(result):
  value, unit = result.split(' ')
  value = float(value)

  if unit in 'MBytes':
    return value * 8 / 30

  if unit in 'KBytes':
    return value * 8 * 1000 / 30

  if unit in 'Bytes':
    return value * 8 * 10**6 / 30

  raise ValueError('Result string must have an unit of MBytes, KBytes or Bytes got', unit)



main()