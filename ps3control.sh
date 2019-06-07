#!/bin/sh

# Copy from Saved Projects directory to /var/volatile
# Permissions for brickhid.arm are already executable
cp brickhid.arm ps3_tank.config /var/volatile/

killall -STOP udevd
killall bluetoothd
hciconfig hci0 up pscan

/var/volatile/brickhid.arm ps3_tank.config

