from datetime import datetime
import glob

def main():
  trace_file_paths = glob.glob("data/trace-*.cap")

  filenames = map(lambda fn: fn.split("/")[-1].split(".")[0], trace_file_paths)

  meta_data = map(filename_to_meta, filenames)

  meta_data = sorted(meta_data, key=lambda x: x['ts'])

  print "Ordered Overview of capture-time and settings"
  print ("=" * 65)

  for meta in meta_data:
    print "| %20s | ANT: %6s | TXPWR: %5s | CH: %5s |" % (
      meta['ts'].strftime('%H:%M:%S %d.%m.%Y '),
      meta['antenna'],
      meta['txpower'],
      meta['ch'],
    )

  print ("-" * 65)
  print "\n%i captures in total" % len(meta_data)






def filename_to_meta(filename):
  splits = filename.split("-")
  return {
    'ch': splits[1],
    'txpower': splits[2],
    'antenna': splits[3],
    'ts': datetime.fromtimestamp(int((splits[4]))),
  }

main()