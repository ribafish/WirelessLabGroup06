# Question 1:

### Useful links:
* [`iw` command](https://wireless.wiki.kernel.org/en/users/Documentation/iw)
* [about antenna options](https://sourceforge.net/p/android-x86/kernel/ci/604eeadd1880bddfb155369491cc13fb8d3f9df6/)
* [ani.h file - gitlab](https://gitlab.denx.de/marex/linux-denx/blob/b1cdc4670b9508fcd47a15fbd12f70d269880b37/drivers/net/wireless/ath/ath5k/ani.h)

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
        echo sens-low > /sys/kernel/debug/ath5k/phy0/ani
    * set highest sensitivity (=lowest noise immunity):
        echo sens-high > /sys/kernel/debug/ath5k/phy0/ani
    * automatically control immunity (default):
        echo ani-on > /sys/kernel/debug/ath5k/phy0/ani
    * Noise immunity level
        echo noise-high > /sys/kernel/debug/ath5k/phy0/ani
        echo noise-low > /sys/kernel/debug/ath5k/phy0/ani
    * Control OFDM weak signal detection
        echo ofdm-on > /sys/kernel/debug/ath5k/phy0/ani
        echo ofdm-off > /sys/kernel/debug/ath5k/phy0/ani
    * Control CCK weak signal detection
        echo cck-on > /sys/kernel/debug/ath5k/phy0/ani
        echo cck-off > /sys/kernel/debug/ath5k/phy0/ani
    ```
  
  
  2. Select antenna port B on both `ath5k` cards. Antenna on B is connected, port A is empty.

    ```
    echo fixed-b > /sys/kernel/debug/ieee80211/phy0/ath5k/antenna
    ```
    
    All options:
    
    ```
    echo diversity > antenna: use default antenna mode (RX and TX diversity) - NOTE: this does not reset the antenna file to default value
    echo fixed-a > antenna: use fixed antenna A for RX and TX
    echo fixed-b > antenna: use fixed antenna B for RX and TX
    echo clear > antenna: reset antenna statistics
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
  
  * To change `ofdm` and `cck` settings edit `/sys/kernel/debug/ieee80211/phy0/ath5k/ani` file.
