import os        #for is_file(), is_dir(), abspath()
import pathlib   #for iterdir()
import hashlib   #for calculating sha256 digest
import shutil    #for copy()
import time      #for time()

trackingArea = {}   #for now
index = {}          #for now
commitHead = None   #for now
treeOfCommits = {}  #for now

def shaOf (filename):
    sha256_hash = hashlib.sha256()
    with open(filename,"rb") as f:
        for byte_block in iter(lambda: f.read(4096),b""):
            sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

def addDir (path):
    for p in pathlib.Path(path).iterdir():
        if p.is_file() and p not in trackingArea:
            trackingArea[p] = None
            print(p,":",trackingArea[p])
        elif p.is_dir():
            addDir (p)

def gitAdd (p):
    absolutePath = pathlib.Path(os.path.abspath(p))
    if absolutePath.is_file():
        trackingArea[absolutePath] = None
    elif absolutePath.is_dir():
        addDir (absolutePath)

#gitAdd(".")
gitAdd("C:\\Users\\mmdwi\\OneDrive\\Desktop\\Gargi Documents")
gitRepoPath = "C:\\Users\\mmdwi\\OneDrive\\Desktop\\Gargi Documents\\.git\\"

def getCommitId ():
    t = str(time.time())
    t_encoded = t.encode("utf-8")
    soc = hashlib.sha256()
    soc.update(t_encoded)
    return soc.hexdigest()

def getExtension (fileName):
    pos = fileName.rfind(".")
    extension = fileName[pos:]
    #handle no extension
    return extension

def gitCommit ():
    curr_commit_id = getCommitId ()
    treeOfCommits[curr_commit_id] = commitHead
    commitHead = curr_commit_id
    index[curr_commit_id] = {}
    for fileName in trackingArea:
        index[curr_commit_id][fileName] = shaOf (fileName)
        if ((trackingArea[fileName] == None) or (index[curr_commit_id][fileName] != trackingArea[fileName])):
            trackingArea[fileName] = index[curr_commit_id][fileName]
            getExtension (fileName) #add new file to repo
            dest = gitRepoPath + index[curr_commit_id][fileName] + extension
            shutil.copy(fileName, dest)
            

            
