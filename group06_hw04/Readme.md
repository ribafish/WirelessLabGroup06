# WirelessLab, Homework 04

## Question 1:

### Useful commands, not tied to specific point in question.

* `ip link show`: Shows interfaces, replacement command for `ifconfig -a`. 
At the beginning all Wifi interfaces all down (both nodes). 

* `dmesg | grep -i ath`: shows all initialisations that logged ath, `-i` for case independent.
Used this to confirm that Node 6 has the ath9k interface for monitoring purposes (phy1). 
So, both nodrs have the `ath5k`radio mapped to phy0 and Node 6 has `ath9k` radio mapped to phy1. 

* `uci` command explanation (LEDE uses uci configuration files):  [link to LEDE site](https://wiki.lede-project.org/docs/user-guide/introduction_to_lede_configuration)

* on the stepping stone there are alias defined to quickly connect to the nodes:
	* `cnode6` will connect you over ip/ssh to node **6**
	* `cnode15` will connect you over ip/ssh to node **15**

* on both nodes in the folder `/etc/config/` configs are backed up under `/etc/config/<filename>.bak` 


### Setup group06 node as AP (wlan1)

SSID: group06_ap

#### wireless
`uci set wireless.default_radio1.ssid="group06_ap"`

`uci set wireless.default_radio1.network=wlan1`

`uci set wireless.default_radio1.ifname=wlan1`

`uci set wireless.radio1.disabled=0`

`uci commit`

#### Eventual config wireless
```

config wifi-device 'radio0'
        option type 'mac80211'
        option channel '11'
        option hwmode '11g'
        option path 'pci0000:00/0000:00:0c.0'
        option disabled '1'

config wifi-iface 'default_radio0'
        option device 'radio0'
        option network 'lan'
        option mode 'ap'
        option ssid 'LEDE'
        option encryption 'none'

config wifi-device 'radio1'
        option type 'mac80211'
        option channel '11'
        option hwmode '11g'
        option path 'pci0000:00/0000:00:0e.0'
        option htmode 'HT20'
        option disabled '0'

config wifi-iface 'default_radio1'
        option device 'radio1'
        option mode 'ap'
        option encryption 'none'
        option ssid 'group06_ap'
        option network 'wlan1'
        option ifname 'wlan1'
```

#### network

`uci set network.wlan1=interface`

`uci set network.wlan1.ipaddr="172.17.5.10"`

`uci set network.wlan1.netmask="255.255.255.0"`

`uci set network.wlan1.proto="static"`

`uci set network.wlan1.dns="172.17.255.254"`

`uci commit`

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

config interface 'wlan1'
        option ifname 'wlan1'
        option ipaddr '172.17.5.10'
        option netmask '255.255.255.0'
        option proto 'static'
        option dns '172.17.255.254'

```

#### Check for success
`iw wlan1 scan | grep 'SSID' | sort -u | awk '{print $2}'`

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



