# Scripts for working with DV files
Here is my collection of scripts I wrote while digitizing old NTSC minidv tapes. Below I've included
my workflow and other commands that I used.

I created a folder structure:
~/Videos/RawDV/TAPELABEL/dgrab-*

My tapes were nicely labeled. I took a picture of each tape, both front and side if applicable, and
added the images to the folder. I named these Label or Side.

### watch.py
I ran into issues dumping to my filesystem. I an error indicating a "buffer underrun". For some reason
my drive was too slow. I started dumping into RawDV/dump which I mounted to tmpfs with this command
`sudo mount tmpfs -t tmpfs -o gid=kristian -o uid=kristian ./dump`

To avoid my ram filling up I wrote watch.py which will move completed clips into a folder called next.
I soft linked whatever tapelabel folder to next by running a command like this:
`ln -s ../Disney2 ./next `

### Generating logs
I could not get dvgrab to output to stdout so I captured the log information with script. Before
starting dvgrab I would run `script ./next/log.txt`

### Warning on Failure
I had quite a few errors on the tapes I was working on and dvgrab crashed multiple times.
I adjusted my dvgrab command to run zenity with either an error message on failure or a success notice.
I made the error windows show up on top by adding a rule to kwin.

`dvgrab -s 0 -autosplit -t && zenity --info --text="capture complete" || zenity --error --text="capture failed"`

### stills.sh
My tapes had quite a few still images. These were ~32mb files with audio in the background. I made
a new folder called Pictures under any tape directory I found stills in. I manually moved the stills
into the Pictures folder, and then ran stills.sh. This will move ahead by 3 seconds. Moving forward
avoided corruption at the start of some of my stills. Then it pipes the frame to Magick to convert to
HEIC.

### Deinterlacing and createvpy.py
I decided to deinterlace with QTGMC. I used vapoursynth as my frameserver. Look at base.vpy for my
configuration file. Installing all of the packages took some effort even with my AUR helper on Archlinux.
[Arch Fourm Thread](https://bbs.archlinux.org/viewtopic.php?id=297627)
Vapoursynth expects a .vpy file which contains the name of the source to use. That means creating a vpy file
for each and every .dv.

### extractwav.sh
I did not get Vapoursynth to work with the audio in my DV files. By extracting the wav files I can add them
back when re-encoding.

### Dealing with Metadata.
I really wanted to preserve the timestamp for each file. By using exiftool I was able to copy the original
date and time into the new files. For the still images I ran this command:
`exiftool -tagsfromfile %d%f.dv -datetimeoriginal -ext HEIC -overwrite_original .`
I extracted the original date and time information for videos into a seperate file with this command
`exiftool -ext dv -o %d%f.xmp -r -DateTimeOriginal .`
That way I can delete the dv files as I got to keep track of what files have been encoded already.

### encode.sh
Finally, we encode using vapoursynth by running the vspipe command. I'm using BTRFS and made a reflink copy
of my dumped tapes, so this command **deletes the original** as it goes. You could easily modify this to delete
the vpy file, or not delete anything if you won't need to stop and start this command.

Also, don't take my ffmpeg flags too seriously. I'm pretty sure my -crf is too low and I am not an expert.

Hope this helps!
