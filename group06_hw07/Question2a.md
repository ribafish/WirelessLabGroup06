# Question 2: Analysis of Rate Control Algorithms

## a) How Minstrel selects its rate when there is something to send.

### Minstrel

* Minstrel is the standard rate control algorithm in Linux `mac80211`
* ACK based mechanism
* Throughput and probability of success for each rate measured/calculated every 100 ms
* The core of the Minstrel rate algorithm is the EWMA, or Exponential Weighted Moving Average

##### Exponential Weighted Moving Average:

EWMA controls the balance of influence of both the old and new packet delivery statistics, as shown here:

$$
P_{new} = (1 - \alpha) * P_{this} + \alpha * P_{previous}
$$

Where: 
* *P~new~* is the weighted probability of success for this interval, which will be used by the rate selection process.
* *~alpha~* is a smoothing factor (or the scaling value) in the EWMA mechanism.
* *P~this~* interval is the probability of success of this interval before the rate selection, and it is calculated as the ratio of the number of packets sent successfully to the number of packets sent.
* *P~Previous~* is the weighted probability of success for the last interval used to select last transmission rate.

### Minstrel retry chain