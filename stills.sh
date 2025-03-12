#!/bin/bash
for filename in ./*.dv; do
    [ -e "$filename" ] || continue
    ffmpeg -ss 3 -i "$filename" -frames:v 1 -update 1 -c:v pam -f image2 - | magick - "${filename%.*}".heic
done
exiftool -tagsfromfile %d%f.dv -datetimeoriginal -ext HEIC -overwrite_original .
