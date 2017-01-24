#!/usr/bin/python3

import glob
import matplotlib.pyplot as plt
import sys, getopt
import re


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hi:", ["ifolder="])
    except getopt.GetoptError:
        print('q2c2.py -i <input folder>')
        sys.exit(2)
    for opt, arg in opts:
        print (opt, arg)
        if opt == '-h':
            print('q2c2.py -i <input folder>')
            sys.exit()
        elif opt in ("-i", "--ifolder"):
            folder = arg

    if len(folder) == 0:
        folder = ""
    elif folder[len(folder) - 1] != "/":
        folder = folder + "/"

    udp_file_paths = glob.glob("%siperf_server_UDP*.log" % folder)
    udp_file_paths.sort(key=natural_keys)
    udp_data = []
    udp_names = []

    for file_path in udp_file_paths:
        udp_data.append(get_UDP_data(file_path))
        udp_names.append(get_UDP_info(file_path))

    plt.boxplot(udp_data, notch=True, labels=udp_names)
    plt.title("Throughput vs. UDP packet size")
    plt.ylabel("Throughput [Mbps]")
    plt.grid(True)
    plt.savefig("udp_packet_lengths.png")
    plt.close()

    tcp_file_paths = glob.glob("%siperf_server_TCP*.log" % folder)
    tcp_data = []
    tcp_names = []

    for file_path in tcp_file_paths:
        tcp_data.append(get_TCP_data(file_path))
        tcp_names.append(get_TCP_info(file_path))

    plt.boxplot(tcp_data, notch=True, labels=tcp_names)
    plt.title("Throughput vs. TCP algorithms")
    plt.ylabel("Throughput [Mbps]")
    plt.grid(True)
    plt.savefig("tcp_algos.png")

    # plot data_sets

def get_TCP_data(path):
    with open(path, 'r') as file:
        lines = file.readlines()

    throughputs = []

    for line in lines:
        if line.split()[0] == '[SUM]':
            throughputs.append(float(line.split()[5]))

    return throughputs


def get_TCP_info(file_path):
    file_name_partials = file_path.split('/')[-1].split('.')[0].split('_')

    algo = file_name_partials[-1]   # get the algorithm

    return algo

def get_UDP_data(path):
    with open(path, 'r') as file:
        lines = file.readlines()

    throughputs = []

    next = False
    for line in lines:
        if next:
            throughputs.append(float(line.split()[6]))
        if line.split()[0] == '[' and line.split()[1] == 'ID]':
            next = True
        else:
            next = False

    return throughputs


def get_UDP_info(file_path):
    file_name_partials = file_path.split('/')[-1].split('.')[0].split('_')

    size = file_name_partials[-1]   # get packet size

    return size

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split('(\d+)', text) ]


if __name__ == '__main__':
    main(sys.argv[1:])