---
title: "Disassembling a Dell Inspiron Laptop"
date: "2021-07-11"
categories: 
  - "tips"
  - "tutorial"
---

I am long-time Dell computer user. My first computer was a large Dell desktop originally running Windows XP, and then Linux Mint when I inherited it. I had an HP after that, which was a complete piece of junk, and after that for college, I got a Dell Inspiron laptop. Since then, I've also bought a Dell XPS for development and personal home use (thanks to its many drives). My family also uses Dell, with two members having Dell Inspirons as well.

While I have a lot of good to say about Dell machines, the only thing that annoys me is the drives aren't always the best for the money. When I bought mine, it had a 2TB hard drive, which is great if you need the space, but for most else it is painfully slow. My mom, who has 20 years of family photos, also had a similar problem (only in her case, the drive was too small). I upgraded my drive about a year after getting mine, and this past weekend, I swapped it out into her laptop and got a new drive for myself.

Today, I'm going to give a quick overview on how to disassemble one of these laptops. The Dell Inspirons have a similar structure regardless of the model, so you should be good to follow through regardless of what you have. In my case, I have a Dell Inspiron 7573.

### Disclaimer...

I've taken apart Inspiron laptops several times, and I've never had an issue. You shouldn't either if you follow instructions and pay attention to what you are doing.

That said, I am not responsible if you mess up your computer by doing this. If something bothers you, don't do it. You have been warned.

### Disassembly

First, you need to unscrew the bottom. The screws near the edge near the front where it curves come out, but depending on the model, the rest may or may not come out (some cases have some kind of prevention mechanism to keep you from losing the screws). On my 7573, they stayed in, but in my mom's lower-end machine, they came out. Just be careful not to lose them.

![](images/step1-768x1024.jpg)

Getting the cover off is tricky. Start by lifting it open from the back corners, by the hinges:

![](images/step2-1024x768.jpg)

Do this on both sides, and when its up enough, you should be able to lift it near the front. Although it sounds counter-intuitive, the case actually opens on the front first, and lifts off the back. Some sources may recommend using tools, but I've been fine just using my hands. Once you get it open, you will see the inside:

![](images/step3-1024x768.jpg)

Before you do anything to it, remove the battery. There are two screws holding it in on each side (so four total):

![](images/step5-768x1024.jpg)

![](images/step4-768x1024.jpg)

When you get the screws out, unplug it from the motherboard. The cord on the battery stays attached to the battery, not the motherboard:

![](images/step6-1024x768.jpg)

The Inspirons have ports for regular SATA drives and NVMe SSDs. There are two types of NVMe SSDs: the full-length ones, and the half-length ones (I'm sure there's an actual technical name for it, but I'm not sure). Full-length SSDs will go right in, but the half-length will not unless you have a brace. My mom's computer came with a brace, but it didn't fit mine, and I couldn't find one so I ended up just getting a new SATA SSD.

The case for the SATA drive looks like this:

![](images/step7-768x1024.jpg)

The number of screws holding it will depend on the model, but it should be self-evident what screws are which. Unhook the drive (if you have an existing one), unscrew the case, and pull it out.

The drive will be screwed into the case, so just pull out the four screws holding it in- two on each side:

![](images/step8-1024x768.jpg)

This is what your machine will look like with the battery and hard drive out. I include it for reference purposes. On the 7573, the NVMe port is that black area between the fan and the HDD area. On my mom's computer, it was located on the side near the front, I think near the battery. If you're looking to upgrade the RAM, it is under that big black square near the opposite side from the fan.

![](images/step9-768x1024.jpg)

When you are finished, simply put it all back together in reverse order. If you put a new drive in, make sure to have a USB ready so you can install the OS on it. If not, you'll get stuck in a BIOS loop when you turn it on. I'm not sure what newer models do, but old models would just run in a loop forever until you turn the computer off.

### Conclusion

Although taking a laptop apart may seem like a scary process, its actually really easy. While I don't have experience taking other models apart, they should be fairly similar to work on. Regardless of what you have, hopefully this gives you a good starting point.

Until next time!
