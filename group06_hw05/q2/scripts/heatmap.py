import sys
import copy
import colorsys

# Represents one pixel within the heatmap
class HeatPixel:
  def __init__(self, weight):
    self.weight = float(weight)

  def color(self):
    r, g, b = colorsys.hsv_to_rgb( 0.66 - (self.weight ), 1.0, 1.0)
    return [r, g, b]

  def __str__(self):
    return "%+4.2f" % self.weight

  def heat(self):
    self.weight += 1

# matrix of the image for the heatmap
class HeatMap:

  def init_map(self, width, height):
    data = []
    for x in range(0, self.width):
      data.append([])
      for y in range(0, self.height):
        data[x].append( HeatPixel(0) )
    return data

  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.map = self.init_map(width, height)

  def __str__(self):
    out = 'Heatmap: \n'
    for y in range(0, self.height):
      out += "| "
      for x in range(0, self.width):
        out += "%s | " % self.map[x][y].__str__()
      out += '\n'
    return out

  # increase signal detect
  def heat_pixel_at(self, x, y):
    self.map[x][y].heat()

  # normalize the data to 0.0 - 1.0
  def normalize(self):
    map = copy.deepcopy(self.map)
    lowest_value = sys.float_info.max
    greatest_value = sys.float_info.min
    for x in range(0, self.width):
      for y in range(0, self.height):
        lowest_value = min(lowest_value, map[x][y].weight)
        greatest_value = max(greatest_value, map[x][y].weight)

    # shift min value to 0
    greatest_diff = greatest_value - lowest_value
    for x in range(0, self.width):
      for y in range(0, self.height):
        map[x][y].weight = (map[x][y].weight - lowest_value) / greatest_diff

    return map

  # normalizes the data, adds color arrays and flips axis
  def img_data(self):
    normalized_map = self.normalize()
    flipped_map = []
    for x in range(0, self.width):
      for y in range(0, self.height):
        if len(flipped_map) <= y:
          flipped_map.append([])
        flipped_map[y].append( normalized_map[x][y].color())

    return flipped_map


  

