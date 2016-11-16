import matplotlib.pyplot as plt
import csv
import glob

def main():
    # plot_rss()
    plot_delivery_rates()

def plot_delivery_rates():
    links = []
    channels = []
    rates = []

    with open("../task_b/aggregated_data_ts_filtered.csv", newline="\n") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            try:
                link = int(row[2])
                channel = int(row[3])
                rate = float(row[0])

                links.append(link)
                channels.append(channel)
                rates.append(rate)
            except Exception:
                pass

    plt.title("Link vs Delivery ratio")
    plt.xlabel("Link")
    plt.ylabel("Delivery ratio")
    plt.scatter(links, rates)
    plt.xticks(links)

    plt.show()

    plt.close()

    plt.title("Channel vs Delivery ratio")
    plt.xlabel("Channel")
    plt.ylabel("Delivery ratio")
    plt.scatter(channels, rates)
    plt.xticks(channels)
    plt.show()




def get_ratios_from_file(file):
    link = 0
    channel = 0
    ratios = []

    with open(file, newline="\n") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            try:
                data.rss.append(int(row[4]))
            except Exception:
                pass

    csvfile.close()
    # print(data.rss)
    return link, channel, ratios

def plot_rss():
    file_paths = glob.glob("../802_11a/link-*-channel-*.csv")
    links_rss = {}
    channels_rss = {}

    for path in file_paths:
        link, channel, rss = get_rss_from_file(path)

        if link not in links_rss:
            links_rss[link] = set()

        if channel not in channels_rss:
            channels_rss[channel] = set()

        links_rss[link].update(rss)
        channels_rss[channel].update(rss)

    links_plotx = []
    links_ploty = []
    for k, v in links_rss.items():
        for rss in v:
            links_plotx.append(k)
            links_ploty.append(rss)
    plt.title("Link vs RSS")
    plt.xlabel("Link")
    plt.ylabel("RSS")
    plt.scatter(links_plotx, links_ploty)
    plt.xticks(links_plotx)

    plt.show()

    plt.close()

    plotx = []
    ploty = []
    for k, v in channels_rss.items():
        for rss in v:
            plotx.append(k)
            ploty.append(rss)
    plt.title("Channel vs RSS")
    plt.xlabel("Channel")
    plt.ylabel("RSS")
    plt.scatter(plotx, ploty)
    plt.xticks(plotx)
    plt.show()



def get_rss_from_file(file):
    filesplit = file.replace("-", ".").split(".")
    link = int(filesplit[3])
    channel =  int(filesplit[5])

    rss = []

    with open(file, newline="\n") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            try:
                rss.append(int(row[4]))
            except Exception:
                pass

    csvfile.close()
    return link, channel, rss



if __name__ == '__main__':
    main()