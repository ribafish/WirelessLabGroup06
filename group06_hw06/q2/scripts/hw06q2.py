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
        print('q1.py -i <input_tcpdump> -r <survey_dump_file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('q1.py -i <input_folder>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            tcpdump = arg
        elif opt in ("-r", "--read"):
            survey = arg

    times_BSS, cus_BSS = get_cu_from_BSS(tcpdump)



    plt.title("Channel utilization")
    plt.xlabel("Time [s]")
    plt.ylabel("Channel Utilization [%]")
    plt.plot(times_BSS, cus_BSS, label="BSS Load")
    plt.legend(loc="best")
    plt.savefig("../utilizations.png")




def get_cu_from_BSS(filepath):

    tcpdump_call = ("tshark -r %s -T fields -e frame.time_epoch -e wlan_mgt.qbss.cu "
                    "-Y (((wlan.fc.type_subtype==0x0008)&&(wlan_mgt.tag.number==11))&&(wlan_mgt.qbss.cu>0))&&(radiotap.channel.freq==2462)"
                    "" % filepath).split(" ")   # TODO: add a -c 1000 here if needed for quick tests
    lines = sub.check_output(tcpdump_call, universal_newlines=True).split('\n')

    utilizations = []
    times = []
    cur_time = int(lines[0].split()[0].split('.')[0])
    cus = []
    for i in range(0, len(lines) - 1):  # -1 because last line is empty
        time = int(lines[i].split()[0].split('.')[0])  # Epoch time
        cu = int(lines[i].split()[1])   # Channel Utilization

        if (time == cur_time):
            cus.append(cu)
        else:
            utilizations.append((sum(cus) / float(len(cus)))/ 2.55)    # Get percent Channel Utilization value (mean/255*100)
            times.append(cur_time)
            cur_time = time
            cus.clear()
            cus.append(cu)
    utilizations.append((sum(cus) / float(len(cus))) / 2.55)  # Get percent Channel Utilization value
    times.append(cur_time)
    # print(times)
    # print(utilizations)
    return times, utilizations



















if __name__ == '__main__':
    main(sys.argv[1:])