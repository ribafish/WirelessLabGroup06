#!/usr/bin/python

import glob
import re
import csv

def main(): 

  # objects that holds the dataset csv files
  file_paths = glob.glob("../802_11a/link-*-channel-*.csv")

  # array that hold the agg data for each link and channel
  agg_data = []

  for file_path in file_paths:
    prog = re.compile(r"-\d{1,3}")
    link, channel = map(lambda find_string: int(find_string.lstrip('-')),prog.findall(file_path))

    data_hash = {
      'link': link,
      'channel': channel      
    }
    data_hash.update( process_file(file_path) )

    agg_data.append(data_hash)

  write_to_csv(agg_data)

  
  
def write_to_csv( data_rows ):
  fieldnames = data_rows[0].keys()
  with open('./aggregated_data.csv', 'wb') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for data_row in data_rows:
      writer.writerow(data_row)


# processes one file. it calculates the median of rss values
# and the delivery rate.
# format: comma seperated values
# col1: ts
# col2: "Data"
# col3: channel
# col4: SNR
# col5: RSS
# col6: noise floor
# col7: data rate (static 6.0)
# col8: MAC sequence number (0-4095)
def process_file( file_path ):
  # get rows and map only rss and mac sequence nr
  # assumption: dataset is sorted by timestamp
  file_filtered = filter_data_rows( read_file(file_path) )
  data_rows = map(lambda x: map_data_row(x) ,file_filtered)

  return {
    'delivery_rate': calculate_delivery_rate(data_rows),
    'rss_median': calculate_median(data_rows)
  }
  
# filter buggs timestamps
# see discussion:
# https://isis.tu-berlin.de/mod/forum/discuss.php?d=112736#p227141
def filter_data_rows( file_read ):
  rows = map(lambda x: x.rstrip('\n').split(','), file_read)
  #return filter(lambda x: int(x[0]) > 1230768000, rows)
  return rows


# helper function see process_file
def map_data_row( row ):
  return { 'rss' : int(row[4]), 'seq' : int(row[7]) }


def calculate_delivery_rate( data ):
  missing_seq_nrs = 0
  for i in range(0, len(data)-1):
    curr_seq = data[i]['seq']
    next_seq = data[i+1]['seq']

    # if no missing diff should be 1
    # with the bitmask negative values can be avoided
    # and real diffs even if curr is bigger then
    # next
    diff_samples = (next_seq - curr_seq) & 4095

    # 1 is the desired diff, everything above are missing packets
    missing_seq_nrs += diff_samples - 1

  received_frames = float(len(data))
  sent_frames = float(missing_seq_nrs + received_frames)
  return None if sent_frames == 0 else received_frames / sent_frames

def calculate_median( data ):
  rss_values = map(lambda x: x['rss'], data)
  rss_values.sort()

  n = len(data)
  if n < 1:
    return None

  # array length is odd
  if ((n & 0b1) == 1):
    # return always float
    return float(data[ ((n+1) / 2) - 1 ]['rss'])
  # array length is even
  else:
    return ( data[ ( n / 2 ) - 1 ]['rss'] + data[ (n / 2 + 1) - 1 ]['rss'] ) / 2.0
  


# reads lines into array
def read_file( file_path ):
  f = open(file_path, 'r')
  lines = f.readlines()
  f.close()
  return lines



main()