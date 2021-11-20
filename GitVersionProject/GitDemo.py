import argparse
import collections
import configparser
import hashlib
import os
import sys
from typing import List


class GitRepository(object):
    """A git repository"""

    worktree = None
    gitdir = None
    logfile = None
    conf = None
    def __init__(self, path, force=False):
        self.worktree = path
        self.gitdir = os.path.join(path, ".git")
        self.logfile = os.path.join(self.gitdir, ".log")

def ExecInit(cmd: List[str], Repoobj: GitRepository):
    if not os.path.exists(Repoobj.gitdir):
        os.mkdir(Repoobj.gitdir)
    if not os.path.exists(Repoobj.logfile):
        open(Repoobj.logfile, 'w').close()
        

def main():
    print("Enter Input:")
    string = str(input())
    print(os.getcwd())

    gitRepo = GitRepository(os.getcwd())

    while(True):
        if len(string) > 0:
            print(string)
            print(gitRepo.gitdir)
            print(gitRepo.worktree)

            command = string.split(' ')
            if command[1] == 'init':
                ExecInit(command, gitRepo)
