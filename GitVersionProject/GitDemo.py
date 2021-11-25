import sys
from typing import List
import os  # for is_file(), is_dir(), abspath()
import pathlib  # for iterdir()
import hashlib  # for calculating sha256 digest
import shutil  # for copy()
import time  # for time()
from colorama import Fore
import difflib


class GitRepository(object):
    """A git repository"""

    def __init__(self, path, force=False):
        self.worktree = path
        self.gitdir = os.path.join(path, ".git")
        self.logfile = os.path.join(self.gitdir, "log.txt")
        self.gitRepoPath = os.path.join(self.gitdir, "Repository")
        self.trackedFilePath = os.path.join(self.gitdir, "trackedFile.txt")
        self.UntrackedFilePath = os.path.join(self.gitdir, "UntrackedFile.txt")
        self.indexFile = os.path.join(self.gitdir, "index.txt")
        self.workingDirectoryFiles = set()
        self.trackedFiles = set()
        self.modifiedFiles = set()
        self.index = {}
        self.trackingArea = {}
        self.commitHead = None
        self.worktree = None
        self.treeOfCommits = {}

    def writeToTxt(self):
        tracked_txt = open('./.git/trackedFile.txt', 'w')
        for file in self.trackedFiles:
            tracked_txt.write(str(file))
            tracked_txt.write("\n")

    def readFromTxt(self):
        tracked_txt = open('./.git/trackedFile.txt', 'r')
        for file in tracked_txt:
            path = pathlib.Path(os.path.abspath(file))
            self.trackedFiles.add(path)

    def shaOf(self, filename):
        sha256_hash = hashlib.sha256()
        with open(filename, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def addDir(self, path):
        for p in pathlib.Path(path).iterdir():
            if p.is_file() and p not in self.trackingArea:
                self.trackingArea[p] = self.shaOf(p)
                # tracking area -> json -> .txt
                self.trackedFiles.add(p)
                # tracked files -> json -> .txt
            elif ((p.is_dir()) & (not p.match("*/.git"))):
                self.addDir(p)

    def addFilesOfWorkingDirectory(self, path):
        absolutePath = pathlib.Path(os.path.abspath(path))
        for p in pathlib.Path(absolutePath).iterdir():
            if p.is_file():
                self.workingDirectoryFiles.add(p)
            elif ((p.is_dir()) & (not p.match("*/.git"))):
                self.addFilesOfWorkingDirectory(p)

    def gitAdd(self, p):
        # p is a list of arguments
        # .txt -> json -> tracking area
        # .txt -> tracked files
        for element in p:
            absolutePath = pathlib.Path(os.path.abspath(element))
            if absolutePath.is_file():
                self.trackingArea[absolutePath] = self.shaOf(element)
                # tracking area -> json -> .txt
                print("path -> ", absolutePath)
                self.trackedFiles.add(absolutePath)
                # tracked files -> .txt
            elif absolutePath.is_dir():
                self.addDir(absolutePath)
        self.writeToTxt()

    def gitStatus(self):
        self.workingDirectoryFiles.clear()
        self.modifiedFiles.clear()
        self.addFilesOfWorkingDirectory(".")

        temp = set()
        for i in self.trackingArea:
            temp.add(i)

        untrackedFiles = self.workingDirectoryFiles - temp

        cwd = pathlib.Path(os.path.abspath("."))
        position = len(str(cwd))

        if len(self.trackedFiles) != 0:
            print("\nAdded Files:")
            counter = 0
            for item in self.trackedFiles:
                path = str(item)[position+1:]
                print(str(counter+1) + "-> " + Fore.GREEN + path + Fore.WHITE)
                counter = counter+1

        if len(untrackedFiles) != 0:
            print("\nUntracked Files:")
            counter = 0
            for item in untrackedFiles:
                path = str(item)[position+1:]
                print(str(counter+1) + "-> " + Fore.RED + path + Fore.WHITE)
                counter = counter+1

        for i in self.trackingArea:
            if self.trackingArea[i] != self.shaOf(i):
                self.modifiedFiles.add(i)

        if len(self.modifiedFiles) != 0:
            print("\nModified Files:")
            counter = 0
            for item in self.modifiedFiles:
                path = str(item)[position+1:]
                print(str(counter+1) + "-> " + Fore.YELLOW + path + Fore.WHITE)
                counter = counter+1

    def getCommitId(self):
        t = str(time.time())
        t_encoded = t.encode("utf-8")
        soc = hashlib.sha256()
        soc.update(t_encoded)
        return soc.hexdigest()

    def getExtension(self, fileName):
        pos = str(fileName).rfind(".")
        extension = str(fileName)[pos:]
        return extension

    def ExecInit(self, cmd):
        if os.path.exists(self.gitdir):
            print("Git already initialised")
            sys.exit(0)
        if not os.path.exists(self.gitdir):
            os.mkdir(self.gitdir)
        if not os.path.exists(self.logfile):
            open(self.logfile, 'w').close()
        if not os.path.exists(self.trackedFilePath):
            open(self.trackedFilePath, 'w').close()
        if not os.path.exists(self.UntrackedFilePath):
            open(self.UntrackedFilePath, 'w').close()
        if not os.path.exists(self.indexFile):
            open(self.indexFile, 'w').close()
        if not os.path.exists(self.gitRepoPath):
            os.mkdir(self.gitRepoPath)

    def ExecCommit(self):
        if len(self.index) == 0:
            self.commitHead = None
        curr_commit_id = self.getCommitId()
        self.treeOfCommits[curr_commit_id] = self.commitHead  # Parent Commit
        self.index[curr_commit_id] = {}
        for fileName in self.trackingArea:
            self.index[curr_commit_id][fileName] = self.shaOf(fileName)
            if (self.trackingArea[fileName] is None) or (self.index.get(self.treeOfCommits.get(curr_commit_id, {}), {}).get('fileName') != self.index[curr_commit_id][fileName]):
                # need to ponder
                self.trackingArea[fileName] = self.index[curr_commit_id][fileName]
                extension = self.getExtension(fileName)
                dest = self.gitRepoPath + "\\" + \
                    self.index[curr_commit_id][fileName] + extension
                shutil.copy(fileName, dest)
        self.commitHead = curr_commit_id
        self.trackedFiles.clear()
        self.modifiedFiles.clear()

    def printDifference (self, file1, file2):
        f1 = open(file1).readlines
        f2 = open(file2).readlines

        delta = difflib.unified_diff(f1, f2)
        sys.stdout.writelines(delta)

    def diff(self, c1, c2):
        c1_files = self.index[c1]
        c2_files = self.index[c2]

        addedFiles = set()
        deletedFiles = set()

        print("Modified files")
        for file in c1_files:
            if file in c2_files and c2_files[file] != c1_files[file]:
                ex = self.getExtension(file)
                print(file)
                self.printDifference(c1_files[file]+ex, c2_files[file]+ex)
            elif file not in c2_files:
                addedFiles.add(file)

        if len(addedFiles) != 0:
            print("Added Files")
        for f in addedFiles:
            print(f)

        for file in c2_files:
            if file not in c1_files:
                deletedFiles.add(file)

        if len(deletedFiles) != 0:
            print("Deleted Files")
        for f in deletedFiles:
            print(f)


def main():
    # print(os.getcwd())

    Gitobj = GitRepository(os.getcwd())
    if os.path.exists(Gitobj.gitdir):
        Gitobj.readFromTxt()

    command = sys.argv
    if len(command) > 0:
        if command[1] == 'init':
            Gitobj.ExecInit(command)
        elif command[1] == 'add':
            argument = command[2:]
            Gitobj.gitAdd(argument)
        elif command[1] == 'status':
            Gitobj.gitStatus()
        elif command[1] == 'commit':
            Gitobj.ExecCommit()
        elif command[1] == 'diff':
            if len(command) == 2:
                Gitobj.diff(Gitobj.commitHead, Gitobj.treeOfCommits[Gitobj.commitHead])
            elif len(command) == 4:
                Gitobj.diff(command[2], command[3])
    else:
        sys.exit(0)

    Gitobj.writeToTxt()

if __name__ == '__main__':
    main()