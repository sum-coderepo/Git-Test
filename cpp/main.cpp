#include <bits/stdc++.h>
#include <iostream>
#include <fcntl.h>
#include <stdio.h>
#include <math.h>
#include <grp.h>
#include <pwd.h>
#include <time.h>
#include <dirent.h>
#include <termios.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/ioctl.h>

using namespace std;

typedef long long ll;
typedef vector<int> vi;
typedef vector<ll> vll;
typedef vector<string> vs;
typedef vector<bool> vb;
typedef vector<vi> vvi;
typedef stack<int> si;
typedef pair<int, int> pii;
typedef pair<long long, long long> pll;
typedef vector<pii> vpii;
typedef vector<pll> vpll;

//GLOBAL_Declarations----------------------------------------------------------------------------------------------------------------------------//

//----------------------------------------------------------------------------------------------------------------------------//

//Utilities----------------------------------------------------------------------------------------------------------------------------//
int check_command(string command);
void list_commands(void);
void error_git_dir(void);
//----------------------------------------------------------------------------------------------------------------------------//

//Commands----------------------------------------------------------------------------------------------------------------------------//
int init(void);
int add(vs);
//----------------------------------------------------------------------------------------------------------------------------//

int check_command(string input)
{
    if (input == "init") //initialise the git directory
        return 1;

    else if (input == "add") //
        return 2;

    else if (input == "status") //
        return 3;

    else if (input == "commit") //
        return 4;

    else if (input == "rollback") //
        return 5;

    else if (input == "diff") //
        return 6;

    else if (input == "log") //
        return 7;

    else if (input == "retrieve") //
        return 8;

    else if (input == "push") //
        return 9;

    else if (input == "push") //
        return 10;

    else if (input == "merge") //
        return 11;

    else
        return 0;
}

void list_commands(void)
{
    cout << "\nList of available commands:\n"
         << "1. init\n"
         << "2. add\n"
         << "3. status\n"
         << "4. commit\n"
         << "5. rollback\n"
         << "6. diff\n"
         << "7. log\n"
         << "8. push\n"
         << "9. pull\n"
         << "10. merge\n";
    exit(0);
}

void error_git_dir(void)
{
    cout << "Error : Git folder couldn't be initialised.\n";
    exit(0);
}

int init(void)
{
    char cur_dir[1024];
    getcwd(cur_dir, 1024);
    string path(cur_dir);

    //checking if it already exists
    string git_dir = path + "/" + ".git_dir";
    if (filesystem::exists(git_dir))
    {
        cout << "\".git_dir\" directory already exists.\n";
        exit(0);
        return 0;
    }

    //making .git_dir folder in current path
    int check = mkdir(".git_dir", 0777);

    if (check == -1)
        error_git_dir();

    //creating the directory tree of git folder
    check = chdir(".git_dir");
    if (check == -1)
        error_git_dir();

    //creating required folders inside git_dir
    if (mkdir("versions", 0777) == -1)
        error_git_dir();

    if (mkdir("logs", 0777) == -1)
        error_git_dir();

    if (mkdir("info", 0777) == -1)
        error_git_dir();

    if (mkdir("objects", 0777) == -1)
        error_git_dir();

    //creating version_0
    string version_0 = git_dir + "/versions";

    check = chdir(version_0.c_str());
    if (check == -1)
        error_git_dir();

    if (mkdir("ver_0", 0777) == -1)
        error_git_dir();

    //copying all files to ver_0 folder for initialisation

    return 1;
}

int add(vs list_files)
{
    char cur_dir[1024];
    getcwd(cur_dir, 1024);
    string path(cur_dir);

    int counter{1};
    for (auto i : list_files)
    {
        cout << counter++ << ".) " << path << "/" << i << endl;
    }

    return 1;
}

int main(int argc, char *argv[])
{
    //checking for command line arguments
    if (argc < 2)
    {
        cout << "<<-- Invalid count of parameters -->>\nTry again with proper command.\n";
        list_commands();
        exit(0);
    }

    //handling command line arguments
    string command = "";
    command = argv[1];

    int cases = check_command(command);

    //Dealing with all given possible commands
    int dir_init,
        added;
    switch (cases)
    {
    case 0:
        cout << "<<-- Invalid command -->>\nTry again with proper command.\n";
        list_commands();
        break;

    case 1: //init
        // cout << "Command is : ./git init" << endl;
        dir_init = init();

        if (dir_init == 1)
        {
            cout << " \".git_dir\" has  been created.\n"
                 << "Proceed with other commands now.\n";
        }
        else
            error_git_dir();

        break;

    case 2: //add
        // cout << "Command is : ./git add" << endl;

        if (argc == 2)
        {
            cout << "ADD Command requires name(s) of file(s) to be added.\nTry Again..\n";
            exit(0);
        }

        vs files_to_add;

        for (int i = 2; i < argc; i++)
        {
            string file_name = argv[i];
            files_to_add.push_back(file_name);
        }

        added = add(files_to_add);

        break;
    }

    return 0;
}