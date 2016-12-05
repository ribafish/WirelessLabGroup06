# Question 1
## a) Data throughput with and without RTS/CTS

The following figure gives an overview of the data flow from 
a STA to an AP without using RTS/CLS mechanism. A few general assumptions were made:

* no loss or collsion during transmission
* no interference 
* no hidden or exposed terminals

![](q1/transmission_without_RTS_CTS.png)

Defintions:

* DIFS time: $t_{DIFS} = 34\ \mu s$
* Slot Time: $t_{ST} = 9\ \mu s$
* Maximal Backoff: $b_{max} = 15$
* Random Backoff: $RB = \{ n : \text{n is an integer; and } 1 \leq n \leq b_{max} \}$
* Expected Backoff: $b_{expt} = \frac{b_{max} + 1}{2} = 8$
* Contention Window: $t_{CW} = b_{expt} \cdot t_{ST} = 72\ \mu s$
* Propagation Delay: $t_{pd} = 1\ \mu s$
* SIFS time: $t_{SIFS} = 16\ \mu s$
* PHY Layer Overhead = $t_{phy} = 20\ \mu s$
* OFDM Symbol Duration = $t_{ODFM} = 4\ \mu s$
* Mac layer data payload = $d_{mpay} = 1452\ B$
* Max header size = $d_{mhead} = 28\ B$
* Data Transmission Time: $t_{trans} = $