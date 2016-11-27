#!/usr/bin/python3

import subprocess as sub
import numpy as np
import sys, getopt, re
import matplotlib.pyplot as plt
import glob

def main(argv):
    folder = ""

    try:
        opts, args = getopt.getopt(argv, "hi:", ["ifile="])
    except getopt.GetoptError:
        print('q1.py -i <input_folder>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('q1.py -i <input_folder>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            folder = arg

    if len(folder) == 0:
        folder = ""
    elif folder[len(folder)-1] != "/":
        folder = folder + "/"

    iperf_paths = glob.glob("%s*.out" % folder)
    iperf_paths.sort()
    tcpdump_paths = glob.glob("%s*.cap" % folder)
    tcpdump_paths.sort()

    plot_fdr(tcpdump_paths)
    plot_throughput(iperf_paths)

def plot_fdr(filepaths):
    if len(filepaths) == 0:
        raise IOError("No files found")

    setups_fdrs = []
    box_names = []

    for filepath in filepaths:
        print("Reading tcpdump file: %s"%filepath)

        tcpdump_call = ("tshark -r %s -e wlan.seq -e udp.srcport -T fields -Y ip.src==172.17.5.11" % filepath).split(" ")
        lines = sub.check_output(tcpdump_call, universal_newlines=True).split('\n')
        name_parts = re.split('\.|\/', filepath.split()[len(filepath.split())-1])
        name = name_parts[len(name_parts)-2].replace("-", " ")
        box_names.append(name)

        fdrs = []
        missing_seq_nrs = 0
        for i in range(0, len(lines) - 2):  # -2 because we look at i+1 and the last line is empty
            curr_seq = int(lines[i].split()[0])  # MAC Sequence number [0-4095]
            curr_port = int(lines[i].split()[1])   # UDP port (changes between runs) - needed to get fdr per run from combined dataset

            next_seq = int(lines[i+1].split()[0])  # MAC Sequence number [0-4095]
            next_port = int(lines[i+1].split()[1])

            if curr_port != next_port or i == len(lines) - 3:
                # calculate fdr and add to fdrs
                received_frames = float(len(lines))
                sent_frames = float(missing_seq_nrs + received_frames)
                fdr = received_frames / sent_frames
                fdrs.append(fdr)
                missing_seq_nrs = 0
                print("fdr = %f"%fdr)
            else:
                # if no missing diff should be 1
                # with the bitmask negative values can be avoided
                # and real diffs even if curr is bigger then next
                diff_samples = (next_seq - curr_seq) & 4095

                missing_seq_nrs += abs(diff_samples - 1)    # abs in case its the same value -> frame re-sent

        setups_fdrs.append(fdrs)

    make_boxplot("Frame Delivery Ratios by Experiments", box_names, setups_fdrs, "Experiments", "FDR", "fdrs.png", 'log')
    make_boxplot("Frame Delivery Ratios by Experiments - Zoomed", box_names, setups_fdrs, "Experiments", "FDR", "fdrs_zommed.png", 'log', False)


def make_boxplot(title, box_names, box_datas, xlabel, ylabel, filename = None, yscale = None, showfliers = None):
    fig = plt.figure(1, figsize=(12, 8))
    plt.title(title)
    ax = fig.add_subplot(111)
    if showfliers is None:
        ax.boxplot(box_datas, 1)
    else:
        ax.boxplot(box_datas, 1, showfliers=showfliers)
    ax.set_xticklabels(box_names)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.grid(True)
    if filename is None:
        plt.show()
    else:
        plt.savefig(filename)
    if yscale is not None:
        plt.yscale(yscale)
    plt.close()


def plot_throughput(filepaths):
    if len(filepaths) == 0:
        return -1

    box_datas = []
    box_names = []

    for filepath in filepaths:
        print("reading iperf logfile %s"%filepath)
        lines = [line.rstrip('\n') for line in open(filepath, 'r')]
        name_parts = re.split('\.|\_', filepath.split()[len(filepath.split()) - 1])
        name = name_parts[len(name_parts) - 2].replace("-", " ")

        throughputs = []

        for i in range(len(lines)):
            if i > 6 and i%2==1 and len(lines[i]) > 0:
                l = lines[i]
                try:
                    transfer = float(l.split()[4])  #splits on whitespace
                except:
                    print(l)
                    raise
                throughput = transfer/30*8 #/30 to get Mbytes/sec, *8 to get Mbits/sec so we can compare to bandwidth which is set in Mbits/sec
                throughputs.append(throughput)

        box_datas.append(throughputs)
        box_names.append(name)

    make_boxplot("UDP Throughputs by Experiment", box_names, box_datas, "Experiment", "Throughput [Mbit/sec]", "throughputs.png", 'log')
    make_boxplot("UDP Throughputs by Experiment - Zoomed", box_names, box_datas, "Experiment", "Throughput [Mbit/sec]", "throughputs_zoomed.png", 'log', False)





if __name__ == '__main__':
    main(sys.argv[1:])