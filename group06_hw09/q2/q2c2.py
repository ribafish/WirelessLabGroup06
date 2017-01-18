#!/usr/bin/python3


import subprocess as sub
import sys, getopt
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import time

def main(argv):
    tcpfile = ""
    tcptime = 0
    udpfile = ""
    udptime = 0

    try:
        opts, args = getopt.getopt(argv, "ht:u:", ["tcpfile=", "udpfile="])
    except getopt.GetoptError:
        print('q2c2.py -t <input_tcp> -u <input_udp>')
        sys.exit(2)
    for opt, arg in opts:
        print (opt, arg)
        if opt == '-h':
            print('q2c2.py -t <input_tcp> -u <input_udp>')
            sys.exit()
        elif opt in ("-t", "--tcpfile"):
            tcpfile = arg
            tcptime = int(arg.split("/")[-1].split("_")[-1].split(".")[0])
            tcpspeed = arg.split("/")[-1].split("_")[2]
        elif opt in ("-u", "--udpfile"):
            udpfile = arg
            udptime = int(arg.split("/")[-1].split("_")[-1].split(".")[0])
            udpspeed = arg.split("/")[-1].split("_")[2]

    if (len(tcpfile) == 0):
        raise Exception("TCP file not specified")
    elif (len(udpfile) == 0):
        raise Exception("UDP file not specified")

    times_tcp, seqnums_tcp = process_tcp_file(tcpfile)
    date_tcp = time.strftime('%Y-%m-%d %H:%M', time.localtime(tcptime))
    times_udp, seqnums_udp = process_udp_file(udpfile)
    date_udp = time.strftime('%Y-%m-%d %H:%M', time.localtime(udptime))

    # print("last 2 UDP seqnums: %i, %i" %(seqnums_udp[-2], seqnums_udp[-1]))

    plt.figure(figsize=(16, 10))

    fig, ax1 = plt.subplots()
    ax1.set_ylabel("TCP Packet sequence number (relative)")
    tcp, = ax1.plot(times_tcp, seqnums_tcp, label="TCP %s @ %s" % (tcpspeed, date_tcp))
    ax1.tick_params('y', colors='b')
    ax1.set_xlabel("Delta Time from first packet [s]")

    ax2 = ax1.twinx()
    udp, = ax2.plot(times_udp, seqnums_udp, label="UDP %s @ %s" % (udpspeed, date_udp), color='r')
    ax2.set_ylabel("UDP Packet \"sequence number\"")
    ax2.tick_params('y', colors='r')
    ax2.yaxis.get_major_formatter().set_powerlimits((0, 2))

    plt.title("TCP/UDP packet sequence numbers vs. time")
    plt.grid(True)
    plt.legend(handles=[tcp, udp], loc="best")
    plt.savefig("tcp_udp_seqnums.png")


def process_tcp_file(filepath):
    tcpdump_call = ("tcpdump -ttttt -r %s ip src 172.17.5.11" % filepath).split(" ")

    lines = sub.check_output(tcpdump_call, universal_newlines=True).split('\n')
    if len(lines) == 0:
        raise Exception("No data in tcpdump trace: %s"%filepath)

    times = []
    seqnums = []

    for i in range(1, len(lines)-1):
        try:
            line = lines[i]
            sline = line.split(" ")
            ts = line.split(" ")[0].split(":")
            time = float(ts[1])*60 + float(ts[2])
            seqi = sline.index("seq")
            seqnum = int(sline[seqi+1].replace(",", ":").split(":")[0])
            times.append(time)
            seqnums.append(seqnum)
        except ValueError:
            None
        except:
            raise Exception("Error on TCP line %i: %s" % (i, lines[i]))

    return times, seqnums


def process_udp_file(filepath):
    tcpdump_call = ("tshark -Y ip.src==172.17.5.11 -r %s "
                    "-T fields -e frame.time_relative -e data.data" % filepath).split(" ")

    lines = sub.check_output(tcpdump_call, universal_newlines=True).split('\n')
    if len(lines) == 0:
        raise Exception("No data in tcpdump trace: %s" % filepath)

    times = []
    seqnums = []

    for i in range(1, len(lines)-1):
        try:
            data = lines[i].split("\t")[1].split(":")
            time = float(lines[i].split("\t")[0])
            seqstr = data[0]+data[1]+data[2]+data[3]
            seqnum = int(seqstr, 16)
            times.append(time)
            seqnums.append(seqnum)
        except:
            # raise Exception("Error on UDP line %i: %s" % (i, lines[i]))
            print("Error on UDP line %i: %s" % (i, lines[i]))
            None


    return times, seqnums


if __name__ == '__main__':
    main(sys.argv[1:])