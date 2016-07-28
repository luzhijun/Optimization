#!/bin/bash
device=`df |cut -d ' ' -f 1|grep /dev/`
rm -rf /dev/shm/*
rm -rf test.iso
(echo "read from disk ")>>out
(time dd if=$device of=/dev/shm/test.iso  bs=20k count=100000)2>>out
(echo "write in shm " )>>out
(time cp /dev/shm/test.iso /dev/shm/test1.iso)2>>out
(echo "read from shm")>>out
(time mv /dev/shm/test1.iso ./)2>>out
