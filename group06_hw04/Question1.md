## Question 1:

### Setup group06 node as AP (wlan0)

SSID: group06_ap

#### wireless
`uci set wireless.default_radio0.ssid="group06_ap"`

`uci set wireless.default_radio0.network=wlan0`

`uci set wireless.default_radio0.ifname=wlan0`

`uci set wireless.radio0.disabled=0`

`uci commit`

#### Eventual config wireless

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

config wifi-device 'radio1'
        option type 'mac80211'
        option channel '11'
        option hwmode '11g'
        option path 'pci0000:00/0000:00:0e.0'
        option htmode 'HT20'
        option disabled '1'

config wifi-iface 'default_radio1'
        option device 'radio1'
        option network 'lan'
        option mode 'ap'
        option ssid 'LEDE'
        option encryption 'none'
```

#### network

`uci set network.wlan0=interface`

`uci set network.wlan0.ipaddr="172.17.5.10"`

`uci set network.wlan0.netmask="255.255.255.0"`

`uci set network.wlan0.proto="static"`

`uci set network.wlan0.dns="172.17.255.254"`

`uci set network.wlan0.ifname="wlan0"`

`uci commit`

`wifi`

#### Eventual config network

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

#### Check for success
`iw wlan0 scan | grep 'SSID' | sort -u | awk '{print $2}'`

Output:

```
ClosedWRT
FGINET
Group01
LEDE
TUB-Guest
TUB-intern
WirelessLab-Group04
eduroam
group07
```

### Setup group15 node as STA (wlan0)

#### wireless

`uci set wireless.radio0.path='pci0000:00/0000:00:0e.0'`

`uci set wireless.radio0.disabled=0`

`uci set wireless.default_radio0.network=wlan0`

`uci set wireless.default_radio0.mode="sta"`

`uci set wireless.default_radio0.ssid="group06_ap"`

`uci commit`


#### Eventual config wireless

```

config wifi-device 'radio0'
        option type 'mac80211'
        option channel '11'
        option hwmode '11g'
        option path 'pci0000:00/0000:00:0c.0'
        option disabled '0'

config wifi-iface 'default_radio0'
        option device 'radio0'
        option encryption 'none'
        option network 'wlan0'
        option mode 'sta'
        option ssid 'node15'

config wifi-device 'radio1'
        option type 'mac80211'
        option channel '11'
        option hwmode '11g'
        option path 'pci0000:00/0000:00:0e.0'
        option disabled '1'

config wifi-iface 'default_radio1'
        option device 'radio1'
        option network 'lan'
        option mode 'ap'
        option ssid 'LEDE'
        option encryption 'none'
```
#### network

`uci set network.wlan0=interface`

`uci set network.wlan0.ipaddr="172.17.5.11"`

`uci set network.wlan0.netmask="255.255.255.0"`

`uci set network.wlan0.proto="static"`

`uci set network.wlan0.dns="172.17.255.254"`

`uci commit`

`wifi`

#### Eventual config for network

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
        option ipaddr '172.17.5.11'
        option netmask '255.255.255.0'
        option proto 'static'
        option dns '172.17.255.254'

```

### Setup Node 06 as monitor on ath9k (wlan1)
#### Confirming that radio1 is ath9k card:
1. /etc/config/wireless radio1 definition:


```
config wifi-device 'radio1'
        option type 'mac80211'
        option channel '11'
        option hwmode '11g'
        option path 'pci0000:00/0000:00:0e.0'
        option disabled '0'
```
 
2. check the `path 'pci0000:00/0000:00:0e.0'`, 

which states that radio1 is using the device /sys/devices/pci0000:00/0000:00:0e.0. This device has the driver defined as: 
```
driver -> ../../../bus/pci/drivers/ath9k/
```

#### Wireless setup:

`uci set wireless.radio1.disabled=0`

`uci set wireless.radio1.htmode=NONE` <-  `NONE` 

disables 802.11n rates and enforce the usage of legacy 802.11 b/g/a rates. We set this because the ath5k cards support 802.11a/b/g ONLY

`uci set wireless.default_radio1.mode=monitor`

`uci set wireless.default_radio1.hidden=1`

`uci delete wireless.default_radio1.ssid`

`uci delete wireless.default_radio1.encryption`

`uci commit`

`wifi`

#### Monitor interface confirmation:
* Command `iw wlan1 info` output:

