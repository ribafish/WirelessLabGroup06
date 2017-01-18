#!/usr/bin/python3


import subprocess as sub
import sys, getopt
import matplotlib.pyplot as plt
import glob
import time


def main(argv):
    files = []

    try:
        opts, args = getopt.getopt(argv, "hi:", ["ifolder="])
    except getopt.GetoptError:
        print('q2c2.py -t <input_tcp> -u <input_udp>')
        sys.exit(2)
    for opt, arg in opts:
        print (opt, arg)
        if opt == '-h':
            print('q2c2.py -t <input_tcp> -u <input_udp>')
            sys.exit()
        elif opt in ("-i", "--ifolder"):
            folder = arg

    if len(folder) == 0:
        folder = ""
    elif folder[len(folder) - 1] != "/":
        folder = folder + "/"

    paths = glob.glob("%s*.cap" % folder)
    paths.sort()
    files.append(get_first_path(paths, "tcp", "6"))
    files.append(get_first_path(paths, "tcp", "24"))
    files.append(get_first_path(paths, "tcp", "54"))
    files.append(get_first_path(paths, "udp", "6"))
    files.append(get_first_path(paths, "udp", "24"))
    files.append(get_first_path(paths, "udp", "54"))


    #plt.figure(figsize=(25, 15))

    fig, ax1 = plt.subplots(figsize=(12, 10))
    ax1.set_ylabel("TCP Packet number of packets")
    x,y = process_tcp_file(files[0])
    tcp1, = ax1.plot(x, y, label="TCP %s @ %s" % scrape_speed_date(files[0]), color='b')
    x,y = process_tcp_file(files[1])
    tcp2, = ax1.plot(x, y, label="TCP %s @ %s" % scrape_speed_date(files[1]), color='g')
    x,y = process_tcp_file(files[2])
    tcp3, = ax1.plot(x, y, label="TCP %s @ %s" % scrape_speed_date(files[2]), color='r')
    ax1.set_xlabel("Delta Time from first packet [s]")
    ax1.yaxis.get_major_formatter().set_powerlimits((0, 2))

    ax2 = ax1.twinx()
    x, y = process_udp_file(files[3])
    udp1, = ax2.plot(x, y, label="UDP %s @ %s" % scrape_speed_date(files[3]), color='c')
    x, y = process_udp_file(files[4])
    udp2, = ax2.plot(x, y, label="UDP %s @ %s" % scrape_speed_date(files[4]), color='m')
    x, y = process_udp_file(files[5])
    udp3, = ax2.plot(x, y, label="UDP %s @ %s" % scrape_speed_date(files[5]), color='y')
    ax2.set_ylabel("UDP Packet \"sequence number\"")
    ax2.yaxis.get_major_formatter().set_powerlimits((0, 2))

    plt.title("TCP/UDP packet sequence numbers vs. time")
    #plt.grid(True)
    plt.legend(handles=[tcp1, tcp2, tcp3, udp1, udp2, udp3], loc="best")
    plt.savefig("tcp_udp_packetnums.png")

def get_first_path(paths, tcpudp, speed):
    for path in paths:
        if path.find(tcpudp) != -1 and path.find(speed+"mbps") != -1:
            return path
    raise Exception("Cant find a %s file with %smbps" % (tcpudp, speed))

def scrape_speed_date(filepath):
    date = time.strftime('%Y-%m-%d %H:%M', time.localtime(int(filepath.split("/")[-1].split("_")[-1].split(".")[0])))
    speed = filepath.split("/")[-1].split("_")[2]
    return speed, date

def process_tcp_file(filepath):
    tcpdump_call = ("tcpdump -ttttt -r %s ip src 172.17.5.11" % filepath).split(" ")

    lines = sub.check_output(tcpdump_call, universal_newlines=True).split('\n')
    if len(lines) == 0:
        raise Exception("No data in tcpdump trace: %s"%filepath)

    times = []
    seqnums = []
    dif = []

    for i in range(3, len(lines)-1):    # Jump over the handshake
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

    correct_seqs = []
    correct_seqs.append(0)
    for i in range(1, len(seqnums)):
        if seqnums[i] > seqnums[i-1]:
            correct_seqs.append(correct_seqs[-1]+1)
            dif.append(1)
        else:
            correct_seqs.append(correct_seqs[-1])
            dif.append(0)

    print("Average difference between seqnums of packets: %f" % (sum(dif)/float(len(dif))))
    return times, correct_seqs


def process_udp_file(filepath):
    print("Reading from file %s" % filepath)
    tcpdump_call = ("tshark -Y ip.src==172.17.5.11 -r %s "
                    "-T fields -e frame.time_relative -e data.data" % filepath).split(" ")

    lines = sub.check_output(tcpdump_call, universal_newlines=True).split('\n')
    if len(lines) == 0:
        raise Exception("No data in tcpdump trace: %s" % filepath)

    times = []
    seqnums = []
    dif = []

    for i in range(1, len(lines)-1):
        try:
            data = lines[i].split("\t")[1].split(":")
            time = float(lines[i].split("\t")[0])
            seqstr = data[0]+data[1]+data[2]+data[3]
            seqnum = int(seqstr, 16)
            times.append(time)
            if len(seqnums) > 1:
                dif.append(seqnum - seqnums[-1])
            seqnums.append(seqnum)
        except:
            # raise Exception("Error on UDP line %i: %s" % (i, lines[i]))
            print("Error on UDP line %i: %s" % (i, lines[i]))
            None

    print("Average difference between seqnums of packets: %f" % (sum(dif)/float(len(dif))))
    return times, seqnums


if __name__ == '__main__':
    main(sys.argv[1:])