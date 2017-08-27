while true; do
    echo $((1-`cat /sys/class/gpio/gpio337/value`)) > /sys/class/gpio/gpio337/value
    ping -c 1 -W 1 $1 >/dev/null
    echo $? > /sys/class/gpio/gpio338/value
    sleep 1
done
