#!/usr/bin/python
import csv
import glob
from statsmodels.distributions.empirical_distribution import ECDF
import matplotlib.pyplot as plt

# Reads all files with link-1- and link-17- in the name.
# plots the ecdf into one plot
def main():
  link1_data =  format_data(read_files('../802_11a/link-1-channel-*.csv'))
  link17_data = format_data(read_files('../802_11a/link-17-channel-*.csv'))
  plot(link1_data, link17_data)


# Calculates the ecdf here and plots it
def plot(link1, link17):
  x_min = min( min(link1), min(link17) )
  x_max = max( max(link1), max(link17) )
  x_range = range(x_min, x_max)

  f_link1 = ECDF(link1)
  f_link17 = ECDF(link17)

  y_link1 = f_link1(x_range)
  y_link17 = f_link17(x_range)

  plt.step(x_range,y_link1, label='link1')
  plt.step(x_range,y_link17, label='link17')

  plt.axis([x_min, x_max, -0.1, 1.1])

  plt.title('ECDF of Link 1 and 17')
  plt.ylabel('ECDF(RSS)')
  plt.xlabel('RSS[dBm]')
  plt.legend(loc=4)
  plt.show()


# reads the files specified by the glob template string
# and puts them all into one array removing to trailing new line
# and splitting by commas
def read_files( file_path_template ):
  file_paths = glob.glob(file_path_template)

  csv_rows = []
  for file_path in file_paths:
    with open(file_path, 'r') as f:
      csv_rows += f.readlines()

  return map(lambda x: x.rstrip('\n').split(','), csv_rows)


# grabs only  the rss value which is index 4, string to int
def format_data( data_rows ):
  return map(lambda x: int(x[4]) if x[4] is not None else None, data_rows)

main()