import glob
import matplotlib.pyplot as plt



def main():
  iperf_file_paths = glob.glob("iperf-logs/iperf_client_TCP_reno_*bss*.log")
  iperf_outputs = map(lambda x: read_file(x), iperf_file_paths)
  iperf_data_sets = map(lambda x: extract_throughput(x), iperf_outputs)
  plot_data_sets = merge_sets(iperf_data_sets)
  plot_data(plot_data_sets, ["IBSS", "BSS"])


def plot_data(data_sets, labels):
  plt.boxplot(data_sets, notch=True, labels=labels)
  plt.title("IBSS vs BSS Throughput")
  plt.ylabel("Throughput [Mbps]")
  plt.grid(True)
  plt.savefig("ibss_vs_bss.png")
  plt.close()

def merge_sets(data_sets):
  ibss_set = []
  bss_set = []

  for data_set in data_sets:
    if data_set["network_type"] == "bss":
      bss_set += data_set["throughputs"]
    if data_set["network_type"] == "ibss":
      ibss_set += data_set["throughputs"]

  return [ibss_set, bss_set]


def extract_throughput(iperf_output):
  sum_lines = filter(lambda x: x.startswith("[SUM]"), iperf_output["lines"])
  throughputs = []
  
  for sum_line in sum_lines:
    value, unit = sum_line.split()[-2:]

    if unit != "Mbits/sec": 
      raise ValueError('This script only handles Mbit/sec units!')

    throughputs.append(float(value))

  return {
    "throughputs": throughputs,
    "network_type": iperf_output["network_type"]
  }


def read_file(file_path):
  network_type = (
    file_path
      .split("/")[-1] # only get filename without path
      .split(".")[0]  # remove file extension
      .split("_")[-1] # get file_name end which is network id
      .split("-")[0] # strip away the capture number
  )

  with open(file_path, 'r') as file:
    return {
      "lines": file.readlines(),
      "network_type": network_type
    }




main()