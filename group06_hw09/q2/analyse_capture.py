from datetime import datetime
import glob

def main():
  trace_file_paths = glob.glob("traces/trace_*.cap")
  experiment_log = "hw09.log"
  # filenames = map(lambda fn: fn.split("/")[-1], trace_file_paths)
  # traces_with_meta = map(trace_filename_to_meta, filenames)
  # meta_data = sorted(meta_data, key=lambda x: x['ts'])

  




def trace_filename_to_meta(filename):
  splits = filename.split(".")[0].split("_")
  return {
    'proto': splits[1],
    'transmission_rate': splits[2],
    'ts': datetime.fromtimestamp(int((splits[3]))),
    'trace_filename': filename,
  }

main()