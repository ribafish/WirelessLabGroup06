# WirelessLab, Homework 04

## Question 1:

### Useful commands, not tied to specific point in question.

* `ip link show`: Shows interfaces, replacement command for `ifconfig -a`. 
At the beginning all Wifi interfaces all down (both nodes)

* `dmesg | grep -i ath`: shows all initialisations that logged ath, `-i` for case independent.
Used this to confirm that Node 6 has the ath9k interface for monitoring purposes

* `uci` command explanation (LEDE uses uci configuration files):  [link to LEDE site](https://wiki.lede-project.org/docs/user-guide/introduction_to_lede_configuration)
