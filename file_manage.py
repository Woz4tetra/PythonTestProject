
import send2trash
import shutil
import os
import string
import re



def rename(dry_run):
    #printable = set(string.printable)
    os.chdir("/Users/Woz4tetra/Music/iTunes/iTunes Media/Music/Unknown Artist/Breath of the Wild Soundtrack")

    for item in os.listdir():
        if item.endswith(".mp3"):
            print(item, end=" ---> ")
            match = re.match(r"(?P<junk>.+) - (?P<name>.+)", item)
            new_name = match.group("name")
            
            print(new_name)
            if not dry_run:
                shutil.move(item, new_name + ".mp3")

#            end_index = item.rfind(".")
#            start_index = item.find(" ", len("GaMetal - GaMetal V - ")) + 1
#            new_name = item[start_index:end_index] + ".mp3"
#            new_name = ''.join(filter(lambda x: x in printable, new_name))
#            print(repr(new_name))


rename(False)
