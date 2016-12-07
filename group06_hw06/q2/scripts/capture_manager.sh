# !/usr/bin ash


STARTTIME=`date +%s`
DUMPFILE="tcpdump_${STARTTIME}.cap"
SURVEYFILE="surveydump_${STARTTIME}.dump"

echo ""
echo "Starting capture manager"
echo "Make sure you started nc on SteppingStone with command:  nc -l -p 8080 > filename.cap"

# reset survey counter
echo "  Resetting counter of survey dump"
echo "1" > "/sys/kernel/debug/ieee80211/phy0/ath5k/reset"

echo "  Starting tcpdump in the background ..."
# tcpdump -i wlan1 -w- > $DUMPFILE &
tcpdump -i wlan1 -w- | nc 172.17.3.1 8080 &
TCPDUMP_PID=`ps | grep "tcpdump -i wlan1" | grep -v grep | awk '{print $1}'`
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

      for i in `seq 200`; do
        date +%s >> $SURVEYFILE
	  iw dev wlan0 survey dump >> $SURVEYFILE
	    sleep 0.1
	    done


	    kill $IPERF_PID
	    sleep 1
	    kill $TCPDUMP_PID







