#!/bin/bash
bash ./extractmetadata.sh
bash ./extractwav.sh
python ./createvpy.py
python ./createvpymkv.py
bash ./encode.sh
exiftool -tagsfromfile %d%f.xmp -r -DateTimeOriginal -ext mp4 -overwrite_original .
rm **/*.wav **/*.vpy **/*.xmp **/*.ffindex
ln -s ~/Programs/git/dvdigitize/base.vpy ./
