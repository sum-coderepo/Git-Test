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

    #worktree = None
    #gitdir = None
    #logfile = None
    #index = None
    #trackingArea = {}
    #untrackedFiles = set()
    #modifiedFiles = set()
    #trackedFiles = set()
    #index = {}
    #commitHead = None
    #treeOfCommits = {}

    def __init__(self, path, force=False):
        self.worktree = path
        self.gitdir = os.path.join(path, ".git")
        self.logfile = os.path.join(self.gitdir, ".log")
        self.trackedFiles = set()
        self.trackingArea = {}
        self.modifiedFiles = set()
        self.index = {}
        self.commitHead = None
        self.treeOfCommits = {}
        self.worktree = None
        self.treeOfCommits = {}




    @classmethod
    def shaOf(filename, self):
        sha256_hash = hashlib.sha256()
        with open(filename, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    @classmethod
    def addDir(path, self):
        for p in pathlib.Path(path).iterdir():
            if p.is_file() and p not in self.trackingArea:
                self.trackingArea[p] = self.shaOf(p)
                self.trackedFiles.add(p)
                self.untrackedFiles.remove(p)
            elif p.is_dir():
                self.addDir(p)



    @classmethod
    def addDirToUntrackedFiles(path, self):
        absolutePath = pathlib.Path(os.path.abspath(path))
        for p in pathlib.Path(absolutePath).iterdir():
            if p.is_file():
                    self.untrackedFiles.add(p)
            elif p.is_dir():
                self.addDirToUntrackedFiles(p)

    @classmethod
    def gitAdd(p, self):
        self.addDirToUntrackedFiles(".")
        for element in p:
            absolutePath = pathlib.Path(os.path.abspath(element))
            if absolutePath.is_file():
                self.trackingArea[absolutePath] = self.shaOf(element)
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

        path1 = pathlib.Path(os.path.abspath(
            "/Users/ashishchauhan/Desktop/Code_it/AOS/Project/demo.txt"))
        self.trackingArea[path1] = "dddas"

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


    def getExtension( self, fileName):
        pos = fileName.rfind(".")
        extension = fileName[pos:]
        # handle no extension
        return extension

    @classmethod
    def ExecInit(self, cmd):
        if not os.path.exists(self.gitdir):
            os.mkdir(self.gitdir)
        if not os.path.exists(self.logfile):
            open(self.logfile, 'w').close()
            

    def addDir1(path, self):
        for p in pathlib.Path(path).iterdir():
            if p.is_file() and p not in self.trackingArea:
                self.trackingArea[p] = self.shaOf(p)
                self.trackedFiles.add(p)
                self.untrackedFiles.remove(p)
            elif p.is_dir():
                self.addDir(p)


def main():
    print("Enter Input:")
    string = str(input())
    print(os.getcwd())

    Gitobj = GitRepository(os.getcwd())

    Gitobj.gitStatus()


    while(True):
        if len(string) > 0:
            print(string)
            print(Gitobj.gitdir)
            print(Gitobj.worktree)

            command = string.split(' ')
            if command[1] == 'init':
                Gitobj.ExecInit(command)

            string = str(input())

        else:
            sys.exit(0)


if __name__ == '__main__':
    main()
