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
	

4. iperf server command:
	
	`iperf -s -u`
	
	* -s = server mode
	* -u = udp packets

5. start nc on ST

	`nc -l -p 8080 > channel1-<tp>-<tr>.cap`

6. tcpdump on node6

	`tcpdump -i wlan1 -w- | nc 172.17.3.1 8080`
	
7. iperf client command:

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
	* sleep 2s, wait for connection to be closed and set up again

8. Copy Iperf Server output to `iperf-<tp>-<tr>.out`

9. Repeat Step 3, 5, 6, 7, 8 for remaining values

10. TP: 0 dBm, TR: 54mbit/s

	NP15 iperf cmd: `iperf -c 172.17.5.10 -u -b 56M -t 30 -l 1024`
 
 	NP15 tx pwr: `iw wlan0 info | grep txpower` Output: txpower 0.00 dBm [..]
 	
 	NP15 tr : `iw wlan0 link | grep rate` Output: tx bitrate: 54.0 MBit/s
 	
11. TP: 11 dBm, TR: 54mbit/s

	NP15 iperf cmd: `iperf -c 172.17.5.10 -u -b 56M -t 30 -l 1024`
	
	NP15 tx pwr: `iw wlan0 info | grep txpower` Output: txpower 20.00 dBm
	
	NP15 tr : `iw wlan0 link | grep rate` Output: tx bitrate: 54.0 MBit/s
	
	*Couldn't set it to exactly 11dBm, tried a 100 times, 100 ways*