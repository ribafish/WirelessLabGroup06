import parse_spectrum_file_ht20
import matplotlib.pyplot as plt
import heatmap
import math
import gc
import sys


# entrypoint
def main():

  # parsed samples
  samples = parse_spectrum_file_ht20.parse_file('../data/spectral_scan_wlan1_2.data')
  noise_floor = samples[0].noise
  
  # mapped samples to more usable format
  samples_mapped = map_samples(samples)

  # clean up
  del samples; gc.collect()

  # mins and max across all captures (2.4 and 5ghz)
  min_y = math.floor(
    reduce(lambda x, y: min(x, y['signal']), samples_mapped, sys.float_info.max)
  )

  max_y = math.ceil(
    reduce(lambda x, y: max(x, y['signal']), samples_mapped, -200)
  )

  # heatmap width and height
  discret_x = 50
  discret_y = 80

  samples_2ghz, samples_5ghz = split_samples(samples_mapped, 3000)

  maps = [
    create_heatmap(samples_2ghz, min_y, max_y, discret_x, discret_y),
    create_heatmap(samples_5ghz, min_y, max_y, discret_x, discret_y)
  ]  

  plot_data(maps, min_y, max_y, noise_floor)


# creates the heatmaps and adds the samples
def create_heatmap(samples, min_y, max_y, discret_x, discret_y):
  map = heatmap.HeatMap(discret_x, discret_y)

  min_x = math.floor(
    reduce(lambda x, y: min(x, y['freq']), samples, sys.float_info.max)
  )

  max_x = math.ceil(
    reduce(lambda x, y: max(x, y['freq']), samples, 0)
  )

  x_range = max_x - min_x
  y_range = max_y - min_y
  
  for sample in samples:
    x_i = int(round((sample['freq'] - min_x) * (discret_x / x_range))) - 1
    y_i = int(round( (sample['signal'] - min_y) * (discret_y / y_range))) -1
    map.heat_pixel_at(x_i, y_i)

  return (map, min_x, max_x)

# split the samples in 2.4ghz and 5ghz with a splitter value
def split_samples(samples, splitter):
  return (
    filter(lambda x: x['freq'] <= splitter, samples),
    filter(lambda x: x['freq'] > splitter, samples)
  )

# plots the heatmap
def plot_data(heatmaps, min_y, max_y, noise_floor):

  heatmap2ghz = heatmaps[0][0]
  axis2ghz = [heatmaps[0][1], heatmaps[0][2], min_y, max_y]
  heatmap5ghz = heatmaps[1][0]
  axis5ghz = [heatmaps[1][1], heatmaps[1][2], min_y, max_y]

  plt.figure(figsize = (20,8))

  ratio1 = (heatmaps[0][2] - heatmaps[0][1]) / (max_y - min_y) 
  ratio2 = (heatmaps[1][2] - heatmaps[1][1]) / (max_y - min_y)


  plt.subplot(121)
  plt.title('Scan over 2.4GHz')
  plt.imshow(heatmap2ghz.img_data(), interpolation='nearest', extent=axis2ghz, aspect=ratio1)
  plt.axhline(y=noise_floor, linewidth=2, color='w')
  plt.ylabel('RSSI (-dBm)')
  plt.xlabel('Frequency (MHz)')

  plt.subplot(122)
  plt.title('Scan over 5GHz')
  plt.imshow(heatmap5ghz.img_data(), interpolation='nearest', extent=axis5ghz, aspect=ratio2)
  plt.axhline(y=noise_floor, linewidth=2, color='w')
  plt.ylabel('RSSI (-dBm)')
  plt.xlabel('Frequency (MHz)')


  plt.show()


# maps the samples 
# see https://github.com/simonwunderlich/FFT_eval/blob/master/fft_eval.c
def map_samples(samples):
  samples_mapped = []
  for sample in samples:
    # calc data square sum
    data_square_sum = 0
    for i in range(0, 56):
      data_tmp = (sample.data[i] << sample.max_exp) ** 2
      data_square_sum += data_tmp


    for i in range(0, 56):
      freq = sample.freq - (22.0 * 56 / 64.0) / 2 + (22.0 * (i +0.5) / 64.0)
      raw_data = sample.data[i] << sample.max_exp
      raw_data = raw_data if raw_data != 0 else 1
      data_square_sum = data_square_sum if data_square_sum != 0 else 1

      signal = sample.noise + sample.rssi + 20.0 * math.log10(raw_data) - math.log10(data_square_sum) * 10

      samples_mapped.append({'freq': freq, 'signal': signal})

  return samples_mapped


main()