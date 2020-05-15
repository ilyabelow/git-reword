# Git Reword

This tool allows you to quickly reword the latest commits. The usual way to do it is to use `git rebase --interactive`, which is really slow on big repos. This tool only edits meta information of commits

#### Usage:

In a directory of a repo to edit:

> git-reword &lt;commit&gt; &lt;message&gt; ...

Enter as much commit-message pairs as you need

#### Example:

![https://imgur.com/OGIQ5os.png](https://imgur.com/OGIQ5os.png)

#### Limitations:

The script assumes that all requested commits are in one line (starting from HEAD) with no other refs or commits pointing to it. If there were other refs or commits, they would point to old versions of reworded commits. So use this tool to only reword commit on local topic branches with no other branches based on it.


## Installation

One way is to add the project directory to `PATH` with

> export PATH=$(pwd):$PATH

for bash or with

> set PATH (pwd) $PATH

for fish.

Another way is to create a symbolic link to the script in a PATH directory of your choice:

> cd ~/.local/bin
> ln -s path/to/script/git-reword.py git-reword

## Requirements

You have to install `pygit2`:

> pip install pygit2 --user


