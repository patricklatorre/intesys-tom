from os import walk
import re

global debug
debug = False


def gather(current_dir):
    files = []
    dirs = []

    # Store all dirs and files from current dir into dirs[] and files[]
    for (dirpath, dirnames, filenames) in walk(current_dir):
        dirs.extend(dirnames)
        files.extend(filenames)
        for i in range(len(files)):
            files[i] = current_dir + files[i]
        break
    
    # Call gather in all found folders
    inner_files = []
    for d in dirs:
        inner_files.extend(gather(current_dir + d + "/"))

    # Append child dir's files to current dir's files
    files.extend(inner_files)
    
    return files



def tally(filename, keys):
    count = 0
    tokens = []
    
    with open(filename) as file:
        lines = [line.rstrip('\n') for line in file]
        for line in lines:
            tokens = splitter(line, ',', '.', ' ', '?', '!', '<', '>', '#', '{', '}', ';', '\t')
            tokens = [s.lower() for s in tokens]

            for k in keys:
                if k in tokens:
                    count += 1

    sliced_dir = splitter(filename, '/', '.')
    for s in range(7, len(sliced_dir)):
        if sliced_dir[s].lower().startswith(key.lower()):
            count += 10*s
                
    return filename, count



def crawl(all_files):
    results = {}
    for file in all_files:
        k,v = tally(file, keys)
        results[k] = v
    return results



def splitter(string, *delimiters):
    pattern = '|'.join(map(re.escape, delimiters))
    return re.split(pattern, string)





root = "D:/Toby/root/"
toby = "D:/Toby/Toby.out"

key = ''
while (key == ''):
    key = input("Search: ")

keys = key.split(" ")
keys = [k.lower() for k in keys]


# if key == '///': break
    
all_files = gather(root)
results = crawl(all_files)

sorted_r = sorted( ((v,k) for k,v in results.items()), reverse=True)

for v,k in sorted_r:
    if v != 0:
        print("%d\t: %s\n" % (v,k))
        
with open(toby, 'w') as out:
    for v,k in sorted_r:
        if v != 0:
            out.write("%d\t: %s\n" % (v,k))





