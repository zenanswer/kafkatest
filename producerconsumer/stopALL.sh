KA_PIDS=$(ps ax | grep -i 'kafka\.Kafka' | grep java | grep -v grep | awk '{print $1}')
if [ -n "$KA_PIDS" ]; then
  kill -9 $KA_PIDS
  sleep 2
fi
ZK_PIDS=$(ps ax | grep -i 'QuorumPeerMain' | grep java | grep -v grep | awk '{print $1}')
if [ -n "$ZK_PIDS" ]; then
  kill -s TERM $ZK_PIDS
fi
