
import os
import re
import glob
from eyed3 import mp3
from pprint import pprint

# use python 2.7
# command: youtube-dl --download-archive downloaded.txt --no-post-overwrites -ciwx --extract-audio --audio-format mp3 -o "%(autonumber)s %(title)s.%(ext)s" [url]
# navigate to OUTPUT TEMPLATE section of the man page for youtube-dl for all templates
os.chdir("/Users/Woz4tetra/Downloads/playlist")
audiofiles = glob.glob("*.mp3") + glob.glob("*.m4a") + glob.glob("*.flac") 

dry_run = False

for file_name in audiofiles:
    match = re.match(r"(\d*) ([\s\S]*) - [\s\S]*\.mp3", file_name)
    if match is not None:
        track_num = int(match.group(1))
        new_name = match.group(2)
        
        mp3_file = mp3.Mp3AudioFile(file_name)
        mp3_file.initTag()
        mp3_file.tag.track_num = (track_num, len(audiofiles))
        mp3_file.tag.album = u"Super Mario Odyssey Soundtrack"
        
        if not dry_run:
            mp3_file.tag.save()
            
            mp3_file.rename(unicode(new_name, 'utf-8'))
        print("%s ---> %s" % (file_name, new_name))
            
