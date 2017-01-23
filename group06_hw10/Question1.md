# Question 1: Communication between Station and AccessPoint

## a) Setup

## b) Data gathering

## c) Questions:

### 1. What is the measured TCP throughput in infrastructure mode from station to access point? Compare this throughput with the physical data rate of 54 Mbps that the hardware is configured with. Can you explain the difference (generic, no calculations needed)?

### 2. Is the TCP throughput lower compared to the UDP throughput? If yes, why?

### 3. What is (are) the limiting factor(s) in the TCP protocol?

### 4. What is the optimum packet size (accuracy 1 byte) and the corresponding data rate for maximum UDP throughput?

[StackOverflow](http://stackoverflow.com/questions/14993000/the-most-reliable-and-efficient-udp-packet-size)

[MTU](https://en.wikipedia.org/wiki/Maximum_transmission_unit)

[PDU](https://en.wikipedia.org/wiki/Protocol_data_unit)

### 5. Why is the throughput lower if you use a packet size higher than the optimum? Explain the optimum value as identified previously.

`Hint: look at configuration settings at network layer (output of ifconfig) and data link layer (output of iwinfo). What are the sizes of the headers of IP, UDP, etc. ? `


### 6. Check the congestion control algorithm in your node `Hint : sysctl -a | grep congestion`. Please carry out measurements twenty times each on TCP Reno and TCP Cubic by sending two parallel iperf streams distributed during the day and plot the throughput and explain your observations.

