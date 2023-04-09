#!/bin/bash

# Check eth0 adapter status and toggle it
if [[ $(ip link show eth0 | grep 'state' | awk '{print $9}') == "DOWN" ]]; then
    echo "Enabling eth0 adapter"
    ip link set eth0 up
else
    echo "Disabling eth0 adapter"
    ip link set eth0 down
fi

# Check eth1 adapter status and toggle it
if [[ $(ip link show eth1 | grep 'state' | awk '{print $9}') == "DOWN" ]]; then
    echo "Enabling eth1 adapter"
    ip link set eth1 up
else
    echo "Disabling eth1 adapter"
    ip link set eth1 down
fi