#!/bin/bash
mkdir -p /home/ubuntu/participant_audio/$1
mkdir -p /home/ubuntu/participant_data/$1
cp /home/ubuntu/rero_core/conf/config.ini.template /home/ubuntu/rero_core/conf/config.ini
sed -i "s:<storeAudioPath>:/home/ubuntu/participant_audio/$1:g" /home/ubuntu/rero_core/conf/config.ini
sudo service rerocore restart
sleep 1m
