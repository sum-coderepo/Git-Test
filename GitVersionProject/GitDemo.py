import argparse
import collections
import configparser
import sys
from typing import List
import os  # for is_file(), is_dir(), abspath()
import pathlib  # for iterdir()
import hashlib  # for calculating sha256 digest
import shutil  # for copy()
import time  # for time()
from colorama import Fore


class GitRepository(object):
    """A git repository"""

    def __init__(self, path, force=False):
        self.worktree = path
        self.gitdir = os.path.join(path, ".git")
        self.logfile = os.path.join(self.gitdir, ".log")
        self.gitRepoPath = os.path.join(self.gitdir, "Repository")
        self.trackedFilePath = os.path.join(self.gitdir, "trackedFile.txt")
        self.UntrackedFilePath = os.path.join(self.gitdir, "UntrackedFile.txt")
        self.trackedFiles = set()
        self.trackingArea = {}
        self.modifiedFiles = set()
        self.indexFile = os.path.join(self.gitdir, ".index")
        self.index = {}
        self.commitHead = None
        self.untrackedFiles = set()
        self.worktree = None
        self.treeOfCommits = {}

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
                self.trackedFiles.add(p)
                self.untrackedFiles.remove(p)
            elif ((p.is_dir()) & (not p.match("*/.git"))):
                self.addDir(p)

    def addDirToUntrackedFiles(self, path):
        absolutePath = pathlib.Path(os.path.abspath(path))
        for p in pathlib.Path(absolutePath).iterdir():
            if ((p.is_file()) & (p not in self.trackedFiles)):
                self.untrackedFiles.add(p)
            elif ((p.is_dir()) & (not p.match("*/.git"))):
                self.addDirToUntrackedFiles(p)

    def gitAdd(self, p):
        path = p[2]
        self.addDirToUntrackedFiles(".")

        absolutePath = pathlib.Path(os.path.abspath(path))
        if absolutePath.is_file():
            self.trackingArea[absolutePath] = self.shaOf(path)
            self.trackedFiles.add(absolutePath)
            self.untrackedFiles.remove(absolutePath)
        elif absolutePath.is_dir():
            self.addDir(absolutePath)

    def gitStatus(self):
        cwd = pathlib.Path(os.path.abspath("."))
        position = len(str(cwd))

        print("\nAdded Files:")
        counter = 0
        for item in self.trackedFiles:
            path = str(item)[position+1:]
            print(str(counter+1) + "-> " + Fore.GREEN + path + Fore.WHITE)
            counter = counter+1

        print("\nUntracked Files:")
        counter = 0
        for item in self.untrackedFiles:
            path = str(item)[position+1:]
            print(str(counter+1) + "-> " + Fore.RED + path + Fore.WHITE)
            counter = counter+1

        for i in self.trackingArea:
            if self.trackingArea[i] != self.shaOf(i):
                self.modifiedFiles.add(i)

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
            if (self.trackingArea[fileName] is None) or (self.index.get(self.treeOfCommits.get(curr_commit_id, {}), {}).get('fileName') != self.trackingArea[fileName]):
                self.trackingArea[fileName] = self.index[curr_commit_id][fileName]
                extension = self.getExtension(fileName)
                dest = self.gitRepoPath + "\\" + \
                    self.index[curr_commit_id][fileName] + extension
                shutil.copy(fileName, dest)
        self.commitHead = curr_commit_id


def main():
    print("Enter Input:")
    string = str(input())
    print(os.getcwd())

    Gitobj = GitRepository(os.getcwd())

    while(True):
        if len(string) > 0:
            print(string)
            print(Gitobj.gitdir)

            command = string.split(' ')
            if command[1] == 'init':
                Gitobj.ExecInit(command)
            elif command[1] == 'add':
                Gitobj.gitAdd(command)
            elif command[1] == 'status':
                Gitobj.gitStatus()
            elif command[1] == 'commit':
                Gitobj.ExecCommit()

            string = str(input())

        else:
            sys.exit(0)


if __name__ == '__main__':
    main()
