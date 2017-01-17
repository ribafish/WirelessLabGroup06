# Question 2: TCP performance

## a)

*following commands are issued both on N6 and N15*

monitor interface uses ath9k card, all other ath5k

### Transmission power: 1 dBm

`iw dev wlan0 set txpower fixed 100`

### Transmission rate: 6 Mbps

`iw dev wlan0 set bitrates legacy-2.4 6.0`

### HW mode

`uci show wireless.radio0.hwmode`

Output: `wireless.radio0.hwmode='11g'` on both N6 and N15

### Disable ANI

`echo ani-off > /sys/kernel/debug/ieee80211/phy0/ath5k/ani`

Test:
`cat /sys/kernel/debug/ieee80211/phy0/ath5k/ani | grep "operating mode"`

Output: `operating mode:			OFF`


### Set Noise Immunity Level to 0

`echo noise-low >/sys/kernel/debug/ieee80211/phy0/ath5k/ani`

Test:
`cat /sys/kernel/debug/ieee80211/phy0/ath5k/ani | grep "noise immunity"`

Output: `noise immunity level:		0`

### Enable OFDM Weak Signal Detection

`echo ofdm-on > /sys/kernel/debug/ieee80211/phy0/ath5k/ani`

Test:
`cat /sys/kernel/debug/ieee80211/phy0/ath5k/ani | grep "OFDM weak"`

Output:
`OFDM weak signal detection:	on`

### RX and TX Antenna = 2 and disable diversity

`echo fixed-b >  /sys/kernel/debug/ieee80211/phy0/ath5k/antenna`

Test:

```
echo clear >  /sys/kernel/debug/ieee80211/phy0/ath5k/antenna
cat /sys/kernel/debug/ieee80211/phy0/ath5k/antenna | grep "\[antenna"
```

Output:

```
[antenna 1]	0	0
[antenna 2]	<some number gt 0>	<some number gt 0>
[antenna 3]	0	0
[antenna 4]	0	0
```

Only Antenna 2 sends and receives

## b)

### Template for a capture

Start nc to receive the trace:

ST: `nc ‐l ‐p 8080 > "trace-<tcp/udp>‐<6/24/54>mbps‐$(date +%s).cap"`

Start iperf server (tcp)

N6: `iperf -s`

Start iperf server (udp)

N6: `iperf -s -u`

Start tcpdump on monitor interface on STA

N6: `tcpdump -i wlan1 -s 104 -w- <udp/tcp> and ip src or dst 172.17.5.10 | nc 172.17.3.1 8080`

* -i defines the interface to capture
* -s removes the udp payload to reduce filesize
* -w- outputs to STDOUT
* udp/tcp filters only udp packets
* ip src or dst filters only packets coming or going from host x


Start sending packets with iperf

N15: 

```
for i in `seq 10`; do	iperf ‐c 172.17.5.10 ‐u ‐b <7/25/56>M ‐t 60	sleep 2sdone
```
A loop which performs 10 runs with 60 seconds duration. For the 
tcp run just omit the -u flag.

### Perform runs with these parameters:

*  Time t1, transmission rate 6Mbps, udp
*  Time t1, transmission rate 24Mbps, udp
*  Time t1, transmission rate 54Mbps, udp
*  Time t1, transmission rate 6Mbps, tcp
*  Time t1, transmission rate 24Mbps, tcp
*  Time t1, transmission rate 54Mbps, tcp
*  Time t2, transmission rate 6Mbps, udp
*  Time t2, transmission rate 24Mbps, udp
*  Time t2, transmission rate 54Mbps, udp
*  Time t2, transmission rate 6Mbps, tcp
*  Time t2, transmission rate 24Mbps, tcp
*  Time t2, transmission rate 54Mbps, tcp
