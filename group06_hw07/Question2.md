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


* * *

## b) Comparison with the *Rate Control Algorithm Evaluation Paper*

In the paper they comapare different rate control algorithms, focusing on Minstrel, PID and at the end PIDE. We did our tests using only Minstrel, but with different received signal strength configurations, using different transmission powers and different antennas. 

Their test setup was much more extensive. They tested it using three vastly different configurations: 
* **Controllable platform**, where they connected the transcievers using a co-axial cable, with an attenuator in between. 
* **Semi-controlled over-the-air** experiments, where they used actual antennas, but they did them on an empty channel during the night, where there was not interference.
* **In-the-wild over-the-air** experiments, where they used actual antennas, but on a shared channel during office hours, when there were other people using the channel, walking around, using microwaves. These were the real-life experiments, the same that we did.


Furthermore, all experiments they did were performed using IEEE 802.11a. This has two benefits, the first being that the 5 GHz frequency band is currently much less used than 2.4 GHz, and secondly it means that all transmission rates use the same family of modulation and coding methods. On the other hand, we used 802.11g, which uses 2.4GHz, which is used by much more devices, with addition of other interference, not tied to 802.11 standards.

They tested five different scenarios in each group of experiments: static channel, dynamic channel, fading channel, progressive increase/decrease of channel quality and a sudden channel quality change.
We tested just one scenario, the static channel scenario, where we did 6 different experiments. We used three different transmission powers (1dBm, 10dBm, 20dBm) and two different antennas (one is attached, one is without the actual antenna). This all amounts to different received signal strength, but a static channel for each run (as far as we control it).

Realistically, we can only compare our results with *In-the wild over-the-air* experiment results from the paper, but even here there isn't much to compare, given that we only did tests using Minstrel, without testing PID rate control algorithm and in a totaly different environment. We can see that in their tests even in the real-world experiments Minstrel outperformed PID, but the difference wasn't that big. Sadly we can not confirm nor deny this data, as we didn't test PID ourselves.

We can see that their test locations S1 and S3 produced similar throughput to our tests. Interestingly, when comparing those runs to our runs, we can see that Minstrel in their case chose mostly 6Mbps transmission rate, while in our tests it chose mostly 18Mbps (runs without the antenna) or 36Mbps - 54Mbps (runs with the antenna). Their location S2, for which Minstrel chose mostly 18Mbps got a throughput around 13 Mbit/s, while we only got around 4.5 Mbit/s. Their location S4, at which Minstrel chose mostly transmission rate of 36Mbps, got an even better throughput of around 23 Mbit/s, while we still got only marginally better results at around 5 Mbit/s.

Comparing these results is interesting, as in their results the differences in throughput when comparing which transmission rate Minstrel chose are significant, whereas in our test the differences were very small. On the other hand, we have no information on what the environment was like when they did their tests for the paper, so we have no way to actually compare the results with any level of confidence, with the only thing we can say with certainity is that the environment must have been quite different in our experiments versus the experiments for the paper.

The only explanation for such low throughpout in our experiments is that our enviromnet is extremely noisy, as the received signal strength we got was very good, above -65dBm, for which in the *Controllable platform* experiments from the paper, the Minstrel should pick the 54Mbps transmission rate and should have gotten a throughput upwards of 30Mbit/s. 

One explanation we can see, why Minstrel would select such high transmission rates even in a very noisy environment, is that with high transmission rate, the packet takes much less time to transmit and has better chances of not getting destroyed by another packet than a slow transmission rate, where the packet is "on the air" for a longer time. We can then account the low throughput to a very busy environment, where there is a lot of devices talking at the same time, so even though the SNR we got is very good, the throughput is severely limited by MAC because of multiple devices trying to transmit.