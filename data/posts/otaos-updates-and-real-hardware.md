---
title: "OtaOS: Updates and Real Hardware"
date: "2022-11-16"
categories: 
  - "os-dev"
---

I made some recent updates to OtaOS. As a quick background, my dad got a new computer, so I re-inherited the one he was using. This particular computer is an old model, meaning it has the classic BIOS and text-mode hardware. While this sounds like a nightmare on the surface, it's nice because it means I can run some hobby and small-scale operating systems. Which includes my OtaOS project (and no, the name has no meaning if I haven't said that before).

I tried to get OtaOS running on one of my two computers, but the problem is that the laptop was made in 2018, and my desktop in 2020, so both of them had the latest (at the time) Intel processors, both of them had UEFI hardware, and neither of them had text-mode graphics. The desktop is actually easiest to work with, and I can get stuff to boot on it, but nothing displays because this mode doesn't exist. So, the 10-year-old computer comes to the rescue!

I had to reluctantly make one change to the OS though, and switch to Grub for bootloading. Although UEFI isn't the most loved piece of firmware ever created, it offers a huge advantage in being a standardized format for Intel PC hardware, whereas the old BIOSes were basically a collection of suggestions and conventions that might be followed, though in reality if you lined up 10 classic BIOS computers, they would all do 10 totally different things. And then you have your development emulators like QEMU, Boschs, VirtualBox, and VMWare which all do totally different things from the hardware and from each other. So yeah. Apparently, my custom bootloader didn't work on this particular piece of hardware, so I decided to just switch it back to Grub. Everything still works except for the disk driver. Apparently, using Grub broke it- either that, or I'm not detecting the drive correctly now. I lean towards Grub because it doesn't seem to be working in QEMU either now.

Everything is on Github. The main branch has the updated, Grub-based version, while the "oldboot" branch has the original custom bootloader version. Since it boots with Grub, it should (keyword: "should") work on any hardware with text-mode graphics. Keyboard and software interrupts should still work (software interrupts can be triggered with "1", "2", and "3" on the keyboard (not the numpad, the ones above the letters).

Here's a picture of it running. All the text except the first line was typed with the keyboard:

![](/images/otaos-1024x768.jpg)

