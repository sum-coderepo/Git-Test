import os        #for is_file(), is_dir(), abspath()
import pathlib   #for iterdir()

trackingArea = {}   #for now
untrackedFiles = set() #for now

def addDir (path):
    for p in pathlib.Path(path).iterdir():
        if p.is_file() and p not in trackingArea:
            trackingArea[p] = None
            print(p,":",trackingArea[p])
        elif p.is_dir():
            addDir (p)

def addDirToUntrackedFiles (path):
    absolutePath = pathlib.Path(os.path.abspath(path))
    for p in pathlib.Path(absolutePath).iterdir():
        if p.is_file():
            untrackedFiles.add(p)
        elif p.is_dir():
            addDirToUntrackedFiles (p)

def gitAdd (p):
    addDirToUntrackedFiles(".")
    #split p
    #for element in p
        # absolutePath = pathlib.Path(os.path.abspath(p))
        # if absolutePath.is_file():
        #     trackingArea[absolutePath] = None
        # elif absolutePath.is_dir():
        #     addDir (absolutePath)

gitAdd("ksjf")
print(untrackedFiles)