while true; do
    usr=`vmstat | awk '{print $13}' | tail -1`
    sys=`vmstat | awk '{print $14}' | tail -1`
    tot=`expr $usr + $sys`
    if [ $tot -gt 80 ]
    then
        supervisorctl stop chatroom
        sleep 3s
        supervisorctl start emergency
    fi
    sleep 5s
done
