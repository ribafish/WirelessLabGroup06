from datetime import datetime
import subprocess as sp
import glob

TRACES_FOLDER = "traces/"

def main():
  trace_file_paths = glob.glob(TRACES_FOLDER + "trace_*.cap")

  #debug
  trace_file_paths = [trace_file_paths[0]]

  filenames = map(lambda fn: fn.split("/")[-1], trace_file_paths)
  meta = map(trace_filename_to_meta, filenames)
  meta = sorted(meta, key=lambda x: x['ts'])

  traces_with_meta = map(read_trace_with_meta, meta)
  print traces_with_meta


def read_trace_with_meta(meta):
  return {
    'throughput': get_tshark_throughput_in_mbps(TRACES_FOLDER + meta["trace_filename"], meta["proto"]),
    'meta': meta,
  }


def get_tshark_throughput_in_mbps(file_path, proto):
  # call to be executed
  tshark_call = ["tshark", "-nr", file_path, "-z", "conv," + proto, "-q"]

  # call tcpdump and save output
  statistics_string = sp.check_output(tshark_call)

  # keep only the line with the stats and split them by n number of consecutive
  # whitespaces, where n > 0
  stats_line = statistics_string.split("\n")[5].split()

  transmitted_bytes = float(stats_line[6])
  duration_in_s = float(stats_line[-1])

  ## return throughput
  return (transmitted_bytes / duration_in_s) / 1000 / 1000

def trace_filename_to_meta(filename):
  splits = filename.split(".")[0].split("_")
  return {
    'proto': splits[1],
    'transmission_rate': splits[2],
    'ts': datetime.fromtimestamp(int((splits[3]))),
    'trace_filename': filename,
  }

main()