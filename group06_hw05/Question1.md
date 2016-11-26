# Question 1: Weak vs. strong signal detection

### Useful links:
* [`iw` command](https://wireless.wiki.kernel.org/en/users/Documentation/iw)
* [about antenna options](https://sourceforge.net/p/android-x86/kernel/ci/604eeadd1880bddfb155369491cc13fb8d3f9df6/)
* [ani.h file - gitlab](https://gitlab.denx.de/marex/linux-denx/blob/b1cdc4670b9508fcd47a15fbd12f70d269880b37/drivers/net/wireless/ath/ath5k/ani.h)
* [debug commands info - also useful info on how to set stuff in general on debugfs files](http://osdir.com/ml/linux.drivers.ath5k.devel/2007-12/msg00011.html)
* [supported ani modes](https://gitlab.tkn.tu-berlin.de/wishful/wishful_module_wifi_ath/commit/096248f71d33603d0c7631e995c536469131ad94?view=inline)

### Setup:
  1. Disable ANI on both `ath5k` cards: **NOTE: if nodes loose connection the ani settings will reset**
  
    ```
    echo ani-off > /sys/kernel/debug/ieee80211/phy0/ath5k/ani
    ```
    
    This changes value in `/sys/kernel/debug/ieee80211/phy0/ath5k/ani` from `AUTO` to `OFF`
    
    Other options for ani are:
    
    ```
    echo ani-auto > /sys/kernel/debug/ieee80211/phy0/ath5k/ani
    echo ani-on > /sys/kernel/debug/ieee80211/phy0/ath5k/ani
    
    * set lowest sensitivity (=highest noise immunity):
        echo sens-low > /sys/kernel/debug/ieee80211/phy0/ath5k/ani
    * set highest sensitivity (=lowest noise immunity):
        echo sens-high > /sys/kernel/debug/ieee80211/phy0/ath5k/ani
    * automatically control immunity (default):
        echo ani-on > /sys/kernel/debug/ieee80211/phy0/ath5k/ani
        
      --------------- These sometimes? don't all work as expected ----------------
    * Noise immunity level
        echo noise-high > /sys/kernel/debug/ieee80211/phy0/ath5k/ani
        echo noise-low >/sys/kernel/debug/ieee80211/phy0/ath5k/ani
    * Control OFDM weak signal detection
        echo ofdm-on > /sys/kernel/debug/ieee80211/phy0/ath5k/ani
        echo ofdm-off > /sys/kernel/debug/ieee80211/phy0/ath5k/ani
    * Control CCK weak signal detection
        echo cck-on > /sys/kernel/debug/ieee80211/phy0/ath5k/ani
        echo cck-off > /sys/kernel/debug/ieee80211/phy0/ath5k/ani
    ```
  
  
  2. Select antenna port B on both `ath5k` cards. Antenna on B is connected, port A is empty.

    ```
    echo fixed-b > /sys/kernel/debug/ieee80211/phy0/ath5k/antenna
    ```
    
    All options:
    
    ```
    echo diversity >  /sys/kernel/debug/ieee80211/phy0/ath5k/antenna     use default antenna mode (RX and TX diversity) - NOTE: this does not reset the antenna file to default value
    echo fixed-a >  /sys/kernel/debug/ieee80211/phy0/ath5k/antenna       use fixed antenna A for RX and TX
    echo fixed-b >  /sys/kernel/debug/ieee80211/phy0/ath5k/antenna       use fixed antenna B for RX and TX
    echo clear >  /sys/kernel/debug/ieee80211/phy0/ath5k/antenna         reset antenna statistics
    ```
    
  3. Set modulation on both cards to 24 Mbps:
    
    ```
    iw wlan0 set bitrates legacy-2.4 24
    ```
    
  4. Set tx power and check it, check bitrate:
    
    ```
    iw dev wlan0 set txpower fixed 100    (100* mBm == 1 dBm)
    ```
    
  5. Check txpower, bitrate, antenna and ani settings:
  
    ```
    iw wlan0 info | grep txpower
    
    iw wlan0 station dump | grep 'tx bitrate'
    
    cat /sys/kernel/debug/ieee80211/phy0/ath5k/antenna
    
    cat /sys/kernel/debug/ieee80211/phy0/ath5k/ani | grep "operating\|OFDM\|CCK" | grep -v "errors"
    ```
    
  6. Check that nodes are connected using ping or iperf
  
  7. Start iperf server on Node 6
  
  `iperf -s -u`
  
  8. Start nc on SteppingStone
  
  `nc -l -p 8080 > filename.cap`
  
  9. Start tcpdump piped to nc on Node 6
  
  `tcpdump -i wlan1 -w- | nc 172.17.3.1 8080`
  
  10. Iperf command on Node 15
  
  ```
  for i in `seq 10`; do 
      iperf -c 172.17.5.10 -u -b 25M -t 30 -l 1024
      sleep 2s
  done
  ```
  
## Runs:
1. Ani-off, cck-off, ofdm-off, Antenna-b, txpower 0dBm: `weak-off.cap`
2. Ani-off, cck-on, ofdm-on, Antenna-b, txpower 0dBm: `weak-on.cap`
3. Ani-off, cck-on, ofdm-on, Antenna-b, txpower 0dBm, sens-high: `sens-high.cap`
4. Ani-off, cck-on, ofdm-on, Antenna-b, txpower 0dBm, sens-low: `sens-low.cap`

  * on sender node (node15) we had to run ani-on as otherwise the nodes wouldn't connect.

5. Ani-off, cck-on, ofdm-on, Antenna-b, txpower 0dBm, noise-high: `noise-high.cap`
6. Ani-off, cck-on, ofdm-on, Antenna-b, txpower 0dBm, noise-low: `noise-low.cap`
