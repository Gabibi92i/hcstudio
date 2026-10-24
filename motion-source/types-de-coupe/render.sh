#!/bin/bash
# Rendu (1 seul processus : machine partagée) puis encodage master crf 14 + mix audio
set -e; export NODE_PATH=$(npm root -g)
FPS=60; DUR=28.2; N=$(python3 -c "print(round($DUR*$FPS))"); D=${1:-frames}
rm -rf $D; node frames.js scene.html $D $FPS 0 $N
ffmpeg -loglevel error -y -framerate $FPS -i $D/%05d.jpg -c:v libx264 -pix_fmt yuv420p -profile:v high -preset slow -crf 14 -x264-params aq-mode=3 master.mp4
python3 synth.py
ffmpeg -loglevel error -y -i master.mp4 -i audio.wav -map 0:v -map 1:a -c:v copy -af loudnorm=I=-14:TP=-1.5:LRA=11 -ar 48000 -c:a aac -b:a 192k -shortest final-crf14.mp4
ffmpeg -loglevel error -y -i final-crf14.mp4 -c:v libx264 -pix_fmt yuv420p -profile:v high -preset slow -crf 20 -c:a copy -movflags +faststart reel.mp4
echo RENDER_OK
