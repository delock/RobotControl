# open gpio port 0~3
echo 337 > /sys/class/gpio/export
echo 338 > /sys/class/gpio/export
echo 339 > /sys/class/gpio/export
echo 340 > /sys/class/gpio/export

# set gpio ports to out
echo out >/sys/class/gpio/gpio337/direction
echo out >/sys/class/gpio/gpio338/direction
echo out >/sys/class/gpio/gpio339/direction
echo out >/sys/class/gpio/gpio340/direction
