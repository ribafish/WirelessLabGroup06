import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import csv
import glob



def main():
    file_paths = glob.glob("../802_11a/link-*-channel-*.csv")
    rsss = []

    for path in file_paths:
        rsss.append(get_rss_from_file(path))
    

























class Combination(object):
    name = ""
    link = 0
    channel = 0
    rss = []

    def __init__(self, link, channel):
        self.link = link
        self.channel = channel
        self.name = "Link %i Channel %i" % (link, channel)
        self.rss = []


def get_rss_from_file(file):
    filesplit = file.replace("-", ".").split(".")

    data = Combination(int(filesplit[3]), int(filesplit[5]))
    data.rss.clear()

    with open(file, newline="\n") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            try:
                data.rss.append(int(row[4]))
            except Exception:
                pass

    csvfile.close()
    # print(data.rss)
    return data



if __name__ == '__main__':
    main()