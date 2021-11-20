import os  # for is_file(), is_dir(), abspath()
import pathlib  # for iterdir()
import hashlib  # for calculating sha256 digest
import shutil  # for copy()
import time  # for time()
from colorama import Fore

trackingArea = {}       # for now
untrackedFiles = set()  # for now
trackedFiles = set()    # for now
modifiedFiles = set()    # for now
index = {}              # for now
commitHead = None       # for now
treeOfCommits = {}      # for now


# while adding files to trackingArea at the time of git add, strike them out from this set


def shaOf(filename):
    sha256_hash = hashlib.sha256()
    with open(filename, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()


def addDir(path):
    for p in pathlib.Path(path).iterdir():
        if p.is_file() and p not in trackingArea:
            trackingArea[p] = shaOf(p)
            trackedFiles.add(p)
            untrackedFiles.remove(p)
        elif p.is_dir():
            addDir(p)


def addDirToUntrackedFiles(path):
    absolutePath = pathlib.Path(os.path.abspath(path))
    for p in pathlib.Path(absolutePath).iterdir():
        if p.is_file():
            untrackedFiles.add(p)
        elif p.is_dir():
            addDirToUntrackedFiles(p)


def gitAdd(p):
    # p is a list of arguments
    addDirToUntrackedFiles(".")
    for element in p:
        absolutePath = pathlib.Path(os.path.abspath(element))
        if absolutePath.is_file():
            trackingArea[absolutePath] = shaOf(element)
            trackedFiles.add(absolutePath)
            untrackedFiles.remove(absolutePath)
        elif absolutePath.is_dir():
            addDir(absolutePath)


def gitStatus():
    cwd = pathlib.Path(os.path.abspath("."))
    position = len(str(cwd))

    print("\nAdded Files:")
    counter = 0
    for item in trackedFiles:
        path = str(item)[position+1:]
        print(str(counter+1) + "-> " + Fore.GREEN + path + Fore.WHITE)
        counter = counter+1

    print("\nUntracked Files:")
    counter = 0
    for item in untrackedFiles:
        path = str(item)[position+1:]
        print(str(counter+1) + "-> " + Fore.RED + path + Fore.WHITE)
        counter = counter+1

    # temp solution as hash is not stored loacally
    # create temporary path as per your local directory
    path1 = pathlib.Path(os.path.abspath(
        "/Users/ashishchauhan/Desktop/Code_it/AOS/Project/demo.txt"))
    trackingArea[path1] = "dddas"

    for i in trackingArea:
        if trackingArea[i] != shaOf(i):
            modifiedFiles.add(i)

    print("\nModified Files:")
    counter = 0
    for item in modifiedFiles:
        path = str(item)[position+1:]
        print(str(counter+1) + "-> " + Fore.YELLOW + path + Fore.WHITE)
        counter = counter+1


# gitAdd(".")
p = {"demo.txt", "flow.jpeg", "demo"}  # as per the local directory
gitAdd(p)

print("\nTrackning Area : \n")
for item in trackingArea:
    print(trackingArea[item], "-> " + str(item))


gitStatus()


def getCommitId():
    t = str(time.time())
    t_encoded = t.encode("utf-8")
    soc = hashlib.sha256()
    soc.update(t_encoded)
    return soc.hexdigest()


def getExtension(fileName):
    pos = fileName.rfind(".")
    extension = fileName[pos:]
    # handle no extension
    return extension

# def gitCommit():
#     curr_commit_id = getCommitId()
#     treeOfCommits[curr_commit_id] = commitHead
#     commitHead = curr_commit_id
#     index[curr_commit_id] = {}
#     for fileName in trackingArea:
#         index[curr_commit_id][fileName] = shaOf(fileName)
#         if ((trackingArea[fileName] == None) or (index[curr_commit_id][fileName] != trackingArea[fileName])):
#             trackingArea[fileName] = index[curr_commit_id][fileName]
#             extension = getExtension(fileName)  # add new file to repo
#             dest = gitRepoPath + index[curr_commit_id][fileName] + extension
#             shutil.copy(fileName, dest)
