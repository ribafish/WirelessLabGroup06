from datetime import datetime
import subprocess as sp
import glob
import matplotlib.pyplot as plt

TRACES_FOLDER = "traces/"

def main():
  trace_file_paths = glob.glob(TRACES_FOLDER + "trace_*.cap")

  #debug
  #trace_file_paths = trace_file_paths[0:1]

  filenames = map(lambda fn: fn.split("/")[-1], trace_file_paths)
  meta = map(trace_filename_to_meta, filenames)
  meta = sorted(meta, key=lambda x: x['ts'])

  traces_with_meta = filter(lambda x: x['throughput'] is not None, map(read_trace_with_meta, meta))
  grouped_sorted_traces = group_and_sort_traces(traces_with_meta)

  boxplot(grouped_sorted_traces)


def boxplot(data_sets):
  labels = []
  data = []

  for data_set in data_sets:
    data.append(data_set['throughputs'])
    labels.append("Protocol: %s\n TX Rate: %s" % (
      data_set['meta']['proto'].upper(),
      data_set['meta']['transmission_rate'].upper()
    ))

  plt.boxplot(data, notch=True, labels=labels)
  plt.title('Protocol and Transmission Rate vs Throughput')
  plt.ylabel('Throughput [Mb/s]')
  plt.show()

def group_and_sort_traces(traces):
  grouped_traces_dict = {}
  for trace in traces:
    group_key = trace['meta']['transmission_rate'] + trace['meta']['proto']
    if group_key in grouped_traces_dict.keys():
      grouped_traces_dict[group_key]['throughputs'].append(trace['throughput'])
    else:
      grouped_traces_dict[group_key] = {
        'throughputs': [trace['throughput']],
        'meta': {
          'transmission_rate': trace['meta']['transmission_rate'],
          'proto': trace['meta']['proto']
        }
      }
  return sorted(
    grouped_traces_dict.values(), key=lambda x: (x['meta']['proto'], int(x['meta']['transmission_rate'].rstrip('mbps')))
  )



def read_trace_with_meta(meta):
  return {
    'throughput': get_tshark_throughput_in_mbps(TRACES_FOLDER + meta["trace_filename"], meta["proto"]),
    'meta': meta,
  }


def get_tshark_throughput_in_mbps(file_path, proto):
  # call to be executed
  tshark_call = ["tshark", "-nr", file_path, "-z", "conv," + proto, "-q"]

  # call tcpdump and save output
  try:
    statistics_string = sp.check_output(tshark_call)
  except sp.CalledProcessError as e:
    print 'could not process file ' + file_path
    return None

  # keep only the line with the stats and split them by n number of consecutive
  # whitespaces, where n > 0
  stats_line = statistics_string.split("\n")[5].split()

  if len(stats_line) < 7:
    print stats_line
    return None

  transmitted_bytes = float(stats_line[6])
  transmitted_frames = int(stats_line[5])

  #calculate the overhead by a given protocol
  if proto == 'tcp':
    overhead = transmitted_frames * 128
  else:
    overhead = transmitted_frames * 104

  duration_in_s = float(stats_line[-1])

  ## return throughput
  return ((transmitted_bytes - overhead )/ duration_in_s) / 1000 / 1000

def trace_filename_to_meta(filename):
  splits = filename.split(".")[0].split("_")
  return {
    'proto': splits[1],
    'transmission_rate': splits[2],
    'ts': datetime.fromtimestamp(int((splits[3]))),
    'trace_filename': filename,
  }

main()