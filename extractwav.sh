#!/bin/bash
for filename in */*.dv; do
    [ -e "$filename" ] || continue
    ffmpeg -i "$filename" -map 0:a:0 -c:a copy "${filename%.*}".wav
done

# I've been using MKV to trim files, run those through too
for filename in */*.mkv; do
    [ -e "$filename" ] || continue
    ffmpeg -i "$filename" -map 0:a:0 -c:a copy "${filename%.*}".wav
done
