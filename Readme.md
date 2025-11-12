# Scripts for working with DV files
Here is my collection of scripts I wrote while digitizing old NTSC minidv tapes. Below I've included
my workflow and other commands that I used.

I created a folder structure:
~/Videos/RawDV/TAPELABEL/dgrab-*

My tapes were nicely labeled. I took a picture of each tape, both front and side if applicable, and
added the images to the folder. I named these Label or Side.

### Dumping with dvgrab
dvgrab tended to crash occasionally, especially when encountering issues on the tapes. It is still the best tool
for the job. I dumped with this command
```dvgrab -s 7168 -autosplit -t && zenity --info --text="capture complete" || zenity --error --text="capture failed"```
I then added some window rules in KDE to make Zenity appear on top of any other window so I would immediately see when
a capture needed to be restarted. -s 7168 is because I was dumping to ram and needed to make sure I wouldn't
trigger the Out Of Memory killer even if I was gaming at the same time.
#### about -t
The -t flag tells dvgrab to dump with the timestamps of the file. Unfortunately, some files got corrupt
or didn't have a date set on the camera. Older versions of dvgrab would silently overwrite these files.
Make sure you are running a version of dvgrab with the commit linked in this [issue](https://github.com/ddennedy/dvgrab/pull/17)
Sadly, my ramdisk dumping interfered with this fix, so watch.py also appends a number to the end of the file extension.
This kinda sucks, but worked well enough for me. If you don't get any buffer underruns when dumping with
dvgrab then don't do the tmpfs part.

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
into the Pictures folder, and then ran stills.sh. The command pipes the frame from ffmpeg to Magick to convert to
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

### Manually Cutting Video
I'm used to cutting video with mpv using the [mpv-cut](https://github.com/familyfriendlymikey/mpv-cut).
Unfortunately this did not work with some of my dv files. For whatever reason some of my files were 32000 Hz
audio which ffmpeg fails to copy with the folowing error:
`[dv @ 0x5579dedc7980] Invalid sample rate 32000 for audio stream #0 for this video profile, must be 48000.
[dv @ 0x5579dedc7980] Can't initialize DV format!`
In order to cut these I just remux to God's gift Matroska which as far as I can tell will take any video format
with any audio format. Once muxed into an mkv mpv-cut works like normal. Many of my clips were corrupt or had 1
frame of a pervious scene at the start of the file. See ```ffmpegcopytomkv.sh```. It's an easy command but by
saving it to a script I was able to invoke with with a hotkey on KDE.

### Dealing with Metadata.
I really wanted to preserve the timestamp for each file. By using exiftool I was able to copy the original
date and time into the new files. For the still images I ran this command:
`exiftool -tagsfromfile %d%f.dv -datetimeoriginal -ext HEIC -overwrite_original .`
I extracted the original date and time information for videos into a seperate file with this command
`exiftool -ext dv -o %d%f.xmp -r -DateTimeOriginal .`
That way I can delete the dv files as I go to keep track of what files have been encoded already.

### encode.sh
Finally, we encode using vapoursynth by running the vspipe command. I'm using BTRFS and made a reflink copy
of my dumped tapes, so this command **deletes the original** as it goes. You could easily modify this to delete
the vpy file, or not delete anything if you won't need to stop and rerun this command.

Also, don't take my ffmpeg flags too seriously. I personally found that settings -threads to /2 my core count -2
ran faster as vspipe can get starved for cycles. I'm pretty sure my -crf is too low and I am not an expert.

## runencode.sh
Once I got comfortable using all this and trusting that it would work correctly I put everything together into runencode.sh.
I moved all of the video files into subfolders and linked all of the scripts and base.vpy into the top level folder.


Hope this helps!
