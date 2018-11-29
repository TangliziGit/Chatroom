while true; do
    usr=`vmstat 1 3 | awk '{print $13}' | tail -1`
    sys=`vmstat 1 3 | awk '{print $14}' | tail -1`
    tot=`expr $usr + $sys`
    if [ $tot -gt 80 ]
    then
	supervisorctl restart chatroom
	echo '['`date`'] ' 'restart'
	sleep 5s
    fi
done
