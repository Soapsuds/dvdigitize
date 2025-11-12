import os
import subprocess
import pathlib
from pathlib import Path

# Read base file into a string
with open("base.vpy", "r") as f:
    basevpy = f.read()

# Find every .dv file
p = Path('.')
list = p.rglob('*.mkv')

# if I run this from digitizedv:
# f.parts[0] will be the folder name
# f.parts[1] will be the filename with extension

# Iterate through the list of DV files, and write a vpy file with the correct filename
for f in list:
    dir = str(f.parts[0])
    filename = str(f.parts[1])
    no_ext = filename.replace(".mkv", "")
    with open(dir + "/" + no_ext + ".vpy", "w") as vpyf:
        vpyf.write(basevpy.replace("REPLACE", filename))
