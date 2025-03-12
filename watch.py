import os
import shutil
import pyinotify

# The watch manager stores the watches and provides operations on watches
wm = pyinotify.WatchManager()

mask = pyinotify.IN_CLOSE_WRITE # watched events, IN_CLOSE_NOWRITE means file was written and is now closed

class EventHandler(pyinotify.ProcessEvent):
    count = 0
    namelist = []
    def process_IN_CLOSE_WRITE(self, event):
        EventHandler.count += 1
        if event.name in EventHandler.namelist:
            shutil.move("./" + event.name, "./next/" + event.name + str(EventHandler.count))
        else:
            shutil.move("./" + event.name, "./next/" + event.name)
        EventHandler.namelist.append(event.name)

handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)
wdd = wm.add_watch('./', mask)

notifier.loop()
