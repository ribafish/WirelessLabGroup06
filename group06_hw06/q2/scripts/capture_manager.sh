# !/usr/bin ash


STARTTIME=`date +%s`
DUMPFILE="tcpdump_${STARTTIME}.cap"
SURVEYFILE="surveydump_${STARTTIME}.dump"

echo ""
echo "Starting capture manager"

# reset survey counter
echo "  Resetting counter of survey dump"
echo "1" > "/sys/kernel/debug/ieee80211/phy0/ath5k/reset"

echo "  Starting tcpdump in the background ..."
tcpdump -i wlan0 -w- > $DUMPFILE &
TCPDUMP_PID=`ps | grep "tcpdump -i wlan0" | grep -v grep | awk '{print $1}'`
echo "  tcpdump started with PID $TCPDUMP_PID"

for i in `seq 50`; do
  date +%s >> $SURVEYFILE
  iw dev wlan0 survey dump >> $SURVEYFILE
  sleep 0.1
done

echo "Starting iperf server"
iperf -s -u > /dev/null 2>&1 &
IPERF_PID=`ps | grep "iperf -s -u" | grep -v grep | awk '{print $1}'`
echo "iperf started with PID $IPERF_PID"

for i in `seq 150`; do
  date +%s >> $SURVEYFILE
  iw dev wlan0 survey dump >> $SURVEYFILE
  sleep 0.1
done


kill $IPERF_PID
sleep 1
kill $TCPDUMP_PID






