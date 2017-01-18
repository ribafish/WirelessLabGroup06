from datetime import datetime
import glob

def main():
  trace_file_paths = glob.glob("traces/trace_*.cap")
  
  filenames = map(lambda fn: fn.split("/")[-1].split(".")[0], trace_file_paths)

  meta_data = map(filename_to_meta, filenames)

  meta_data = sorted(meta_data, key=lambda x: x['ts'])

  

  print "Ordered Overview of capture-time and settings"
  print ("=" * 55)

  for meta in meta_data:
    print "| %20s | PROTO: %3s | TX RATE: %6s |" % (
      meta['ts'].strftime('%H:%M:%S %d.%m.%Y '),
      meta['proto'],
      meta['transmission_rate'],
    )

  print ("-" * 55)
  print "\n%i captures in total" % len(meta_data)




def filename_to_meta(filename):
  splits = filename.split("_")
  return {
    'proto': splits[1],
    'transmission_rate': splits[2],
    'ts': datetime.fromtimestamp(int((splits[3]))),
  }

main()