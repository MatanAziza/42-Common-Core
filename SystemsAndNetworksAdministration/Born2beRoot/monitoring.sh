#!/bin/bash

arch=$(uname -a)

phys=$(grep "physical id" /proc/cpuinfo | wc -l | awk '{printf("Physical processors: %d\n", $1)}')

virt=$(grep "processor" /proc/cpuinfo | wc -l | awk '{printf("Virtual processors: %d\n", $1)}')

ram=$(free --mega | awk '$1 == "Mem:" {printf("Memory used: %ld/%ld (%.2f%%)\n", $3, $2, $3/$2*100)}')

storage=$(df -m | grep "/dev/" | grep -v "/boot" | awk '{memory_use += $3} {total += $2} END {printf("Used storage: %ld (%.2f%%)\n", memory_use, memory_use/total*100)}')

cpu=$(vmstat | tail -1 | awk '{printf("CPU usage (percentage): %d%%\n", $15)}')

reboot=$(who -b | awk '$1 == "system" {print "Last reboot date & time: " $3 " " $4}')

lvm=$(lsblk | grep "lvm" | wc -l | awk '{if ($1 > 0) print "LVM is active"; else print "LVM is inactive"}')

tcp=$(ss -ta | grep "ESTAB" | wc -l | awk '{print "TCP conncted devices: " $1}')

users=$(users | wc -w | awk '{print "Number of users: " $1}')

ip=$(hostname -I | awk '{print "IP Adress: " $1}')

mac=$(ip link | grep "link/ether" | awk '{print "MAC Address: " $2}')

sudos=$(journalctl _COMM=sudo | grep COMMAND | wc -l | awk '{print "Number of executed sudo commands: " $1}')

wall "Architecture: $arch
$phys
$virt
$ram
$storage
$cpu
$reboot
$lvm
$tcp
$users
$ip, $mac
$sudos"
