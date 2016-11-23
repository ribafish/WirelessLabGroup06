#!/usr/bin/python3

import re
import subprocess as sub
import sys, getopt
import matplotlib.pyplot as plt
import glob
from statsmodels.distributions.empirical_distribution import ECDF


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hi:", ["ifile="])
    except getopt.GetoptError:
        print('q3b.py -i <input_folder>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('q3b.py -i <input_folder>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            folder = arg
            print('Input folder is %s' %folder)

    if len(folder) == 0:
        folder = ""
    elif folder[len(folder)-1] != "/":
        folder = folder + "/"

    iperf_paths = glob.glob("%s*.out"%folder)
    iperf_paths.sort()
    plot_throughput(iperf_paths)
    
    tcpdump_paths = glob.glob("%s*.cap"%folder)
    tcpdump_paths.sort()
    plot_rss(tcpdump_paths)

class Scenario(object):
    name = ""
    power = 0
    rate = 0
    data = []

    def __init__(self, power, rate, data):
        self.power = power
        self.rate = rate
        self.name = "%iMbit/s@%idBm"%(rate, power)
        self.data = data

    def min(self):
        return min(self.data)

    def max(self):
        return max(self.data)




def plot_throughput(filepaths):
    if len(filepaths) == 0:
        return -1

    scenarios = []
    mins = []
    maxs = []
    box_datas = []
    box_names = []

    for filepath in filepaths:
        print("reading iperf logfile %s"%filepath)
        lines = [line.rstrip('\n') for line in open(filepath, 'r')]
        name_parts = re.split('\.|\-', filepath.split()[len(filepath.split())-1])
        power = int(name_parts[1])
        rate = int(name_parts[2])
        throughputs = []

        for i in range(len(lines)):
            if i > 6 and i%2==1:
                l = lines[i]
                transfer = float(l.split()[4])  #splits on whitespace
                throughput = transfer/30*8 #/30 to get Mbytes/sec, *8 to get Mbits/sec so we can compare to bandwidth which is set in Mbits/sec
                throughputs.append(throughput)

        s = Scenario(power, rate, throughputs)
        scenarios.append(s)
        mins.append(s.min())
        maxs.append(s.max())

    x_range = range( int(min(mins)), int(max(maxs))+1)

    # Plotting

    plt.figure(figsize=(12, 8))

    for s in scenarios:
        box_datas.append(s.data)
        box_names.append(s.name)
        func = ECDF(s.data)
        y = func(x_range)

        plt.step(x_range, y, label=s.name)


    plt.axis([min(mins), max(maxs), -0.1, 1.1])
    plt.title("ECDF of throughput")
    plt.ylabel("ECDF")
    plt.xlabel("Throughput [Mbit/sec]")
    plt.legend(loc=4)
    plt.grid(True)
    plt.savefig("throughput_ECDF.png")
    plt.close()

    fig = plt.figure(1, figsize=(12, 8))
    plt.title("Throughput Boxplots")
    ax = fig.add_subplot(111)
    ax.boxplot(box_datas, 1)
    ax.set_xticklabels(box_names)
    plt.ylabel("Throughput [Mbit/s]")
    plt.grid(True)
    plt.savefig("throughput_box.png")
    plt.close()


def plot_rss(filepaths):
    if len(filepaths) == 0:
        return -1

    scenarios = []
    mins = []
    maxs = []
    box_datas = []
    box_names = []

    for filepath in filepaths:
        tcpdump_call = ('tcpdump -l -K -n -r %s src 172.17.5.11' % filepath).split(" ")
        lines = sub.check_output(tcpdump_call, universal_newlines=True).split('\n')
        name_parts = re.split('\.|\-', filepath.split()[len(filepath.split()) - 1])
        power = int(name_parts[1])
        rate = int(name_parts[2])
        rssis = []
        for l in lines:
            try:
                rssdb = next(x for x in l.split(" ") if "dB" in x)  # this finds and returns the first dB value
                rss = int(rssdb[:len(rssdb)-2])                     # this parses the "dB" out and leaves the int
                rssis.append(rss)
            except StopIteration:
                None

        s = Scenario(power, rate, rssis)
        scenarios.append(s)
        mins.append(s.min())
        maxs.append(s.max())

    x_range = range( min(mins), max(maxs))

    # Plotting

    plt.figure(figsize=(12, 9))

    for s in scenarios:
        box_datas.append(s.data)
        box_names.append(s.name)
        func = ECDF(s.data)
        y = func(x_range)

        plt.step(x_range, y, label=s.name)

    plt.axis([min(mins), max(maxs), -0.1, 1.1])
    plt.title("ECDF of RSSs")
    plt.ylabel("ECDF")
    plt.xlabel("RSS [dB]")
    plt.legend(loc=4)
    plt.grid(True)
    plt.savefig("rss_ECDF.png")
    plt.close()

    fig = plt.figure(1, figsize=(12, 8))
    plt.title("RSS Boxplots")
    ax = fig.add_subplot(111)
    ax.boxplot(box_datas, 1)
    ax.set_xticklabels(box_names)
    plt.ylabel("RSS")
    plt.grid(True)
    plt.savefig("rss_box.png")
    plt.close()











if __name__ == '__main__':
    main(sys.argv[1:])