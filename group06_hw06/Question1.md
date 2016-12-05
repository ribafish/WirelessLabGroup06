# Question 1
## a) Data throughput with and without RTS/CTS

The following figure gives an overview of the data flow from 
a STA to an AP without using RTS/CLS mechanism. A few general assumptions were made:

* no loss or collsion during transmission
* no interference 
* no hidden or exposed terminals
* no fragmentation

<!--![](q1/transmission_without_RTS_CTS.png)-->

Defintions:

* DIFS time: $t_{DIFS} = 34\ \mu s$
* Slot Time: $t_{ST} = 9\ \mu s$
* Maximum backoff slots: $b_{max} = 15$
* Random backoff: $RB = \{ n : \text{n is an integer; and } 1 \leq n \leq b_{max} \}$
* Expected backoff: $b_{expt} = \frac{b_{max} + 1}{2} = 8$
* Contention window: $t_{CW} = b_{expt} \cdot t_{ST} = 72\ \mu s$
* Propagation delay: $t_{pd} = 1\ \mu s$
* SIFS time: $t_{SIFS} = 16\ \mu s$
* PHY layer overhead = $t_{phy} = 20\ \mu s$
* OFDM symbol duration = $t_{ODFM} = 4\ \mu s$
* MAC layer data payload = $d_{mpay} = 1452\ B$
* MAC header size = $d_{mhead} = 28\ B$
* MAC ack size = $d_{mack} = 14\ B$
* PHY Layer transmission rate: $r = 54\ \text{Mbps} = 7.077888\ \frac{B}{\mu s} $
* Transmission duration data: $t_{data} = t_{phy} + t_{ODFM} + \frac{d_{mhead} + d_{mpay}}{r} \approx 233\ \mu s$
* Transmission duration ack: $t_{ack} = t_{phy} + t_{ODFM} + \frac{d_{mhead} + d_{mack}}{r} \approx 30\ \mu s$
* Total Time: $t_{total} = t_{DIFS} + t_{CW} + 2 \cdot t_{pd} + t_{data} + t_{SIFS} + t_{ack} = 387\ \mu s$