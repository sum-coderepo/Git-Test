import os        #for is_file(), is_dir(), abspath()
import pathlib   #for iterdir()
import hashlib   #for calculating sha256 digest
import shutil    #for copy()

stagingArea = {}
index = {}

def shaOf (filename):
    sha256_hash = hashlib.sha256()
    with open(filename,"rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096),b""):
            sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()


def addDir (path):
    for p in pathlib.Path(path).iterdir():
        if p.is_file():         #and staginArea[p] not present
            stagingArea[p] = None
            print(p,":",stagingArea[p])
        elif p.is_dir():
            addDir (p)

def gitAdd (p):
    absolutePath = pathlib.Path(os.path.abspath(p))
    if absolutePath.is_file():
        stagingArea[absolutePath] = None
    elif absolutePath.is_dir():
        addDir (absolutePath)

gitAdd(".")
#addDir("C:\\Users\\mmdwi\\OneDrive\\Desktop\\Gargi Documents")

#def gitCommit ():
#    for fileName in stagingArea:
#        if stagingArea[fileName] 
        
