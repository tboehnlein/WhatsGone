# Overview
Everyone should backup their files. But they don't at all. Or don't do it often enough. Or don't have enough storage to do a backup. Tons of reasons. So what that happens and all of a sudden your E:\ drive is gone. The first question you ask is "What's gone?" Well this won't bring your files back, but you can at least know what you lost.

WizTree is a wonderful program that let's you see all of the files on your drive within seconds. Luckily, the software has a command line interface to read the drive and spit out a list of files. So instead of actually looking for everything on your drive file by file for many minutes or an hour or whatever, it's done in seconds.

This is the perfect software to use to archive a list of your files no matter how big the drive is.

## Operation
If the drive is there, it will make a record of all of the files that match the filter patterns with their paths into a text file.

If a drive is missing, a timestamped message will be recorded in a file so it is known when it is missing.

If the drive has nothing in it, it will not overwrite an existing file.

The output directory should obviously be on a different drive otherwise what's the point? 🤣

## Setup
Python script should be run through Windows Task Scheduler with highest privelages to make it run on a schedule and to get rid of the WizTree UAC pop up.

It needs admin rights to work because of how it reads everything so quickly using the file table directly. 

## Helpful Links
[WizTree Download Page](https://diskanalyzer.com/download)

[WizTree Command Line Arguments Page](https://diskanalyzer.com/guide#cmdlinecsv)

[Task Scheduler Tutorial](https://www.digitalcitizen.life/advanced-users-task-creation-task-scheduler/)
