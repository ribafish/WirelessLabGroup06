## Question 2:

### a)
* Selected channels: 1, 6, 11 (should be most used ones)
* Wireless setup:
  
  * Channel setup:  
    `iw wlan1 set channel <cnumber>`    
    `iw wlan1 info` to check wlan1 monitoring interface status

* Logging command: We decided to stop logging after 5min (ST = Stepping Stone, N6 = Node 6)
	* **Channel 1**
		
		ST: `nc -l -p 8080 > channel1.cap`
		
		N6: `iw wlan1 set channel 1`
		
		N6: `iw wlan1 info | grep channel`
		
		Output: channel 1 (2412 MHz), width: 20 MHz (no HT), center1: 2412 MHz
		
		N6: `tcpdump -i wlan1 -G 300 -w- | nc 172.17.3.1 8080`
		
		
	* **Channel 6**
		
		ST: `nc -l -p 8080 > channel6.cap`
		
		N6: `iw wlan1 set channel 6`
		
		N6: `iw wlan1 info | grep channel`
		
		Output: channel 6 (2437 MHz), width: 20 MHz (no HT), center1: 2437 MHz
		
		N6: `tcpdump -i wlan1 -G 300 -w- | nc 172.17.3.1 8080`
		

	* **Channel 11**
		
		ST: `nc -l -p 8080 > channel11.cap`
		
		N6: `iw wlan1 set channel 11`
		
		N6: `iw wlan1 info | grep channel`
		
		Output: channel 11 (2462 MHz), width: 20 MHz (no HT), center1: 2462 MHz
		
		N6: `tcpdump -i wlan1 -G 300 -w- | nc 172.17.3.1 8080`
		

**tcpdump flags explained:**
 
 * `-i wlan1` sets it to listen on interface 1 (Monitor)
      
 * `-G 300` sets it to listen for 300s or 5min
   
 *all traces are saved at ~/hw04/q2a/ on ST*
 
 
  

  

