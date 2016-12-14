# Question 1: RCA in mac802.11

Network & Terminology:

 * N6  = Node 6  (172.17.5.10 on wlan0, 172.17.3.106 on br-lan)
 * N15 = Node 15 (172.17.5.11 on wlan0)
 * ST  = Stepping Stone (172.17.3.1 on eth1)

## a)

### Setup:

* checking connectivity:

	* **N6 <-> N15**:

		N6: `ping -I wlan0 172.17.5.11 | head -n 2` 
		
		Output: 
		
		```
		PING 172.17.5.11 (172.17.5.11): 56 data bytes
		64 bytes from 172.17.5.11: seq=0 ttl=64 time=0.615 ms
		```
		
		*Connected*
		
	* **N6 <-> ST**:
	
		N6: `ping -I br-lan 172.17.3.1 | head -n 2`
		
		Output:
		
		```
		PING 172.17.3.1 (172.17.3.1): 56 data bytes
		64 bytes from 172.17.3.1: seq=0 ttl=64 time=0.645 ms
		```
		
		*Connected*
		
* checking channel on wireless, either (1,6,11)

	* N6: `iw wlan0 info | grep channel`

		Output:
		`channel 11 (2462 MHz), width: 20 MHz (no HT), center1: 2462 MHz`
		
	* N6: `iw wlan1 info | grep channel`

		Output: 
		`channel 11 (2462 MHz), width: 20 MHz (no HT), center1: 2462 MHz`
		
	* N15: `iw wlan0 info | grep channel`
	
		Output:
		`channel 11 (2462 MHz), width: 20 MHz (no HT), center1: 2462 MHz`
		
	*All cards are on the same channel (11)*
	

* set transmission power to 1.0 dBm on sender

	* N15: `iw dev wlan0 set txpower fixed 100; iw wlan0 info | grep txpower`

		Output (1st line):
	
		`txpower 1.00 dB`
	
* set antenna A fixed for both sender and receiver

	* N6: `echo "fixed-a" > /sys/kernel/debug/ieee80211/phy0/ath5k/antenna`
	
	* N15: `echo "fixed-a" > /sys/kernel/debug/ieee80211/phy0/ath5k/antenna`

* check if ministrel is enabled

	* N15: `dmesg | grep "ieee80211 phy0"`

		Output: 
		
		```
		[   14.225247] ieee80211 phy0: Selected rate control algorithm 'minstrel_ht'
		```
		
		Ministel is enabled
	
* start nc on ST to receive the trace

	* ST: `nc -l -p 8080  > "trace-ch11-1dbm-ant1-$(date +%s).cap"`
	
		File naming structure:
		
		`trace-<ch + channel>-<tx_power + dbm>-<ant + antenna used>-<unix timestamp>.cap`
	
* start iperf server on receiver

	* N6: `iperf -s -u`

* start tcpdump on receiver without capturing the udp body, forward to ST

	* N6: `tcpdump -i wlan1 -s 104 -w- udp | nc 172.17.3.1 8080`
	
		* `-s 104` snaplen of 104 bytes on the frames. enought to have udp header
		* `-i wlan1` interface of the monitor
		* `-w-` outputs to STDOUT

* start iperf client on sender

	* N15: 

		```
		for i in `seq 12`; do 
	    	iperf -c 172.17.5.10 -u -b 55M -t 30 -l 1024
			sleep 2s
		done
		```
		
* Repeat with different txpower and antenna settings:

	* txpower = 10.00dBm, Ant 1

		* n15: `iw dev wlan0 set txpower fixed 1000; iw wlan0 info | grep txpower`
	
		* Output (1st line): 
	
			```
			txpower 10.00 dBm
			```
		* ST: `nc -l -p 8080 > "trace-ch11-10dbm-ant1-$(date +%s).cap"`
	
	* txpower = 20.00dBm, Ant 1

		* n15: `iw dev wlan0 set txpower fixed 2000; iw wlan0 info | grep txpower`
	
		* Output (1st line): 
	
			```
			txpower 20.00 dBm
			```
		* ST: `nc -l -p 8080 > "trace-ch11-20dbm-ant1-$(date +%s).cap"`

		
	* txpower = 1.00dBm, Ant 2

		* n15: `iw dev wlan0 set txpower fixed 100; iw wlan0 info | grep txpower`
	
		* Output (1st line): 
	
			```
			txpower 1.00 dBm
			```
			
		* n6: `echo "fixed-b" > /sys/kernel/debug/ieee80211/phy0/ath5k/antenna`

 		* n15: `echo "fixed-b" > /sys/kernel/debug/ieee80211/phy0/ath5k/antenna`
		
		* ST: `nc -l -p 8080 > "trace-ch11-1dbm-ant2-$(date +%s).cap"`

	* txpower = 10.00dBm, Ant 2

		* n15: `iw dev wlan0 set txpower fixed 1000; iw wlan0 info | grep txpower`
	
		* Output (1st line): 
	
			```
			txpower 10.00 dBm
			```
		
		* ST: `nc -l -p 8080 > "trace-ch11-10dbm-ant2-$(date +%s).cap"`

	* txpower = 20.00dBm, Ant 2

		* n15: `iw dev wlan0 set txpower fixed 2000; iw wlan0 info | grep txpower`
	
		* Output (1st line): 
	
			```
			txpower 20.00 dBm
			```
		
		* ST: `nc -l -p 8080 > "trace-ch11-20dbm-ant2-$(date +%s).cap"`
	
* Repeat all steps at a different time of the day
