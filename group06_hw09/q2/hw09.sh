#!/bin/bash

EXP=/home/pi/WirelessLab/hw09/hw09.exp
LOG=/home/pi/WirelessLab/hw09/hw09.log 

$EXP 6 7 udp >> $LOG
$EXP 24 26 udp >> $LOG
$EXP 54 58 udp >> $LOG
$EXP 6 7 tcp >> $LOG
$EXP 24 26 tcp >> $LOG
$EXP 54 58 tcp >> $LOG
