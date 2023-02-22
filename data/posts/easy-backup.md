---
title: "Easy Backup"
date: "2021-09-05"
categories: 
  - "tips"
  - "tutorial"
---

While storage media has vastly improved in reliability, that doesn't mean your data is safe. If you've paid attention to technology news, even from a high level, there are plenty of horror stories of people losing data, especially to ransomware. But even if you are on a low-risk platform or in a low-risk environment, things can happen, so you should have your data on a regular backup schedule.

While there are probably plenty of good backup tools out there, you don't need anything fancy. Whether you're on Linux or Windows, a simple script will do the trick. In this post, I'm going to share the scripts I use on my machines.

What's special about these scripts is they do not do full backups, except for the first time. They do incremental backups, meaning they only backup stuff that's changed since the last backup. They also do a mirror copy, with the source (your computer) being the master copy. That way, provided you do regular backups, the backup will exactly mirror your computer.

### Backing up Linux

On Linux, we will use a tool called RSync. In my experience, RSync comes preinstalled on most if not all common distros, so no extra step is required. You could do one command that backups up the whole home folder, but then you will backup a ton of extra settings and application-specific gunk. Its up to you, but I wouldn't recommend it.

The command we use is:

```
rsync -av --delete $HOME/Documents $BACKUP
```

The "-a" flag stands for "archive mode", which is a shorthand for a bunch of other flags- one of them being the very import recursive flag, which copies all sub files and sub folders. The "-v" stands for "verbose". Just me, but I like to see what's going on. The "--delete" is used to mirror the destination (the backup) with the source; it means that anything in the backup folder that is not on your computer gets deleted.

Here is my full script:

```
#!/bin/bash
BACKUP="/run/media/patrick/Backup/xps-dev-main"
if [[ ! -d $BACKUP ]] ; then
    mkdir $BACKUP
fi
rsync -av --delete $HOME/Arduino $BACKUP
rsync -av --delete $HOME/Desktop $BACKUP
rsync -av --delete $HOME/Documents $BACKUP
rsync -av --delete $HOME/Downloads $BACKUP
rsync -av --delete $HOME/scripts $BACKUP
rsync -av --delete $HOME/.ssh $BACKUP/ssh
echo "Done"
```

### Backing up Windows

Backing up Windows is a similar process with a similar command. In this case, however, we use Robocopy instead of Rsync. Once again, in my experience robocopy is pre-installed on recent versions of Windows.

Here is the command we use. A very good explanation of the flags (if you're interested) can be found at this link: [https://superuser.com/questions/814102/robocopy-command-to-do-an-incremental-backup](https://superuser.com/questions/814102/robocopy-command-to-do-an-incremental-backup)

```
robocopy C:\Users\patrick\Documents D:\laptop\Documents /MIR /FFT /R:3 /W:10 /Z /NP /NDL
```

And, here is my full script. Notice the "pause" at the bottom. On Windows, you can double-click a batch script, and it will open the command prompt for you, which is nice. But it will close it automatically when its done. This is not a good idea in case there are any errors. The "pause" command will keep the command prompt open until you hit a key.

```
@echo off
echo "Beginning backup..."
robocopy C:\Users\patrick\Archive D:\laptop\Archive /MIR /FFT /R:3 /W:10 /Z /NP /NDL
robocopy C:\Users\patrick\Desktop D:\laptop\Desktop /MIR /FFT /R:3 /W:10 /Z /NP /NDL
robocopy C:\Users\patrick\Documents D:\laptop\Documents /MIR /FFT /R:3 /W:10 /Z /NP /NDL
robocopy C:\Users\patrick\Downloads D:\laptop\Downloads /MIR /FFT /R:3 /W:10 /Z /NP /NDL
robocopy C:\Users\patrick\Music D:\laptop\Music /MIR /FFT /R:3 /W:10 /Z /NP /NDL
robocopy "C:\Users\patrick\Project Archive" "D:\laptop\Project Archive" /MIR /FFT /R:3 /W:10 /Z /NP /NDL
robocopy C:\Users\patrick\Pictures D:\laptop\Pictures /MIR /FFT /R:3 /W:10 /Z /NP /NDL
echo "Done"
pause
```

### Conclusion

Hopefully you found this post useful. Stay safe, and stay backed up.


