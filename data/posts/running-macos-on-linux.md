---
title: "Running MacOS on Linux"
date: "2021-06-27"
categories: 
  - "interesting"
  - "linux"
  - "tutorial"
---

A few weeks ago, I stumbled across an article on installing and running MacOS in a Docker container, and having absolutely nothing to do with my life the other day, I decided to try it. I had managed to get MacOS running in VirtualBox in the past, but performance wasn't great, installation was difficult, and I could go on. So far, this seems to be working rather well. The installation was super easy- much, much easier than the VM method.

I'm not going to walk you through how to do this right now, so here's the link if you're interested: [https://www.linuxuprising.com/2021/03/install-macos-big-sur-or-catalina-in.html](https://www.linuxuprising.com/2021/03/install-macos-big-sur-or-catalina-in.html)

### Why Would I Want To Do This?

Other than the coolness factor, this a great way to do application testing on MacOS if you don't have easy access to a Mac. Someday I'd like to upgrade to a Mac now that the M1 chips are out, but as a developer, my needs would be closer to the MacBook Pro range, and I have a hard time envisioning myself spending on one computer what my laptop and desktop combined cost. But anyway: The short answer is for testing.

This was very useful even when I had the VirtualBox version going. I ended up getting most of my desktop applications running on MacOS as a result. Stuff from the Apple Store never seemed to work, but it still ran. This new Docker version is the opposite. I got XCode working, along with the Apple Developer tools.

### System Specs

I'm not sure of the minimum specs, but you will need a fairly decent computer for this to run well. I run on a Dell desktop, and at the time of writing, its using about 6 GB of memory, but its certainly running up my processors. I got by running the VirtualBox version on my laptop, which has 12GB of RAM and an 8-core i7 processor. I would say that would be your minimum.

Since this is running Docker, however, you can probably get by with lower specs. Docker is a container solution, not a full virtualization solution, so there is a lot less overhead. However, the disk image takes up a fair among of disk space, so make sure you have plenty of disk space. And I would highly recommend using either an SSD or an M.2.

As far as performance goes, I haven't done extensive testing, but after installation, I installed XCode, the development tools, the Brew package manager, and built and ran a few things. Performance wasn't great at first when it was installing and starting for the first time, but afterwards it ran really well. I wouldn't say at near-native speeds, but certainly fast enough to justify using it.

### Pictures

Installing XCode and the developer tools (it actually didn't take long despite what the progress indicators said):

![](images/macos_installing_stuff-1024x576.png)

Here are two of my programs, including my text editor running in it:

![](images/programs-running-1024x576.png)

A little hello-world MacOS program in XCode:

![](images/xcode-helloworld-1024x577.png)
