# WirelessLab, Homework 04

* [Question 1](Question1.md)

* [Question 2](Question2.md)


### Useful commands, not tied to specific point in question.

* `ip link show`: Shows interfaces, replacement command for `ifconfig -a`. 
At the beginning all Wifi interfaces all down (both nodes). 

* `dmesg | grep -i ath`: shows all initialisations that logged ath, `-i` for case independent.
Used this to confirm that Node 6 has the ath9k interface for monitoring purposes (phy1). 
So, both nodrs have the `ath5k`radio mapped to phy0 and Node 6 has `ath9k` radio mapped to phy1. 

* `uci` command explanation (LEDE uses uci configuration files):  [link to LEDE site](https://wiki.lede-project.org/docs/user-guide/introduction_to_lede_configuration)

* on the stepping stone there are alias defined to quickly connect to the nodes:
	* `cnode6` will connect you over ip/ssh to node **6**
	* `cnode15` will connect you over ip/ssh to node **15**

* on both nodes in the folder `/etc/config/` configs are backed up under `/etc/config/<filename>.bak` 



