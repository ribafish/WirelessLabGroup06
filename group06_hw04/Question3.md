## Question 3:

(ST = Stepping Stone, N6 = Node 6, N15 Node 15)

### a)

1. Check that all interfaces are on the same channel

	N6 `iw wlan0 info | grep channel` Output: channel 11 [..]
	
	N6 `iw wlan1 info | grep channel` Output: channel 11 [..]
	
	N15 `iw wlan0 info | grep channel` Output: channel 11 [..]
	
	Fine. All are on the same CH

2. check settings on N6
	
	`iw wlan0 info | grep txpower`
	
 	Output: txpower 30.00 dBm
 	
 	TX Power on Max

3. setup transmission power (tp) and transmission rate (tr) on N15

	`iw wlan0 set txpower fixed 0`
	
	`iw wlan0 info | grep txpower`
	
	Output: txpower 0.00 dBm
	
	`iw wlan0 set bitrates legacy-2.4 6`
	
	`iw wlan0 station dump | grep 'tx bitrate'`
	
	Output: tx bitrate:	6.0 MBit/s
	

4. iperf server command (N6):
	
	`iperf -s -u`
	
	* -s = server mode
	* -u = udp packets

5. start nc  (ST)

	`nc -l -p 8080 > channel11-<tp>-<tr>.cap`

6. tcpdump on N6

	`tcpdump -i wlan1 -w- | nc 172.17.3.1 8080`
	
7. iperf client command (N15):

	```
	for i in `seq 12`; do 
		iperf -c 172.17.5.10 -u -b 7M -t 30 -l 1024
		sleep 2s
	done
	```

	
	* -c = client mode (server ip)
	* -u = upd packets
	* -b = bandwidth #
	* -t = test interval #
	* -l = upd packet size #
	* sleep 2s, wait for connection to be closed

8. Copy iperf Server output to `iperf-<tp>-<tr>.out`

9. Repeat Step 3, 5, 6, 7, 8 for remaining values

10. TP: 0 dBm, TR: 54mbit/s

	NP15 iperf cmd: `iperf -c 172.17.5.10 -u -b 56M -t 30 -l 1024`
 
 	NP15 tx pwr: `iw wlan0 info | grep txpower` Output: txpower 0.00 dBm
 	
 	NP15 tr : `iw wlan0 link | grep rate` Output: tx bitrate: 54.0 MBit/s
 	
11. TP: 11 dBm, TR: 54mbit/s

	NP15 iperf cmd: `iperf -c 172.17.5.10 -u -b 56M -t 30 -l 1024`
	
	NP15 tx pwr: `iw wlan0 info | grep txpower` Output: txpower 11.00 dBm
	
	NP15 tr : `iw wlan0 link | grep rate` Output: tx bitrate: 54.0 MBit/s
	
12. TP: 11dBm, TR: 6mbit/s

	NP15 iperf cmd: `iperf -c 172.17.5.10 -u -b 7M -t 30 -l 1024`
	
	NP15 tx pwr: `iw wlan0 info | grep txpower` Output: txpower 11.00 dBm
	
	NP15 tr : `iw wlan0 link | grep rate` Output: tx bitrate: 6.0 MBit/s
	
13. TP: 0 dBm, TR: 6mbit/s

	NP15 iperf cmd: `iperf -c 172.17.5.10 -u -b 7M -t 30 -l 1024`
 
 	NP15 tx pwr: `iw wlan0 info | grep txpower` Output: txpower 0.00 dBm
 	
 	NP15 tr : `iw wlan0 link | grep rate` Output: tx bitrate: 6.0 MBit/s
	

### b)
![Image of RSS ECDF](https://github.com/ribafish/WirelessLabGroup06/blob/master/group06_hw04/q3/rss_ECDF.png)
![Image of RSS boxplot](https://github.com/ribafish/WirelessLabGroup06/blob/master/group06_hw04/q3/rss_box.png)
![Image of Throughput ECDF](https://github.com/ribafish/WirelessLabGroup06/blob/master/group06_hw04/q3/throughput_ECDF.png)
![Image of Throughput boxplot](https://github.com/ribafish/WirelessLabGroup06/blob/master/group06_hw04/q3/throughput_box.png)

* Medians:

```
54Mbit/s@0dBm: median = 5.013333Mbit/s
6Mbit/s@0dBm: median = 3.360000Mbit/s
54Mbit/s@11dBm: median = 6.093333Mbit/s
6Mbit/s@11dBm: median = 4.186667Mbit/s
```

```
54Mbit/s@0dBm: median = -25dBm
6Mbit/s@0dBm: median = -65dBm
54Mbit/s@11dBm: median = -25dBm
6Mbit/s@11dBm: median = -26dBm
```

* From RSS plots we can conclude that there was some kind of interference when capturing scenario 2 (6Mbit/s, 0dBm), which produced so much readings at -65dBm to push the median to -65dBm, as opposed to other scenario medians, which are around -25dBm. We see no other reason for this scenario to be that much worse than the others. Although it is true that with wour settings (7Mbit/s on 6Mbit/s medium and 56Mbit/s on 54Mbit/s medium) this is expected to be the worst run, as it's at the lower power and 17% oversaturated we don't think this would give such a drastic difference when looking at RSS value. What is also interesting is that 54Mbit/s at 0dBm power is the best performing run, instead of 54Mbit/s at 11dBm. On ewould expect the latter one to perform the best, as it's saturated only by 4% and has the highest transmit power, although saturation shouldn't have much impact on received strength.

* When we look at throughput everything is following expectations, as all the runs are lower than the max throughput medium supports because of medium saturation. We also expected to see a better throughput with higher transmit power. We were quite surprised by how much the throughput has fallen of maximum for 54Mbit/s medium, but we do acknowledge that we used Channel 11, which is probably most used in this environment. When we look at boxplot of scenario 6Mbit/s at 0dBm we again see something interesting, as the 75% quartile is lower than higher confidence interval of median, which tells us that the median is quite unconfident with our dataset of this scenario.

	
	
