---
title: "Reinstalling Grub on Linux Mint"
date: "2022-03-09"
categories: 
  - "linux"
  - "tips"
  - "tutorial"
---

The title of this post is the nice way of saying "How to fix your computer after committing an act of stupidness."

So my day started out with me trying to boot up my Dell Inspirion laptop, only for it to go into the hardware diagnostics (and please note: it literally worked perfectly 8 hours earlier). After the laptop said all the hardware was good and giving the foghorn-like beep to prove it, I poked around the EFI menu (F12 on Dell computers), and found that the entire entry just disappeared. After consultation with the internet, I got it fixed.

I'm actually really happy about this because 9/10 times, if the computer breaks (and its rare for Linux to break), I just reinstall. But since this had important stuff on it, I really didn't want to get into that.

## Prerequisites

You will need a LiveCD/USB, ideally with either Linux Mint or Ubuntu. I used Mint just in case I had to reinstall everything, but most Linux distros should work. I also only did this on a screwed-up Linux Mint system. Most Linux distros should work the same way, but test at your own risk. Ubuntu and Debian systems definitely should work with this method.

Disclaimer: Do this at your own risk. But chances are if you are here, you can't screw it up much more :)

Boot up the LiveCD, and make sure you are in EFI mode:

```
ls /sys/firmware/efi
```

If there are files in that folder, you are good to continue.

## Step 1: Mount

In this tutorial, I'm assuming you have 3 partitions:

```
- /dev/sda1 -> the EFI partition
- /dev/sda2 -> the boot partition
- /dev/sda3 -> The LUKS-encrypted system partition
```

If you don't have disk encryption enabled and don't have other operating systems on your device, your table may look like this:

```
- /dev/sda1 -> the EFI partition
- /dev/sda2 -> the system partition
```

Please note that I'm assuming you have the encrypted partition layout. If you don't, adjust the commands accordingly. ALSO: run all commands as root, either with "sudo" or by entering root mode with "su root".

If you have the encrypted main partition, run these commands first. **Important:** the "lvdisplay" command will display which device your main partition is. Replace the "mount" command with the appropriate output from lvdisplay.

```
cryptsetup luksOpen /dev/sda3 crypt
lvdisplay
mount /dev/mintvg/root /mnt
```

Now mount the boot partitions:

```
mount /dev/sda2 /mnt/boot
mount /dev/sda1 /mnt/boot/efi
```

And now mount any other virtual filesystems. Copy-and-paste this if you are able, but if not, **copy it exactly**.

```
for i in /dev /dev/pts /proc /sys /sys/firmware/efi/efivars /run; do sudo mount -B $i /mnt$i; done
```

Now, "chroot" into your system.

```
chroot /mnt
```

At this point, the shell should look a little different. On my system, the user became "root@mint". Note that you are in a root shell now, so it is not necessary to preface the last two commands with "sudo". These commands will reinstall grub. For the first command, note that you are not providing a partition number- just the disk name.

```
grub-install /dev/sda
update-grub
```

Note that the "update-grub" command may give you a warning; this is because it noticed your LiveCD, didn't know what to do with it, and just skipped. This is normal. The first command should not give you any errors.

## If this fails...

If your system is still broken after following these steps, you're probably just better off reinstalling. You can still use these steps to copy your files off the encrypted partition if needed. I would imagine that most GUI file managers in the LiveCDs can open an encrypted partition (provided you have the password of course), but if not the commands above will work.

## Conclusion & Sources

While I mainly wrote this for my future reference, hopefully someone out there finds this helpful. For the curious, I have no idea what triggered this. The last thing I did was run some updates, which included a kernel update, so that may have triggered it. I was doing something with grub yesterday, but I don't remember actually triggering anything... oh well, it seems to be fixed.

Remember to keep things backed up!

Many thanks to these sources:

- [https://wiki.debian.org/GrubEFIReinstall](https://wiki.debian.org/GrubEFIReinstall)
- [https://ixnfo.com/en/solving-the-error-mount-unknown-filesystem-type-lvm2\_member.html](https://ixnfo.com/en/solving-the-error-mount-unknown-filesystem-type-lvm2_member.html)


