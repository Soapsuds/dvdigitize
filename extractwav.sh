#!/bin/bash
for filename in */*.dv; do
    [ -e "$filename" ] || continue
    ffmpeg -i "$filename" -map 0:a:0 -c:a copy "${filename%.*}".wav
done
