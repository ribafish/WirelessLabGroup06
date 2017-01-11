# Question 3: How secure is eduroam

## a) KoreK, PTW and WPA Dictionary attack

First we need some information about eduroam:

* security: WPA2 Enterprise / AES
* EAP Type secured EAP (PEAP)
* uses certificates

Source: [https://www.tubit.tu-berlin.de/wlan/](https://www.tubit.tu-berlin.de/wlan/)

In WPA2 Enterprise we do not authenticate directly against the
AP, but the request is forwarded to a RADIUS server that does
not only check the for the passphrase but requires account based
authentification. 

KoreK and PTW are attacks that only work on WEP and a Dictionary
attack does not work on account based authentification.

There is no practical attack on WPA Enterprise with this configurations known to us, but there are some approaches.

1. Setting up an Network similar to eduroam with own RADIUS server that logs username and tokens. Then force associated
user to deauthenticate and connect to the faked eduroam and
hope they accept the untrusted certificate. Jamming the eduroam
AP could help that the victim pics the faked AP.
Also in at university we would pick a campus
where less technical versed victims roam but internet access
is essential

2. Phishing the credentials via email.
