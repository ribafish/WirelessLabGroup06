# WirelessLab, Homework 04

* [Back to Readme.md](Readme.md)

## Question 2:

### a)
* Selected channels: 1, 6, 11 (should be most used ones)
* Wireless setup:
  
  * Channel setup: 
  
    `uci set wireless.radio1.channel=1` (or 6 or 11)

    `uci commit`

    `reboot` -> `wifi` and `/etc/init.d/network restart` do not change channel, don't know the reason
    
    `iw wlan1 info` to check wlan1 monitoring interface status

* Logging command: We decided to stop logging after 5min because of space constraints -> 
nc on SteppingStone doesn't accept incoming connections, all ports are closed

`tcpdump -i wlan1 -G 300 -W 1 -w channel1.cap` (and channel6.cap and channel11.cap)
  `-i wlan1` sets it to listen on interface 1
  `-G 300` sets it to listen for 300s
  `-W 1` sets the maximum files to be written to 1
  `-w filename` sets the file to which output is written
all traces are saved at ~/hw04/q1a/ on SteppingStone
  

