# Question 1:

### Setup:
  1. Disable ANI on both `ath5k` cards:
  
    ```
    echo "ani-off" > /sys/kernel/debug/ieee80211/phy0/ath5k/ani
    ```
  
  
  2. Select antenna port B on both `ath5k` cards. Antenna on B is connected, port A is empty.

    ```
    echo "fixed-B" > /sys/kernel/debug/ieee80211/phy0/ath5k/antenna
    ```
    
  3. Set modulation on both cards to 24 Mbps:
    
    ```
    iw wlan0 set bitrates legacy-2.4 24
    ```
    
  4. Check bitrate and tx power:
    
    ```
    iw wlan0 station dump | grep 'tx bitrate'
    iw wlan0 info | grep txpower
    ```
    
  6. Check that nodes are connected using ping or iperf
