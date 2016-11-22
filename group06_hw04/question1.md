1. `ip link show`: Shows interfaces, replacement command for `ifconfig -a`. 
At the beginning all Wifi interfaces all down (both nodes)

2. `dmesg | grep -i ath`: shows all initialisations that logged ath, `-i` for case independent.
Used this to confirm that Node 6 has the ath9k interface for monitoring purposes

3. `uci` command explanation (LEDE uses uci configuration files):  [link to LEDE site](https://wiki.lede-project.org/docs/user-guide/introduction_to_lede_configuration)
