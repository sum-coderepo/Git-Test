import os
import sys
import time
import json
import shutil
import pathlib
import hashlib
import difflib
import datetime
from typing import List
from colorama import Fore


class GitRepository(object):
    """A git repository"""

    def __init__(self, path, force=False):
        self.gitdir = os.path.join(path, ".git")
        self.logfile = os.path.join(self.gitdir, "log.txt")
        self.gitRepoPath = os.path.join(self.gitdir, "Repository")
        self.trackedFilePath = os.path.join(self.gitdir, "trackedFile.txt")
        self.commitHeadPath = os.path.join(self.gitdir, "commitHead.txt")
        self.trackingAreaPath = os.path.join(self.gitdir, "trackingArea.json")
        self.treeOfCommitsPath = os.path.join(
            self.gitdir, "treeOfCommits.json")
        self.indexFilePath = os.path.join(self.gitdir, "index.json")
        self.workingDirectoryFiles = set()
        self.modifiedFiles = set()
        self.trackedFiles = set()
        self.treeOfCommits = {}
        self.trackingArea = {}
        self.index = {}
        self.commitHead = None
        self.RemoteRepo = "C:\\Users\\sumeet\\Desktop\\PGSSP_2019-22_IIIT\\Monsoon 2021\\Adv OS\\Final Project\\Remote\\"

    # writing from data structures into the files in .git folder

    def writeToTxt_tf(self):
        tracked_txt = open('./.git/trackedFile.txt', 'w')
        for file in self.trackedFiles:
            line = str(file) + "\n"
            tracked_txt.write(line)

    def writeToTxt_ch(self):
        tracked_txt = open('./.git/commitHead.txt', 'w')
        if self.commitHead is None:
            to_write = "None"
        else:
            to_write = str(self.commitHead)

        tracked_txt.write(to_write)

    def writeToJson_ta(self):
        tracking_json = open('./.git/trackingArea.json', 'w')
        temp = {}
        for item in self.trackingArea:
            temp[str(item)] = self.trackingArea[item]
        json.dump(temp, tracking_json)

    def writeToJson_toc(self):
        toc_json = open('./.git/treeOfCommits.json', 'w')
        temp = {}
        for item in self.treeOfCommits:
            temp[str(item)] = self.treeOfCommits[item]
        json.dump(temp, toc_json)

    def writeToJson_index(self):
        index_json = open('./.git/index.json', 'w')
        json.dump(self.index, index_json)


    # reading from files into data structures from .git folder


    def readFromTxt_tf(self):
        self.trackedFiles.clear()
        tracked_txt = open('./.git/trackedFile.txt', 'r')
        for file in tracked_txt:
            path = pathlib.Path(os.path.relpath(file))
            self.trackedFiles.add(path)

    def readFromTxt_ch(self):
        tracked_txt = open('./.git/commitHead.txt', 'r')
        self.commitHead = tracked_txt.read()

    def readFromJson_ta(self):
        tracking_json = open('./.git/trackingArea.json', 'r')
        self.trackingArea = json.load(tracking_json)

    def readFromJson_toc(self):
        toc_json = open('./.git/treeOfCommits.json', 'r')
        self.treeOfCommits = json.load(toc_json)

    def raedFromJson_index(self):
        index_json = open('./.git/index.json', 'r')
        self.index = json.load(index_json)


    # utility functions


    def shaOf(self, filename):
        sha256_hash = hashlib.sha256()
        with open(filename, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def delFilesOfWorkingDirectory(self, path):
        relative = pathlib.Path(os.path.relpath(path))
        for p in pathlib.Path(relative).iterdir():
            if p.is_file():
                os.remove(p)
            elif p.is_dir():
                self.delFilesOfWorkingDirectory(p)
                os.rmdir(p)

    # git_INIT

    def ExecInit(self, cmd):
        if os.path.exists(self.gitdir):
            print("\n<<-- Git Directory has been ALREADY initialised -->>\n")
            sys.exit(0)

        if not os.path.exists(self.gitdir):
            os.mkdir(self.gitdir)

        if not os.path.exists(self.logfile):
            open(self.logfile, 'w').close()

        if not os.path.exists(self.trackedFilePath):
            open(self.trackedFilePath, 'w').close()

        if not os.path.exists(self.commitHeadPath):
            open(self.commitHeadPath, 'w').close()

        if not os.path.exists(self.treeOfCommitsPath):
            open(self.treeOfCommitsPath, 'w').close()

        if not os.path.exists(self.indexFilePath):
            open(self.indexFilePath, 'w').close()

        if not os.path.exists(self.trackingAreaPath):
            open(self.trackingAreaPath, 'w').close()

        if not os.path.exists(self.gitRepoPath):
            os.mkdir(self.gitRepoPath)


    # git_ADD

    def addDir(self, path):
        for p in pathlib.Path(path).iterdir():
            if p.is_file() and p not in self.trackingArea:
                self.trackingArea[p] = self.shaOf(p)
                self.trackedFiles.add(p)
            elif ((p.is_dir()) & (not p.match("*/.git"))):
                self.addDir(p)

    def gitAdd(self, p):
        # p is a list of arguments
        for element in p:
            # print(" ->", element)
            relative = pathlib.Path(os.path.relpath(element))
            print("relative path : ", relative)
            if relative.is_file():
                self.trackingArea[relative] = self.shaOf(element)
                self.trackedFiles.add(relative)
            elif relative.is_dir():
                for k in list(self.trackingArea.keys()): # To Handle if file is deleted
                        if k.startswith(element): # To Handle if file is deleted
                            del self.trackingArea[k] # To Handle if file is deleted
                self.addDir(relative)


    # git_STATUS

    def addFilesOfWorkingDirectory(self, path):
        relative = pathlib.Path(os.path.relpath(path))
        for p in pathlib.Path(relative).iterdir():
            if p.is_file():
                self.workingDirectoryFiles.add(p)
            elif ((p.is_dir()) & (not p.match(".git"))):
                self.addFilesOfWorkingDirectory(p)

    def gitStatus(self):
        self.workingDirectoryFiles.clear()
        self.modifiedFiles.clear()
        self.addFilesOfWorkingDirectory(".")

        temp = set()
        temp2 = set()
        untrackedFiles = set()

        for i in self.workingDirectoryFiles:
            temp.add(str(i))

        for i in self.trackingArea:
            temp2.add(str(i))

        untrackedFiles = temp.difference(temp2)

        cwd = pathlib.Path(os.path.abspath("."))
        position = len(str(cwd))

        if len(self.trackedFiles) != 0:
            print("\nAdded Files:")
            counter = 0
            for item in self.trackedFiles:
                print(str(counter+1) + "-> " + Fore.GREEN + str(item) + Fore.WHITE)
                counter = counter+1

        if len(untrackedFiles) != 0:
            print("\nUntracked Files:")
            counter = 0
            for item in untrackedFiles:
                #path = str(item)[position+1:]
                print(str(counter+1) + "-> " +
                      Fore.RED + str(item) + Fore.WHITE + "\n")
                counter = counter+1

        for i in self.trackingArea:
            if self.trackingArea[i] != self.shaOf(i):
                self.modifiedFiles.add(i)

        if len(self.modifiedFiles) != 0:
            print("\nModified Files:")
            counter = 0
            for item in self.modifiedFiles:
                #path = str(item)[position+1:]
                print(str(counter+1) + "-> " + Fore.YELLOW + str(item) + Fore.WHITE)
                counter = counter+1


    # git_COMMIT

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

    def ExecCommit(self, msg):
        if len(self.index) == 0:
            self.commitHead = None

        curr_commit_id = self.getCommitId()
        # if no changes then why commit..?

        self.treeOfCommits[curr_commit_id] = self.commitHead  # Parent Commit
        self.index[curr_commit_id] = {}

        for fileName in self.trackingArea:
            self.index[curr_commit_id][fileName] = self.shaOf(fileName)
            if (self.trackingArea[fileName] is None) or (self.index.get(self.treeOfCommits.get(curr_commit_id, {}), {}).get('fileName') != self.index[curr_commit_id][fileName]):
                # need to ponder
                self.trackingArea[fileName] = self.index[curr_commit_id][fileName]
                extension = self.getExtension(fileName)
                dest = self.gitRepoPath + "/" + \
                       self.index[curr_commit_id][fileName] + extension
                # print('destination path : ', dest)
                shutil.copy(fileName, dest)

        self.commitHead = curr_commit_id
        # updating logs
        log_txt = open('./.git/log.txt', 'r+')
        commit_id = str(self.commitHead)
        if commit_id == "None":
            commit_id = "Initial Commit"
        to_write = "Commit ID : " + commit_id + "\n"
        to_write += "Commit Message : " + str(msg) + "\n"
        time = datetime.datetime.now()
        to_write += "Date : " + str(time.strftime("%c")) + "\n\n"
        prev_log = log_txt.read()
        log_txt.seek(0, 0)
        log_txt.write(to_write.rstrip('\r\n') + '\n' + prev_log)

        self.trackedFiles.clear()
        self.modifiedFiles.clear()


    # git_DIFF

    # def printDifference(self, file1, file2):
    #     f1 = open(file1).readlines
    #     f2 = open(file2).readlines

    #     delta = difflib.unified_diff(f1, f2)
    #     sys.stdout.writelines(str(delta))


    def printDifference(self, x1, x2):
        # Open File in Read Mode
        file_1 = open(x1, 'r')
        file_2 = open(x2, 'r')

        file_1_line = file_1.readline()
        file_2_line = file_2.readline()

        # Use as a Counter
        line_no = 1

        print("Difference Lines in Both Files")
        while file_1_line != '' or file_2_line != '':

            # Removing whitespaces
            file_1_line = file_1_line.rstrip()
            file_2_line = file_2_line.rstrip()

            # Compare the lines from both file
            if file_1_line != file_2_line:

                # otherwise output the line on file1 and use @ sign
                if file_1_line == '':
                    print("@", "Line-%d" % line_no, file_1_line)
                else:
                    print("@-", "Line-%d" % line_no, file_1_line)

                # otherwise output the line on file2 and use # sign
                if file_2_line == '':
                    print("#", "Line-%d" % line_no, file_2_line)
                else:
                    print("#+", "Line-%d" % line_no, file_2_line)

                # Print a empty line
                print()

            # Read the next line from the file
            file_1_line = file_1.readline()
            file_2_line = file_2.readline()

            line_no += 1

        file_1.close()
        file_2.close()

    def diff(self, c1, c2):
        c1_files = self.index[c1]
        c2_files = self.index[c2]

        addedFiles = set()
        deletedFiles = set()

        print("Modified files : \n ")
        for file in c1_files:
            if file in c2_files and c2_files[file] != c1_files[file]:
                ex = self.getExtension(file)
                # print(file)
                f1 = './.git/Repository/'+c1_files[file]+ex
                f2 = './.git/Repository/'+c2_files[file]+ex
                self.printDifference(f1, f2)
            elif file not in c2_files:
                addedFiles.add(file)

        if len(addedFiles) != 0:
            print("Added Files : \n")
        for f in addedFiles:
            print(f)

        for file in c2_files:
            if file not in c1_files:
                deletedFiles.add(file)

        if len(deletedFiles) != 0:
            print("Deleted Files : \n")
        for f in deletedFiles:
            print(f)


    # git_LOG

    def log(self):
        log_txt = open('./.git/log.txt', 'r')
        counter = 0
        for line in log_txt:
            if(counter % 3 == 0):
                print("")
                print(Fore.YELLOW + line + Fore.WHITE, end="")
            else:
                print(line, end="")
            counter += 1
            # formatting is needed


    # git_CHECKOUT

    def rollback1(self):
        if self.treeOfCommits[self.commitHead] is not None:
            for key, value in self.index[self.treeOfCommits[self.commitHead]].items():
                if (self.trackingArea[key] != value):

                    source = self.gitRepoPath + "//" + \
                             value + "." + key.split(".")[-1]
                    fileName = key.split("\\")[-1]
                    print(key, " ", value)
                    print(
                        "Following files moved from commit {0} Successfully.".format(fileName))
                    shutil.copy(source, key)
                    print(fileName)
                    self.trackingArea[key] = value

            print("Commit head shifted from {0} to {1}".format(
                self.commitHead, self.treeOfCommits[self.commitHead]))
            self.commitHead = self.treeOfCommits[self.commitHead]

        else:
            print("Cannot roll back. Possible reason is you have only one commit")
            sys.exit(0)

    def checkout(self, commitID):

        if self.index[commitID] is not None:
            usr_input = ""
            d1_keys = set(self.trackingArea.keys())
            d2_keys = set(self.index[commitID].keys())
            # These files were added if the checkout is previous commit and will be removed.
            Files_Added = d1_keys - d2_keys
            # These files are not present in the current commit. If the checkout is a later commit and will be added.
            Files_Removed = d2_keys - d1_keys

            shared_keys = d1_keys.intersection(d2_keys)
            modified = {o: (self.trackingArea[o], self.index[commitID][o])
                        for o in shared_keys if self.trackingArea[o] != self.index[commitID][o]}
            if len(Files_Added) > 0:
                print("File Removal Alert!!\n")
                print(
                    "Following file(s) were added after the checkout and will be removed.")
                print(
                    "Press 'Y' to continue and 'N' to not remove the files from the current working directory")
                print(Files_Added)

                usr_input = str(input())
                if usr_input == "Y":
                    for file in Files_Added:
                        if os.path.exists(file):
                            os.remove(file)
                            del self.trackingArea[file]
                else:
                    print(" Files not removed from the current working directory")

            if len(modified) > 0:
                print("File Modification Alert!!")
                print(
                    "Following files were modified after the checkout. Press 'Y' to continue and 'N' to ignore")
                print(list(modified.keys()))

                usr_input = str(input())
                if usr_input == "Y":
                    for key, value in self.index[commitID].items():
                        if key in modified:
                            source = self.gitRepoPath + "//" + \
                                     value + "." + key.split(".")[-1]
                            fileName = key.split("\\")[-1]
                            print(key, " ", value)
                            print(
                                "Following files moved from commit {0} Successfully.".format(key))
                            shutil.copy(source, key)
                            print(key)
                            self.trackingArea[key] = value
                else:
                    print("Above modified files are not moved to the working directory")

            if len(Files_Removed) > 0:
                print("File Addition Alert!!")
                print(
                    "Following files are not part of the current commit and will be added after the checkout. Press 'Y' to continue")
                print(list(Files_Removed))

                usr_input = str(input())
                if usr_input == "Y":
                    for key, value in self.index[commitID].items():
                        if key in Files_Removed:
                            source = self.gitRepoPath + "//" + \
                                     value + "." + key.split(".")[-1]
                            fileName = key.split("\\")[-1]
                            print(key, " ", value)
                            print(
                                "Following files moved from commit {0} Successfully.".format(key))
                            shutil.copy(source, key)
                            print(key)
                            self.trackingArea[key] = value
                else:
                    print("Above Added files are not moved to the working directory")

            self.commitHead = commitID

        else:
            print("Cannot roll back. Possible reason is you have only one commit")
            sys.exit(0)


    # git_ROLLBACK

    def rollback(self):
        self.checkout(self.treeOfCommits[self.commitHead])

    # git_PUSH

    def push1(self):
        root_workingDir = os.getcwd().split('\\')[-1]
        print(root_workingDir)
        RemoteDir = os.path.join(self.RemoteRepo, root_workingDir)
        # print("Remote Path->", RemoteDir)
        if os.path.exists(RemoteDir):
            # delete existing dir recursively
            self.delFilesOfWorkingDirectory(RemoteDir)
            os.rmdir(RemoteDir)
        os.mkdir(RemoteDir)
        if self.commitHead is not None:
            for key, value in self.index[self.commitHead].items():

                FilePath = RemoteDir + "\\" + key
                directory = os.path.dirname(FilePath)
                os.makedirs(directory, exist_ok=True)
                source = self.gitRepoPath + "/" +  value + "." + key.split(".")[-1]
                # print("source -> ", source)
                shutil.copy(source, FilePath)

        git_folder = self.gitdir

        from distutils.dir_util import copy_tree
        copy_tree(git_folder, RemoteDir + "/.git")


    def push(self):

        root_workingDir = os.getcwd().split('\\')[-1]
        print(root_workingDir)
        RemoteDir = os.path.join(self.RemoteRepo, root_workingDir)

        if not os.path.exists(RemoteDir):
            os.mkdir(RemoteDir)
            os.mkdir(RemoteDir + '/.git/')
            os.mkdir(RemoteDir + '/.git/Repository')


        if os.path.exists(RemoteDir + '\\.git\\commitHead.txt'):
            FilecommitHead = open(RemoteDir + '\\.git\\commitHead.txt')
            RemotecommitHead = FilecommitHead.read()
        else:
            RemotecommitHead = ""
            FilecommitHead =  None


        if os.path.exists(RemoteDir + '/.git/treeOfCommits.json'):
            Remotetoc_json = open(RemoteDir + '/.git/treeOfCommits.json', 'r')
            RemotetreeOfCommits = json.load(Remotetoc_json)

        else:
            RemotetreeOfCommits = {}
            Remotetoc_json = None


        if os.path.exists(RemoteDir + '/.git/index.json'):
            index_json = open(RemoteDir + '/.git/index.json', 'r')
            Remoteindex = json.load(index_json)

        else:
            Remoteindex = {}
            index_json = None

        NewKeysRemote  = Remoteindex.keys() - self.index.keys()

        if len(NewKeysRemote) > 0:
            print("You are {0} commits behind the remote. Cannot push your changes. First do pull to get the latest changes from Remote.".format(len(NewKeysRemote)))
            print("New Commits : ", NewKeysRemote)
            print("Press Y to do a git pull")
            usr_input = str(input())
            if usr_input == 'Y':
                self.pull()
                self.push()
            else:
                sys.exit(0)
        else:
            d1_keys = set(self.trackingArea.keys())
            if RemotecommitHead != "":
                d2_keys = set(Remoteindex[RemotecommitHead].keys())
            else:
                d2_keys = set()


            try:
                file_names = os.listdir(self.gitRepoPath)
                for file in file_names:
                    shutil.copy2( os.path.join(self.gitRepoPath, file) ,   RemoteDir + '/.git/Repository' )
            except Exception as e:
                print("An exception occurred: ", e)

            Files_Added = d1_keys - d2_keys #Files Added in the local repo but not present in remote.
            Files_Removed = d2_keys - d1_keys #Files present in the Remote but not present in local.
            shared_keys = d1_keys.intersection(d2_keys)

            modified = {o: (self.trackingArea[o], Remoteindex[RemotecommitHead][o])
                        for o in shared_keys if self.trackingArea[o] != Remoteindex[RemotecommitHead][o]}

            if len(Files_Added) > 0:
                print("File Addition Alert!!\n")
                print(
                    "Following file(s) are not present in the remote and will be added in the push.")
                print(
                    "Press 'Y' to continue and 'N' to make the changes in the remote")
                print(Files_Added)
                usr_input = str(input())
                if usr_input == "Y":
                    for key, value in self.index[self.commitHead].items():
                        if key in Files_Added:
                            source = self.gitRepoPath + "//" +  value + "." + key.split(".")[-1]
                            print(key, " ", value)
                            os.makedirs(os.path.dirname(RemoteDir + "//" + key), exist_ok=True)
                            shutil.copy(source, RemoteDir + "//" + key)
                            print(key)
                            print(
                                "Following files Were added in the remote Successfully.".format(key))
                else:
                    print("Above Added files are not moved to the working directory")


            if len(modified) > 0:
                print("File Modification Alert!!")
                print(
                    "Following files were modified after the push. Press 'Y' to continue and 'N' to ignore")
                print(list(modified.keys()))
                usr_input = str(input())
                if usr_input == "Y":
                    for key, value in self.index[self.commitHead].items():
                        if key in modified:
                            source = self.gitRepoPath + "//" + value + "." + key.split(".")[-1]
                            fileName = key.split("\\")[-1]
                            print(key, " ", value)
                            shutil.copy(source, RemoteDir + "//" + key)
                            print(
                                "Following files moved from commit {0} Successfully.".format(key))
                else:
                    print("Above modified files are not moved to the working directory")

            if len(Files_Removed) > 0:
                print("File Removal Alert!!")
                print(
                    "Following files is not part of the current commit and will be deleted from the remote. Press 'Y' to continue")
                print(list(Files_Removed))
                usr_input = str(input())
                if usr_input == "Y":
                    for file in Files_Removed:
                        if os.path.exists(RemoteDir + "//" + file):
                            os.remove(RemoteDir + "//" + file)
                else:
                    print(" Files not removed from the current working directory")

            newCommits =  self.index.keys() -  Remoteindex.keys()
            for key in newCommits:
                Remoteindex[key] = self.index[key]
                RemotetreeOfCommits[key] = self.treeOfCommits[key]

            NewRemotecommitHead = self.commitHead
            if FilecommitHead:
                FilecommitHead.close()
            if index_json:
                index_json.close()
            if Remotetoc_json:
                Remotetoc_json.close()

            f1 = open(RemoteDir + '\\.git\\commitHead.txt', 'w+')
            f1.write(NewRemotecommitHead)
            f1.close()


            index_json_ow = open(RemoteDir + '/.git/index.json', 'w+')
            json.dump(Remoteindex, index_json_ow)
            index_json_ow.close()

            Remotetoc_json_ow = open(RemoteDir + '/.git/treeOfCommits.json', 'w+')
            json.dump(RemotetreeOfCommits, Remotetoc_json_ow)
            Remotetoc_json_ow.close()

            trackingArea_json_ow = open(RemoteDir + '/.git/trackingArea.json', 'w+')
            json.dump(Remoteindex[NewRemotecommitHead], trackingArea_json_ow)
            trackingArea_json_ow.close()






    def pull(self):


        root_workingDir = os.getcwd().split('\\')[-1]
        print(root_workingDir)
        RemoteDir = os.path.join(self.RemoteRepo, root_workingDir)

        RemotecommitHead = open(RemoteDir + '/.git/commitHead.txt', 'r').read()

        Remotetoc_json = open(RemoteDir + '/.git/treeOfCommits.json', 'r')
        RemotetreeOfCommits = json.load(Remotetoc_json)

        index_json = open(RemoteDir + '/.git/index.json', 'r')
        Remoteindex = json.load(index_json)


        d1_keys = set(self.trackingArea.keys())
        d2_keys = set(Remoteindex[RemotecommitHead].keys() )

        try:
            file_names = os.listdir(RemoteDir + '/.git/Repository')
            for file in file_names:
                shutil.copy2(os.path.join(RemoteDir + '/.git/Repository',file), self.gitRepoPath)
        except Exception as e:
            print("An exception occurred: ", e)


        print(Remoteindex.keys() - self.index.keys() , " New commits are identified")

        Files_Added = d1_keys - d2_keys #Files Added in the local repo but not present in remote
        Files_Removed = d2_keys - d1_keys
        shared_keys = d1_keys.intersection(d2_keys)

        modified = {o: (self.trackingArea[o], Remoteindex[RemotecommitHead][o])
                    for o in shared_keys if self.trackingArea[o] != Remoteindex[RemotecommitHead][o]}

        if len(Files_Added) > 0:
            print("File Removal Alert!!\n")
            print(
                "Following file(s) were Removed from the Remote repo after your last push and will be removed from your local working directory.")
            print(
                "Press 'Y' to continue and 'N' to not remove the files from the current working directory")
            print(Files_Added)
            usr_input = str(input())
            if usr_input == "Y":
                for file in Files_Added:
                    if os.path.exists(file):
                        os.remove(file)
                        del self.trackingArea[file]
            else:
                print(" Files not removed from the current working directory")

        if len(modified) > 0:
            print("File Modification Alert!!")
            print(
                "Following files were modified after the checkout. Press 'Y' to continue and 'N' to ignore")
            print(list(modified.keys()))
            usr_input = str(input())
            if usr_input == "Y":
                for key, value in Remoteindex[RemotecommitHead].items():
                    if key in modified:
                        source = self.gitRepoPath + "//" + value + "." + key.split(".")[-1]
                        fileName = key.split("\\")[-1]
                        print(key, " ", value)
                        print(
                            "Following files moved from commit {0} Successfully.".format(key))
                        shutil.copy(source, key)
                        print(key)
                        self.trackingArea[key] = value
            else:
                print("Above modified files are not moved to the working directory")

        if len(Files_Removed) > 0:
            print("File Addition Alert!!")
            print(
                "Following files are not part of the current Repository and will be added after the pull. Press 'Y' to continue")
            print(list(Files_Removed))

            usr_input = str(input())
            if usr_input == "Y":
                for key, value in Remoteindex[RemotecommitHead].items():
                    if key in Files_Removed:
                        source = self.gitRepoPath + "//" +  value + "." + key.split(".")[-1]
                        fileName = key.split("\\")[-1]
                        print(key, " ", value)
                        print(
                            "Following files moved from commit {0} Successfully.".format(key))
                        if str(os.path.dirname(key))  != "":
                            os.makedirs(os.path.dirname(key), exist_ok=True)
                        shutil.copy(source, key)
                        print(
                            "Following files moved from commit {0} Successfully.".format(key))
                        print(key)
                        self.trackingArea[key] = value
            else:
                print("Above Added files are not moved to the working directory")


        newCommits = Remoteindex.keys() - self.index.keys()  #New commits
        if len(newCommits) > 0:
            for key in newCommits:
                self.index[key] = Remoteindex[key]
                self.treeOfCommits[key] = RemotetreeOfCommits[key]

        self.commitHead = RemotecommitHead



# git_PULL


def main():

    Gitobj = GitRepository(os.getcwd())

    print("Enter Input:")

    string = str(input())

    while(True):
        if len(string) > 0:

            if os.path.exists(Gitobj.gitdir):
                Gitobj.readFromTxt_ch()
                Gitobj.readFromTxt_tf()
                Gitobj.readFromJson_ta()
                Gitobj.readFromJson_toc()
                Gitobj.raedFromJson_index()

            command = string.split(' ')  # sys.argv

            if len(command) > 0:
                if command[1] == 'init':
                    Gitobj.ExecInit(command)
                    print("\n<<-- Git Directory has been initialised -->>\n")

                elif command[1] == 'add':
                    if len(command) == 2:
                        argument = ["."]
                    else:
                        argument = command[2:]
                    Gitobj.gitAdd(argument)
                    print("\n<<-- Given file(s) have been added to Staging Area -->>\n")

                elif command[1] == 'status':
                    Gitobj.gitStatus()
                    print("\n<<-- Current Status -->>\n")

                elif command[1] == 'commit':
                    message = input("Type some commit message : ")
                    Gitobj.ExecCommit(message)
                    print("\n<<-- Changes have been committed -->>\n")

                elif command[1] == 'diff':
                    if len(command) == 2:
                        if Gitobj.commitHead != None and Gitobj.treeOfCommits[Gitobj.commitHead] != None:
                            Gitobj.diff(Gitobj.commitHead,
                                        Gitobj.treeOfCommits[Gitobj.commitHead])
                    elif len(command) == 4:
                        Gitobj.diff(command[2], command[3])

                elif command[1] == 'log':
                    Gitobj.log()
                    print("\n<<-- End of Logs -->>\n")

                elif command[1] == 'rollback':
                    Gitobj.rollback()
                    print("\n<<-- End of Logs -->>\n")

                elif command[1] == 'checkout':
                    Gitobj.checkout(command[2])
                    print("\n<<-- End of Logs -->>\n")

                elif command[1] == 'push':
                    Gitobj.push()
                    print("\n<<-- Commit pushed to remote-->>\n")

                elif command[1] == 'pull':
                    Gitobj.pull()
                    print("\n<<-- Pull Operation Complete-->>\n")

            else:
                sys.exit(0)

            Gitobj.writeToTxt_ch()
            Gitobj.writeToTxt_tf()
            Gitobj.writeToJson_ta()
            Gitobj.writeToJson_toc()
            Gitobj.writeToJson_index()

            string = str(input())


            print("")


if __name__ == '__main__':
    main()
