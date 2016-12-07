#!/usr/bin/python3

import subprocess as sub
import sys, getopt
import matplotlib.pyplot as plt
import time

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
    times_manual, cus_manual = get_cu_from_trace_manually(tcpdump)

    date = time.strftime('%Y-%m-%d %H:%M', time.localtime(times_BSS[0]))

    plt.figure(figsize=(12, 8))
    plt.title("Channel utilization on %s"%date)
    plt.xlabel("Time [s]")
    plt.ylabel("Channel Utilization [%]")
    plt.plot(times_BSS, cus_BSS, label="BSS Load")
    plt.plot(times_survey, cus_survey, label="Survey dump")
    plt.plot(times_manual, cus_manual, label="Calculated from tcpdump")
    plt.grid(True)
    plt.legend(loc="best")
    plt.savefig("utilizations.png")

    plot_bar_utilization_by_type(tcpdump)




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
    tcpdump_call = ("tshark -r %s -T fields -e frame.time_epoch -e frame.len -e radiotap.datarate -e radiotap.length -e frame.protocols -e udp.length"
                    # " -c 1000" % filepath).split(" ")   # TODO: add a -c 1000 here if needed for quick tests
                    "" % filepath).split(" ")  # TODO: add a -c 1000 here if needed for quick tests
    lines = sub.check_output(tcpdump_call, universal_newlines=True).split('\n')
    if len(lines) == 0:
        raise Exception("No usable lines in %s" % filepath)

    t_phy_overhead = 20 # 20us = preamble + phy header
    t_ofdm = 4
    utilizations = []
    times = []
    cur_time = int(lines[0].split()[0].split('.')[0])
    time_consumed = 0
    for i in range(0, len(lines) - 1):  # -1 because last line is empty
        try:
            # for each frame in trace
            time = int(lines[i].split()[0].split('.')[0])  # Epoch time
            total_len = int(lines[i].split()[1])    # Total capture len in bytes
            datarate = float(lines[i].split()[2].replace(',', '.'))     # datarate from Radiotap header
            radiotap_len = int(lines[i].split()[3]) # Radiotap header size to be subtracted from total frame len as its transmitted at a different bitrate
            protocols = lines[i].split()[4].split(":") # get all protocols that the frame uses

            rate = datarate*1024*1024/8.0/1000000.0 # get the datarate in Bytes per us

            transmit_time = t_phy_overhead + t_ofdm + (total_len-radiotap_len) / rate

            if "udp" in protocols:
                ack = t_phy_overhead + t_ofdm + (42) / rate    # 42 B = 28 B for mac header + 14 B for ack size
                transmit_time += ack

            if (time == cur_time):
                time_consumed += transmit_time
            else:
                percentage = time_consumed / 1000000.0  # how much time [us] we used in each second
                utilizations.append(percentage * 100)  # Get percent Channel Utilization value (mean/255*100)
                times.append(cur_time)
                cur_time = time
                time_consumed = transmit_time
        except:
            print("Error in line: %s"%lines[i])
            raise

    percentage = time_consumed / 1000000.0  # how much time [us] we used in each second
    utilizations.append(percentage * 100)  # Get percent Channel Utilization value (mean/255*100)
    times.append(cur_time)
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

def plot_bar_utilization_by_type(filepath):
    tcpdump_call = (
    "tshark -r %s -T fields -e frame.time_epoch -e frame.len -e radiotap.datarate -e radiotap.length -e frame.protocols -e udp.length"
    # " -c 1000" % filepath).split(" ")   # TODO: add a -c 1000 here if needed for quick tests
    "" % filepath).split(" ")  # TODO: add a -c 1000 here if needed for quick tests
    lines = sub.check_output(tcpdump_call, universal_newlines=True).split('\n')
    if len(lines) == 0:
        raise Exception("No usable lines in %s" % filepath)

    t_phy_overhead = 20  # 20us = preamble + phy header
    t_ofdm = 4
    first_udp_epoch = 0.0
    last_udp_epoch = 0.0
    udp_time = 0
    non_udp_in_udp_timeframe = 0
    non_udp = 0
    for i in range(0, len(lines) - 1):  # -1 because last line is empty
        try:
            # for each frame in trace
            epoch = float(lines[i].split()[0])  # Epoch time
            total_len = int(lines[i].split()[1])  # Total capture len in bytes
            datarate = float(lines[i].split()[2].replace(',', '.'))  # datarate from Radiotap header
            radiotap_len = int(lines[i].split()[
                                   3])  # Radiotap header size to be subtracted from total frame len as its transmitted at a different bitrate
            protocols = lines[i].split()[4].split(":")  # get all protocols that the frame uses

            rate = datarate * 1024 * 1024 / 8.0 / 1000000.0  # get the datarate in Bytes per us

            transmit_time = t_phy_overhead + t_ofdm + (total_len - radiotap_len) / rate

            if "udp" in protocols:
                if first_udp_epoch == 0: first_udp_epoch = epoch
                last_udp_epoch = epoch

                ack = t_phy_overhead + t_ofdm + (42) / rate  # 42 B = 28 B for mac header + 14 B for ack size
                transmit_time += ack

                non_udp_in_udp_timeframe += non_udp
                non_udp = 0
                udp_time += transmit_time

            else:
                non_udp += transmit_time

        except:
            print("Error in line: %s" % lines[i])
            raise

    timeframe = (last_udp_epoch - first_udp_epoch) * 1000000.0    # Time frame in us
    udp_percent = udp_time / timeframe * 100.0
    other_percent = non_udp_in_udp_timeframe / timeframe * 100.0
    no_traffic_percent = (udp_time + non_udp_in_udp_timeframe) / timeframe * 100.0
    labels = ["UDP", "Other", "No traffic"]
    values  = [udp_percent, other_percent, no_traffic_percent]

    print("First UDP epoch: %f\tLast UDP epoch: %f"%(first_udp_epoch, last_udp_epoch))

    date = time.strftime('%Y-%m-%d %H:%M', time.localtime(first_udp_epoch))
    plt.close()
    plt.figure()
    plt.xlabel("Frame type")
    plt.ylabel("Percentage of time on air [%]")
    plt.title("Channel utilization by frame type on %s" % date)
    plt.bar(range(len(labels)), values, align='center')
    plt.xticks(range(len(labels)), labels)
    plt.savefig("utilization_by_type_while_UDP.png")
    plt.close()
























if __name__ == '__main__':
    main(sys.argv[1:])