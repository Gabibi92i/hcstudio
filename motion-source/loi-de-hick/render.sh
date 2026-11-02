#!/bin/bash
# Rendu (1 seul processus : la machine rend d'autres reels en parallèle) puis encodage master crf 14 + mix audio
set -e; export NODE_PATH=$(npm root -g)
node times.js scene.html > times.json
FPS=60; DUR=$(python3 -c "import json;print(json.load(open('times.json'))['dur'])"); N=$(python3 -c "print(round($DUR*$FPS))"); D=${1:-frames}
rm -rf $D; node frames.js scene.html $D $FPS 0 $N
ffmpeg -loglevel error -y -framerate $FPS -i $D/%05d.jpg -c:v libx264 -pix_fmt yuv420p -profile:v high -preset slow -crf 14 -x264-params aq-mode=3 -threads 2 master.mp4
python3 synth.py
# limiteur suréchantillonné : l'AAC fait remonter les crêtes, on garde de la marge
ffmpeg -loglevel error -y -i audio.wav -af "aresample=192000,alimiter=limit=0.55:attack=1:release=60:level=false,aresample=48000" lim.wav
# loudnorm en 2 passes (mesure puis correction linéaire) : -14 LUFS, crête -1,5 dBTP
J=$(ffmpeg -nostats -i lim.wav -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
g(){ echo "$J" | python3 -c "import json,sys;print(json.load(sys.stdin)['$1'])"; }
AF="loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=$(g input_i):measured_TP=$(g input_tp):measured_LRA=$(g input_lra):measured_thresh=$(g input_thresh):offset=$(g target_offset):linear=true"
ffmpeg -loglevel error -y -i master.mp4 -i lim.wav -map 0:v -map 1:a -c:v libx264 -pix_fmt yuv420p -profile:v high -preset slow -crf 20 -threads 2 -af "$AF" -ar 48000 -c:a aac -b:a 192k -shortest -movflags +faststart reel.mp4
echo RENDER_OK
