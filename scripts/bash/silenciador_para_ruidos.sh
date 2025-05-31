#!/bin/bash
while true
do
    echo checking sound level...
    level=$(arecord -d 1 /dev/shm/tmp_rec.wav 2>/dev/null ; sox -t .wav /dev/shm/tmp_rec.wav -n stat 2>&1 | grep 'Maximum amplit' | cut -d ':' -f 2)
    if (( $(echo "$level > 0.23" | bc -l) ))
    then
        aplay /usr/lib/libreoffice/share/gallery/sounds/cow.wav
    fi
done
