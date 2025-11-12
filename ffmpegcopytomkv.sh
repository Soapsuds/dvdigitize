#!/bin/bash
VIDEO="$(wl-paste)"

exiftool "$VIDEO" -o "${VIDEO%.*}".xmp
ffmpeg -i "$VIDEO" -c copy "${VIDEO%.*}".mkv
