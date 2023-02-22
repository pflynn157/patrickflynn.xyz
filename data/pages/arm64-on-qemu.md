---
title: "Arm64 on Qemu"
date: "2021-06-16"
template: page
output: arm64-on-qemu
menu: false
---

I think I wrote a little bit about this at one point, but one of my new low-level interests is Arm. Partly because of my work in the HPC field, I've found the new Arm supercomputer in Japan to be really interesting. I find it really interesting how what was the architecture of smartphones is now making its way into other fields. Its even coming into the PC market- look at the new Apple computers. But from an even more personal perspective, I've found RISC architectures really interesting. I grew up (so to speak) on x86- and therefore, CISC architectures. Writing a compiler to generate CISC code is really easy; adapting that same code to RISC is an can be challenging.

Out of work and personal needs, I've been trying to get some emulators working for non-x86 architectures. I do have a Raspberry Pi 4, and while it is usable, its a little slow, and doesn't have any SVE support (SVE is Arm's new SIMD architecture). So far, I have MIPS32, RiscV64, Power 10, and AArch64 emulators up and running. The MIPS32 and AArch64 work pretty well; the RISC-V is getting there, and the POWER 10 really sucks (I'm working on it though). Today, I'm going to cover how to set up Ubuntu 20.04 on QEMU.

### Words of Warning

Virtualization is always slower than bare metal. Before you start giving me examples on how well Virtualbox works on your computer, yes you're probably right. But the reason why you can run an entire guest system on Virtualbox with really good speed is because the VM and the host system are x86 based, so the VM doesn't have to do as much translation. For different architectures, every single instruction has to be translated to an x86 instruction. On its own, its still really fast, but when you have an entire operating system on top of it, you will start to notice the difference.

I'm not saying this to scare you off. If you have a powerful computer, you can allocate resources to reduce this overhead quite a bit, but you will still notice. Its good enough for real work, but I wouldn't plan on running any huge builds too often, or doing things too resource-intensive.

### Words of Credit

I like to think I'm a genius, but let's be realistic: I'm not. Therefore, let us give credit where it is due. I initially got things going by following this article: [https://futurewei-cloud.github.io/ARM-Datacenter/qemu/how-to-launch-aarch64-vm/](https://futurewei-cloud.github.io/ARM-Datacenter/qemu/how-to-launch-aarch64-vm/). A lot of stuff is copied from there, so I wish to emphasize that most credit should be given to that author, not to me.

The reason why I wrote my own article is A) so it would be easily accessible for me, and B) because I did have to make enough changes to warrant a rewrite. The article is a little old; if you follow it, you will end up with Ubuntu 18.04. If you follow mine, you end up with Ubuntu 20.04 with SVE.

### Getting Started

First, you need to install these packages (note: I'm on Linux Mint. If you're not on Linux Mint/Ubuntu/Debian, you may have to change the package names):

sudo apt-get install qemu-system-arm qemu-efi-aarch64 qemu-utils

Next, create the boot images and the hard drive:

```
dd if=/dev/zero of=flash1.img bs=1M count=64
dd if=/dev/zero of=flash0.img bs=1M count=64
dd if=/usr/share/qemu-efi-aarch64/QEMU\_EFI.fd of=flash0.img conv=notrunc

qemu-img create ubuntu-image.img 20G
```

To download Ubuntu 20.04:

```
wget http://ports.ubuntu.com/ubuntu-ports/dists/focal/main/installer-arm64/current/legacy-images/netboot/mini.iso
```

Note that the site in question is an FTP site. If you want a different image, go for it.

### Install Ubuntu

Use this command to start the installation:

```
qemu-system-aarch64 \\
    -nographic \\
    -machine virt,gic-version=max \\
    -m 4G \\
    -cpu max \\
    -smp 4 \\
    -netdev user,id=vnet,hostfwd=:127.0.0.1:0-:22 -device virtio-net-pci,netdev=vnet \\
    -drive file=ubuntu-image.img,if=none,id=drive0,cache=writeback -device virtio-blk,drive=drive0,bootindex=0 \\
    -drive file=mini.iso,if=none,id=drive1,cache=writeback -device virtio-blk,drive=drive1,bootindex=1 \\
    -drive file=flash0.img,format=raw,if=pflash -drive file=flash1.img,format=raw,if=pflash 
```

Few notes here. First, the `-m 4G` represents how much memory is allocated to the machine. The original article said to use 512M. That took _FOREVER_ on my computer, so I would highly recommend to scale this up (once I scaled it, it only took like 15 minutes). The `-smp 4` represents the number of CPU cores to allocate to the virtual machine.

Just follow the prompts and instructions to install the system. It's really easy, so I'm not going to walk you through it. When you get to the end where it asks about additional software, I would only recommend doing the SSH server. Don't install a desktop system unless you're feeling adventurous. It will be slow. And quite frankly, I have no idea how you would run it... Maybe VNC?

### Boot Ubuntu

One you finished installing, you can use this command to launch the VM. You should put this in a script to make it easier to launch each time.

```
qemu-system-aarch64 \\
    -nographic \\
    -machine virt,gic-version=max \\
    -m 8G \\
    -cpu max,pmu=off,sve=on,sve256=on \\
    -smp 6 \\
    -netdev user,id=vnet,hostfwd=tcp::5556-:22 \\
    -device virtio-net-pci,netdev=vnet \\
    -drive file=ubuntu-image.img,if=none,id=drive0,cache=writeback -device virtio-blk,drive=drive0,bootindex=0 \\
    -drive file=flash0.img,format=raw,if=pflash -drive file=flash1.img,format=raw,if=pflash 
```

Again, I made a few changes from the original article. I scaled the memory and SMP up to my specs, so _make sure_ to check that before you run it. If you scale up to more than your computer can handle, it may freeze.

Notice the "sve" arguments in the "-cpu" line. This is where you can control the SVE vector lane size. SVE vectors start at 128-bits and increment from there by 128 up to 2048-bits. Also notice the line that begins with "-netdev". This allows you to SSH into the VM. For some reason, even if you're terminal is maximized, QEMU doesn't use the whole thing. SSH makes it more usable. The "5556-:22" sets the SSH port. So, to SSH in, you can use the following command:

```
ssh user@localhost -p 5556
```

Replace "user" with whatever user you created during installation.

### Conclusion

If all goes well, you shouldn't have any issues getting this up and working. So far this seems to run pretty well (even if it makes my computer run up a lot in the process :-). As I get other machines to work, I'll post updates.


