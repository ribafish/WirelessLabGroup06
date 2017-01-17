### Terminology
* N6: Node 6
* N15: Node 15
* ST: Stepping Stone
* PC: Personal Computer running Linux or Mac OS X

# Question 1: Setup

## a)

already covered in previous tasks. 

SSH Config File on PC for simpler access:

```
host wlab
  HostName wirelesslab.inet.tu-berlin.de
  IdentityFile ~/.ssh/id_rsa_wlab
  User group06

host node6
  HostName 172.17.3.106
  User root
  ProxyJump wlab

host node15
  HostName 172.17.3.115
  User root
  ProxyJump wlab
```

## b)

for this task we need the already installed tools:

* iperf
* iw
* tcpdump
* nc

## c)

### State of `/etc/config/network` on N6

```
config interface 'loopback'
        option ifname 'lo'
        option proto 'static'
        option ipaddr '127.0.0.1'
        option netmask '255.0.0.0'

config interface 'lan'
        option type 'bridge'
        option ifname 'eth0'
        option proto 'dhcp'

config interface 'wlan0'
        option ifname 'wlan0'
        option ipaddr '172.17.5.10'
        option netmask '255.255.255.0'
        option proto 'static'
        option dns '172.17.255.254'
        
```
No change required!

### State of `/etc/config/network` on N15

```
config interface 'loopback'
        option ifname 'lo'
        option proto 'static'
        option ipaddr '127.0.0.1'
        option netmask '255.0.0.0'

config interface 'lan'
        option type 'bridge'
        option ifname 'eth0'
        option proto 'dhcp'

config interface 'wlan0'
        option ifname 'wlan0'
        option ipaddr '172.17.5.11'
        option netmask '255.255.255.0'
        option proto 'static'
        option dns '172.17.255.254'
```

No change required!

### Updated wireless config `/etc/config/wireless` on N6 (AP)

```
config wifi-device 'radio0'
        option type 'mac80211'
        option channel '11'
        option hwmode '11g'
        option path 'pci0000:00/0000:00:0c.0'
        option disabled '0'

config wifi-iface 'default_radio0'
        option device 'radio0'
        option mode 'ap'
        option encryption 'none'
        option ssid 'group06_ap'
        option network 'wlan0'
        option ifname 'wlan0'

```

Apply changes on N6 with: `wifi`

### Updated wireless config `/etc/config/wireless` on N15 (STA)

```
config wifi-device 'radio0'
        option channel '11'
        option hwmode '11g'
        option path 'pci0000:00/0000:00:0e.0'
        option disabled '0'
        option type 'mac80211'

config wifi-iface 'default_radio0'
        option device 'radio0'
        option mode 'sta'
        option ssid 'group06_ap'
        option ifname 'wlan0'
        option network 'wlan0'
```

Apply changes on N15 with: `wifi`

### Check for connection with `ping`

**From N15 to N6:**

N15: `ping 172.17.5.10`

Output (head):

```
PING 172.17.5.10 (172.17.5.10): 56 data bytes
64 bytes from 172.17.5.10: seq=0 ttl=64 time=3.817 ms
```

N6 is reachable from N15.

**From N6 to N15:**

N6: `ping 172.17.5.11`

Output (head):

```
PING 172.17.5.11 (172.17.5.11): 56 data bytes
64 bytes from 172.17.5.11: seq=0 ttl=64 time=1.995 ms
```

N15 is reachable from N6.

**From ST to N6:**

ST: `ping 172.17.3.106` (ip address of wired interface)

Output (head):

```
PING 172.17.3.106 (172.17.3.106) 56(84) bytes of data.
64 bytes from 172.17.3.106: icmp_seq=1 ttl=64 time=0.787 ms
```

N6 is reachable from ST.

**From ST to N15:**

ST: `ping 172.17.3.115` (ip address of wired interface)

Output (head):

```
PING 172.17.3.115 (172.17.3.115) 56(84) bytes of data.
64 bytes from 172.17.3.115: icmp_seq=1 ttl=64 time=0.712 ms
```

N15 is reachable from ST.

## d)

N6 has a monitor capable interface. we called it `wlan1`
With the wireless configuration above we already configured it.

Now test if it still works:

N6: `tcpdump -i wlan1 -c 1`

* -i argument defines the interface on which we want to capture
* -c argument is the number of packets we want to trace


Output:

```
tcpdump: WARNING: wlan1: no IPv4 address assigned
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on wlan1, link-type IEEE802_11_RADIO (802.11 plus radiotap header), capture size 65535 bytes
11:50:26.198838 828674862us tsft 24.0 Mb/s 2412 MHz 11g -71dB signal [bit 29] Beacon (TUB-intern) [18.0 24.0* 36.0 48.0 54.0 Mbit] ESS CH: 1
1 packet captured
118 packets received by filter
0 packets dropped by kernel
```

Monitoring works.
