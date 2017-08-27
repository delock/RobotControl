*Note, works on Joule 570x/550x only, if your board have other LED status or you use external status, use your own led port*

LED indicator could come in handy when you want to quickly check whether the CPU board is active and whether network is good.

Note: always copy the script to somewhere else, don't execute them directly from git directory, because these scripts needs
to be executed as *root* and is not safe to do so when a pull operation will change the script.

*Keep these scripts as non-exec to make sure a copy will be needed*

1. create a new directory to put the script in, such as /root/bin/led/
2. copy init.sh and led.sh to the new directory
3. cd to the new directory
4. chmod 750 init.sh
5. chmod 750 led.sh
6. in /etc/rc.local, add the following two lines
    <full path to new directory>/init.sh
    <full path to new directory>/led.sh <LAN router addr> &
    "LAN router addr" is the ip address of your router, usually it is 192.168.0.1, but might be other address if you changed it.   If you are not sure, ask your network admin

After you reboot your system, the first led (named gpio0) will blink (at 1Hz or 0.5Hz), and the second led (named gpio1) will light if the network is not up yet.   After your dev board successfully connected to the network and get an valid IP address, the second led will be off.
