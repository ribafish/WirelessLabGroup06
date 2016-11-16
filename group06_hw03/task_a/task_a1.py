import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import csv

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


def main():
    rsss = []

    rsss.append(get_rss_from_file("../802_11a/link-5-channel-36.csv"))
    rsss.append(get_rss_from_file("../802_11a/link-5-channel-64.csv"))
    rsss.append(get_rss_from_file("../802_11a/link-5-channel-165.csv"))

    rsss.append(get_rss_from_file("../802_11a/link-14-channel-36.csv"))
    rsss.append(get_rss_from_file("../802_11a/link-14-channel-64.csv"))
    rsss.append(get_rss_from_file("../802_11a/link-14-channel-165.csv"))

    rsss.append(get_rss_from_file("../802_11a/link-35-channel-36.csv"))
    rsss.append(get_rss_from_file("../802_11a/link-35-channel-64.csv"))
    rsss.append(get_rss_from_file("../802_11a/link-35-channel-165.csv"))

    data_to_plot=[]
    box_names = []

    for c in rsss:
        # print(c.name)
        # print(c.rss)
        plot_hist(c)
        plot_moving_avg(c)
        data_to_plot.append(c.rss)
        box_names.append(c.name)

    plt.close()
    plt.title("Boxplots")
    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    ax.boxplot(data_to_plot, 1)
    ax.set_xticklabels(box_names)
    plt.xticks(rotation=45)
    plt.ylabel("RSS")
    plt.show()







def plot_hist(combination):
    plt.close()
    plt.title(combination.name)
    # plt.hist(combination.rss, bins=range(-100, -50, 1))
    plt.hist(combination.rss, bins=20)
    # plt.axis([-90, -60, 0, 7000])
    plt.xlabel("RSS")
    plt.grid(True)
    plt.axvline(median(combination.rss), color='r', linestyle='dashed', linewidth=2, label = "Median")
    low, high = medianCI(combination.rss, 0.95)
    plt.axvline(low, color='g', linestyle='dotted', linewidth=2, label = "Median low CI")
    plt.axvline(high, color='y', linestyle='dashdot', linewidth=2, label = "Median high CI")
    plt.legend()
    plt.savefig("hist-l%ic%i.png" % (combination.link, combination.channel))


def median(raw):
    data = np.sort(raw)
    x = 0.0
    if len(data) % 2 == 1:
        x = data[int(len(data)/2)]
    else:
        x = ( data[int(len(data)/2)] + data[int(len(data)/2 + 1)] )/2.0
    # print("median = %.2f" % x)
    return x


def medianCI(data, ci):

    data = np.sort(data)
    lowCount, upCount = stats.binom.interval(ci, len(data), 0.5)

    return data[int(lowCount)], data[int(upCount)]


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

def plot_moving_avg(combination):
    plt.close()
    plt.title("RSS Moving average (16) " + combination.name)
    plt.xlabel("RSS")
    plt.plot(sma(combination.rss, 16), label="SMA")
    plt.savefig("sma-l%ic%i.png" % (combination.link, combination.channel))

def sma(data, n):
    val = []
    for i in range(0, len(data)-n+1):
        x = 0
        for j in range(0, n):
            x += data[i+j]
        val.append(x/n)
    return val




if __name__ == '__main__':
    main()