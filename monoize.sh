#!/bin/bash
for filename in ./*.mp4; do
    [ -e "$filename" ] || continue
    ffmpeg -i "$filename" -c:v copy -af "pan=stereo|c0<c0+c1|c1<c0+c1" "./out/${filename}"
done
