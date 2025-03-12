#!/bin/bash
for filename in */*.dv; do
    [ -e "$filename" ] || continue
    vspipe -c y4m "${filename%.*}".vpy - | ffmpeg -i - -i "${filename%.*}".wav -c:v libx265 -preset slow -crf 18 -pix_fmt yuv420p -tag:v hvc1 -tune grain "${filename%.*}".mp4
    rm "$filename"
done
