#!/usr/bin/python

import csv
import matplotlib.pyplot as plt


def main():
  data_rows = read_csv('./aggregated_data.csv')
  plot(data_rows)


def plot( data_rows ):
  # filter rows that dont have delivery rate or rss_median and count
  data_rows_filtered = filter(lambda x: x['rss_median'] is not None and x['delivery_rate'] is not None, data_rows)

  x_values = map(lambda x: x['delivery_rate'],data_rows_filtered)
  y_values = map(lambda x: x['rss_median'],data_rows_filtered)
  

  x_int = max(x_values) - min(x_values)
  y_int = max(y_values) - min(y_values)

  print "%i link - channel combination ignored because there was no data" % (len(data_rows) - len(data_rows_filtered))

  plt.title('RSS vs FDR')
  plt.ylabel('RSS Median [dBm]')
  plt.xlabel('FDR')
  plt.axis([ 
    min(x_values) - x_int * 0.1, 
    max(x_values) + x_int * 0.1, 
    min(y_values) - y_int * 0.1, 
    max(y_values) + y_int * 0.1 
  ])
  plt.plot(x_values, y_values, 'ro')
  plt.show()

  

def read_csv( file_path ):
  data_rows = []
  with open(file_path, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      data_rows.append(row)
  return map(lambda x: format_row(x), data_rows)


def format_row( data_row ):
  link_value = data_row['link']
  channel_value = data_row['channel']
  rss_median_value = data_row['rss_median']
  delivery_rate_value = data_row['delivery_rate']

  return {
    'link': int(link_value),
    'channel': int(channel_value),
    'rss_median': None if not rss_median_value else float(rss_median_value),
    'delivery_rate': None if not delivery_rate_value else float(delivery_rate_value)
  }


main()