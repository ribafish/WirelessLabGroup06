#!/usr/bin/python3

import subprocess as sub
import numpy as np
import sys, getopt, re
import matplotlib.pyplot as plt
import glob

def main(argv):
    folder = ""

    try:
        opts, args = getopt.getopt(argv, "hi:r:", ["ifile=", "read="])
    except getopt.GetoptError:
        print('q1.py -i <input_tcpdump> -r <survey_dump_file>')
        sys.exit(2)
    for opt, arg in opts:
        print (opt, arg)
        if opt == '-h':
            print('q1.py -i <input_folder>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            tcpdump = arg
        elif opt in ("-r", "--read"):
            survey = arg

    times_BSS, cus_BSS = get_cu_from_BSS(tcpdump)
    times_survey, cus_survey = get_cu_from_survey_dumps(survey)

    plt.figure(figsize=(12, 8))
    plt.title("Channel utilization")
    plt.xlabel("Time [s]")
    plt.ylabel("Channel Utilization [%]")
    plt.plot(times_BSS, cus_BSS, label="BSS Load")
    plt.plot(times_survey, cus_survey, label="Survey dump")
    plt.legend(loc="best")
    plt.savefig("utilizations.png")




def get_cu_from_BSS(filepath):

    tcpdump_call = ("tshark -r %s -T fields -e frame.time_epoch -e wlan_mgt.qbss.cu "
                    "-Y (((wlan.fc.type_subtype==0x0008)&&(wlan_mgt.tag.number==11))&&(wlan_mgt.qbss.cu>0))&&(radiotap.channel.freq==2462)"
                    # " -c 1000" % filepath).split(" ")   # TODO: add a -c 1000 here if needed for quick tests
                    "" % filepath).split(" ")  # TODO: add a -c 1000 here if needed for quick tests
    lines = sub.check_output(tcpdump_call, universal_newlines=True).split('\n')
    if len(lines) == 0:
        raise Exception("No usable lines for Channel Utilization from BSS in %s"%filepath)

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
            if (len(cus) > 0):
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

def get_cu_from_trace_manually(filepath):
    utilizations = []
    times = []


    return times, utilizations

def get_cu_from_survey_dumps(filepath):
    lines = [line.rstrip('\n') for line in open(filepath, 'r')]

    utilizations = []
    times = []
    cur_time = lines[0]
    cus = []
    last_busy = int(lines[4].split()[3])
    last_active = int(lines[5].split()[3])
    for i in range(1, int(len(lines)/8)):
        ii = i*8

        time = int(lines[ii])
        active = int(lines[ii+4].split()[3]) - last_active
        busy = int(lines[ii+5].split()[3]) - last_busy
        cu = busy/(float(active))*100   # get percent

        if time == cur_time:
            cus.append(cu)
        else:
            if (len(cus) > 0):
                utilizations.append(sum(cus) / float(len(cus)))
                times.append(cur_time)
            cur_time = time
            cus.clear()
            cus.append(cu)

        last_busy += busy
        last_active += active

    utilizations.append(sum(cus) / float(len(cus)))
    times.append(cur_time)
    return times, utilizations






















if __name__ == '__main__':
    main(sys.argv[1:])