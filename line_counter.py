
import os
import sys
import traceback

def count_file(filename, directory):
    with open(os.path.join(directory, filename), 'rb') as file_ref:
        try:
            return file_ref.read().decode('utf-8').count("\n")
        except UnicodeDecodeError:
            print("Error in file:", filename)
            traceback.print_exc()
            sys.exit()

def count_lines(directory, ignore_dirs=None, ignore_files=None):
    print()
    print(os.path.abspath(directory))
    if ignore_dirs is None:
        ignore_dirs = []
    if ignore_files is None:
        ignore_files = []
    total_line_count = 0
    file_count = 0
    for dirpath, dirnames, filenames in os.walk(os.path.abspath(directory)):
        if dirpath.split("/")[-1] not in ignore_dirs:
            for filename in filenames:
                if filename not in ignore_files:
                    if filename.endswith(".py"):
                        line_count = count_file(filename, dirpath)
                        total_line_count += line_count
                        file_count += 1
                        print("%s: %s" % (filename, line_count))
                
    return total_line_count, file_count
    
#print("\ntotal: %s, count: %s" % count_lines("/Users/Woz4tetra/Documents/Atlas/roboquasar", ["vision"], ["kalman_filter.py"]))
print("\ntotal: %s, count: %s" % count_lines("/Users/Woz4tetra/Documents/Code/Atlasbuggy/atlasbuggy", ignore_files=["janus.py"]))

