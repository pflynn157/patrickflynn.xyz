---
title: "A Week With Lineage OS"
date: "2022-02-14"
categories: 
  - "android"
  - "interesting"
  - "privacy"
---

Shortly before Christmas last year, I acquired a 2013 LG Nexus 5. Over break, I experimented with it some and eventually got [Lineage OS](https://lineageos.org/) running on it, and running well enough that I felt I could try it out for everyday use. This past week, I did just that- I pulled my SIM card out of my normal phone (a Google Pixel 4a), and used the 10 year old Nexus with its 3rd party OS as my everyday phone.

In all honesty, I am not someone real attached to their phone, so losing the convenience of the Pixel wasn’t a big deal for me. As long as the phone texts and calls, I’m generally happy. But the real purpose of this experiment was to see if 3rd party Android systems are usable.

So why in the world what I want to do this? And how did it go?

![](images/lineageos-768x1024.jpg)

LG Nexus 5 Running Lineage OS 17.1

### What is Lineage OS?

The short answer: Lineage OS is an open source fork of Android compatible with a large number of Android phones in existence.

Let’s rewind. In the smartphone world, there are only two real options if you want a usable smartphone: Android and iOS. IOS phones exist only on Apple hardware and are tied to Apple's ecosystem. The iOS source code is completely closed, whereas the Android source is built on Linux, and most of the actual Google-developed Android source is completely open source. As a result, while iOS only runs on Apple hardware, Android runs on pretty much everything else- Motorola, Samsung, LG, and so forth (and more recently, x86). Although there are technicalities behind the Google app licensing, pretty much any manufacturer can come along and create an Android smartphone.

IOS is very much a walled garden. Although you can jailbreak iOS devices and do a few things with them, you are pretty much at the mercy of Apple. Once your device is no longer supported, that’s it. And because Apple completely controls iOS, they can raise minimum application requirements, effectively rendering older devices obsolete. I’ve only had one iOS device- an iPad Mini- and it was the first and the last for that simple reason. Finally, Apple devices are ridiculously expensive (the combined value of iPhones in my college classes are probably worth more than my car).

Android in most ways is the opposite. Although Google is the primary developer, the code is open source meaning any hardware manufacturer can create an Android smartphone. As a result, Android phones can range from very decent models as good as the best iPhone to ultra cheap models that work well enough for its intended purpose. And although this is definitely a negative of the Android market, the fact that there are so many different Android phones out there means that they tend to have to be pretty old before they become obsolete and unusable. As a result, your average Android phone stands a chance of lasting longer than your equivalent iPhone.

A byproduct of this is the ability to create purely free, open source forks of Android. Although there are a lot of different Android phones out there, they tend to have many similarities, meaning that supporting a large number of devices isn’t impossible. This is where projects like Lineage OS come in. They create an open source Android distribution typically based on the latest versions of Android that can be flashed to many different phone models.

### Why Would I Want to do This?

This is all well and good, but why would I want to do this?

Hopefully you can see the answers between the lines, but if not, there are three main reasons: privacy, security, and economics.

The foremost reason for many people is privacy. Despite its closed nature, iOS is generally known for offering its users better privacy. On the other hand, Google is not known for respecting its users' privacy, to the point that Android is largely regarded as a tracking device. However, this is a double-edge sword. The invasive Android features only exist on phones that come preloaded with carrier and the Google services. If you build Android from the sources without any Google services, Android becomes ideal for mobile privacy. Lineage OS does just that.

The second is security, which overlaps a lot with our next point, the economics. Unless you have a flagship device, chances are that your Android phone manufacturer isn’t going to update it. If you’re lucky, you’ll get security and performance updates every now and then, and if you’re especially lucky you’ll get the next Android version. But that’s about it. Although smartphones are not known for being leaky security buckets like Windows, security does matter. 3rd party OSes tend to be security hardened, although in all honesty most people who know how to do this also know how to keep their devices up to date.

Which leads to our final point: economics. Digital waste is a big problem, and this is really the biggest reason why I refuse to use an Apple device (this applies more towards their mobile devices). Because iOS is closed off, Apple can (and does) make devices obsolete whenever they want. This is called “planned obsolesce”, which means in many cases you have to replace a perfectly good device for no good reason. Android gives you a way out of that. Unless you have an obscure phone, in many cases you can flash a new OS to your phone, and it becomes just as usable as the latest model.

### Why Do I Have a Pixel?

As someone who cares about privacy and hates spending money on a phone, you’re probably wondering why I have a Google Pixel in the first place.

Its true that a phone by Google is arguably the worst thing you can have for privacy. However, phones either manufactured by Google (like the Pixel) or with Google’s blessing (like the Nexus) are going to be the best as far as Androids go. These tend to be supported the earliest and the best by the open source Android community, and even if you don’t care about that, Google’s Android builds come without the bloat many other manufacturers build into theirs, and they tend to update longer. And the best part: they’re still really cheap for the quality (I can buy almost 3 Pixels for the cost of one iPhone).

Such is the irony of the mobile landscape. If you care about privacy and economics, your best choice ironically is to go with a Google phone.

### Installing Lineage OS

Installing Lineage OS was remarkably easy. Because I’ve done device hacking and jailbreaking in the past, and never keep my default OSes on any computer, I found the process super easy. That said, I don’t think you need a lot of technical skill to do this- the instructions are good enough that if you follow them, anyone with minimal technical ability can do this. Also, although I did this on Linux, this can be done on any computer.

Even though the Nexus 5 is well supported by the 3rd party Android ROM community, it is old, so many of the builds are now unofficial. In all, installing Lineage only took about 15 minutes. The phone is running Lineage OS 17.1- one version behind the latest, 18.1. This corresponds to Android 10, which is late enough (I think the Nexus came with Android 6).

The Nexus supports 4G networking, so it worked with my T-Mobile SIM card without any issues. Because its an older device, it had a hard time picking up the phone signal, so I ended up reinstalling Lineage a few times before I realized that was what the issue was. If you're having SIM card issues, trying going to a different room or outside before getting drastic :)

### The Week Without the Pixel

Overall, using the Nexus was not much different from using the Pixel. In fact, I hardly even noticed difference other than cosmetic changes like different messaging and phone apps. Because the hardware is older, it does lose phone signals more easily once I get out of the Charlotte area or when I go inside a building, but other than that I’ve had no issues with the telephony layers.

Although you can install Google apps on Lineage, for me that defeated the privacy aspect of it, so I decided not to do that. To install apps, you have two options: F-Droid and the Aurora Store. F-Droid has only free, open source applications, and in most cases you can find a suitable alternative. Two F-Droid apps that I regularly use, even on the Pixel, are New Pipe (a 3rd party Youtube/Youtube Music application) and Antenna Pod (a podcast app). However, there were applications I needed from the Play store, such as Mega, Discord, and Duo (to sign into school stuff). This is where the Aurora Store comes in. Using this, you can anonymously download Google apps and install and use them as on any other Android device.

The only annoying thing I had to fix was for some reason, Lineage throttles down the SMS app so notifications tended to be delayed. There was a simple fix for this, but the fact this wasn't enabled by default was really annoying. Notifications from other apps such as Discord didn’t seem to appear, but in all honesty I haven’t investigated this much.

As far as performance goes considering that I’m using a very recent version of Android on 10 year old hardware, I really have not noticed anything different. The system is very fast and snappy- really no different from the Pixel.

### Going Forward

Overall, I’m really impressed with 3rd party Android systems. I’m probably going to use the Nexus for another week or two, and then do something with the Pixel. There is another 3rd party OS called [Graphene OS](https://grapheneos.org/) optimized for Pixel phones that I’m probably going to try. Lineage OS is appealing for the Pixel, but Graphene looks a lot easier to install and presents a higher chance that everything will work perfectly.

But that will be another post...
