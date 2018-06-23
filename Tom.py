from os import walk
import re

global master
master = {}

root = "C:/Users/titol/Documents/GitHub/intesys-tom/root/"
tom = "C:/Users/titol/Documents/GitHub/intesys-tom/Tom.out"



def search(keys, current_dir):
    files = []
    dirs = []

    # Store all directories and files from current directory into 2 lists
    for (dirpath, dirnames, filenames) in walk(current_dir):
        dirs.extend(dirnames)
        files.extend(filenames)
        for i in range(len(files)):
            files[i] = current_dir + files[i]
        break
    
    # Call search() for each found directory
    inner_files = []
    for d in dirs:
        search(keys, current_dir + d + "/")

    # Call tally() for each found file
    for f in files:
        k,v = tally(f, keys)
        master[k] = v


    
def tally(filename, keys):
    relevance = 0
    tokens = []

    # Tokenize the contents of the file
    with open(filename) as file:
        lines = [line.rstrip('\n') for line in file]
        for line in lines:
            tokens = splitter(line, ',', '.', ' ', '?', '!', '<', '>', '#', '{', '}', ';', '\t')
            tokens = [s.lower() for s in tokens]

            # For every keyword, increase relevance by 1
            for k in keys:
                if k in tokens:
                    relevance += 1

    # Greatly increase relevance if keyword is
    # found in filenames or parent folders
    sliced_dir = splitter(filename, '/', '.')
    for s in range(7, len(sliced_dir)):
        if sliced_dir[s].lower().startswith(key.lower()):
            relevance += 10*s
                
    return filename, relevance


# Tokenizer method
def splitter(string, *delimiters):
    pattern = '|'.join(map(re.escape, delimiters))
    return re.split(pattern, string)


# Print to console and write to file
def output(sorted_results):
    for v,k in sorted_results:
        if v != 0:
            print("%d\t: %s\n" % (v,k))
        
    with open(tom, 'w') as out:
        for v,k in sorted_results:
            if v != 0:
                out.write("%d\t: %s\n" % (v,k))


    
# User input (loop if empty str)
key = ''
while (key == ''):
    key = input("Search: ")

# Split key by spaces
keys = key.split(" ")
keys = [k.lower() for k in keys]

# Algo proper
search(keys, root)
sorted_results = sorted( ((v,k) for k,v in master.items()), reverse=True)
output(sorted_results)