```
Interface wlan1
        ifindex 19
        wdev 0x100000008
        addr a8:54:b2:71:d3:5d
        type monitor
        wiphy 1
        channel 11 (2462 MHz), width: 20 MHz (no HT), center1: 2462 MHz
        txpower 19.00 dBm
        txpower 19.00 dBm
```

* tcpdump works, command: `tcpdump -i wlan1 -c 10`, output:

```
tcpdump: WARNING: wlan1: no IPv4 address assigned
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on wlan1, link-type IEEE802_11_RADIO (802.11 plus radiotap header), capture size 65535 bytes
22:41:48.094199 248638940us tsft 1.0 Mb/s 2462 MHz 11b -27dB signal [bit 29] Beacon (LEDE) [1.0* 2.0* 5.5* 11.0* 6.0 9.0 12.0 18.0 Mbit] ESS CH: 11
22:41:48.094768 248640469us tsft 54.0 Mb/s 2462 MHz 11g -42dB signal [bit 29] Beacon (foobar) [1.0* 2.0* 5.5* 11.0* 6.0 9.0 12.0 18.0 Mbit] ESS CH: 11, PRIVACY
22:41:48.100009 248644218us tsft 1.0 Mb/s 2462 MHz 11b -77dB signal [bit 29] Beacon (FGINET) [1.0* 2.0* 5.5* 11.0* 6.0 9.0 12.0 18.0 Mbit] ESS CH: 11, PRIVACY
22:41:48.102208 248647838us tsft 24.0 Mb/s 2462 MHz 11g -71dB signal [bit 29] Beacon (TUB-intern) [18.0 24.0* 36.0 48.0 54.0 Mbit] ESS CH: 11
22:41:48.122405 248666638us tsft 1.0 Mb/s 2462 MHz 11b -85dB signal [bit 29] Beacon (FGINET) [1.0* 2.0* 5.5* 11.0* 6.0 9.0 12.0 18.0 Mbit] ESS CH: 11, PRIVACY
22:41:48.126398 248671024us tsft 1.0 Mb/s 2462 MHz 11b -60dB signal [bit 29] Beacon (group002) [1.0* 2.0* 5.5* 11.0* 6.0 9.0 12.0 18.0 Mbit] ESS CH: 11
22:41:48.126417 248671981us tsft 6.0 Mb/s 2462 MHz 11g -52dB signal [bit 29] Beacon (Group03) [6.0* Mbit] ESS CH: 11
22:41:48.126782 248672414us tsft 24.0 Mb/s 2462 MHz 11g -71dB signal [bit 29] Beacon (TUB-Guest) [18.0 24.0* 36.0 48.0 54.0 Mbit] ESS CH: 11
22:41:48.142812 248686531us tsft 1.0 Mb/s 2462 MHz 11b -90dB signal [bit 29] Beacon (MMS-TECHNIK) [1.0* 2.0* 5.5* 6.0* 9.0* 11.0* 12.0* 18.0* Mbit] ESS CH: 11, PRIVACY
22:41:48.151366 248696992us tsft 24.0 Mb/s 2462 MHz 11g -71dB signal [bit 29] Beacon (eduroam) [18.0 24.0* 36.0 48.0 54.0 Mbit] ESS CH: 11, PRIVACY
10 packets captured
131 packets received by filter
0 packets dropped by kernel
```


### Eventual config for wireless:
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

config wifi-device 'radio1'
        option type 'mac80211'
        option channel '11'
        option hwmode '11g'
        option path 'pci0000:00/0000:00:0e.0'
        option disabled '0'
        option htmode 'HT20'

config wifi-iface 'default_radio1'
        option device 'radio1'
        option network 'lan'
        option mode 'monitor'
        option hidden '1'
```

### Check inter-connectivity

(ST = Stepping Stone, N6 = Node06, N15 = Node15)

* get IPs for the nodes once more 
	N6: `ifconfig wlan0 | grep 'inet addr' | awk '{print $2}'`
	
	Output: addr:**172.17.5.10**
	
	N15: `ifconfig wlan0 | grep 'inet addr' | awk '{print $2}'`
	
	Output: addr:**172.17.5.11**
	
* Check for reachability

	N6: `ping 172.17.5.11`
	
	Output (trunc): 	64 bytes from 172.17.5.10: seq=1 ttl=64 time=0.188 ms
	
	N15: `ping 172.17.5.10`
	
	Output (trunc): 64 bytes from 172.17.5.10: seq=1 ttl=64 time=1.136 ms
	

**The Nodes are connected.**