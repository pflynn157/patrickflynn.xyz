---
title: "New Website, New Code, and New Things"
date: "2023-01-21"
---

Hello everyone! It's been a little bit since I've written here- definitely the first time this year- and as you can undoubtedly see, my site has changed. Again. But it's not the only thing that has changed. I'm also migrating to a new source code management system. But let's take one thing at a time.


## Part 1: On WordPress

(This is a mini mind-dump, so feel free to skip :)

The main point of interest is my new website. As you can very likely tell, it is not a WordPress site. In fact, it is anything but that. I got a little tired of dealing with WordPress, and after I succeeded in breaking it again, I decided enough was enough. Yeah, yeah, I know I'm probably clueless and WordPress is the greatest thing, etc, etc, but I'm not a web designer, and I've always had trouble getting it to work well.

And I have issues with it beyond my personal incompetence. For most people, WordPress is a great tool. I would be a fool to say otherwise. WordPress and many other similar website building tools are great examples of how we can take and improve programming in a more positive direction. Rather than sitting down and coding a website from scratch that will probably look like crap and be a security black hole, WordPress allows ordinary people to set up very powerful, relatively secure websites very easily. And I'm not talking about just blogs, although WordPress certainly makes up a huge portion of that market. You can combine WordPress with e-commerce tools and build an online business with minimal technical skills. This is a huge plus in a world where getting computers to do nonstandard things requires technical knowledge.

But as a fact of life for any form of engineering, WordPress had to make trade offs, and in my mind the big trade off was trading simplicity, speed, security, and in some cases, privacy for user friendliness. If you look at WordPress under the hood, it is not so much a website per se as a content generator. If you have a WordPress-based website, your website is the WordPress application which uses a collection of theme files, plugins, and a database to dynamically build and show your website to users, and for you to dynamically build and manage it directly from the server. This makes it easy to use, and for some applications this design is necessary, but it has the trade off of security, simplicity, and speed. If a user is making a request to your website from their browser, and WordPress running on your server has to fetch the content from the database, and build the page all while running plugins and fetching assets, that's always going to be slower than returning an existing HTML page. And it's always going have a much greater potential for privacy and security holes.

And due to this whole big layer-cake design, backing up or moving a WordPress website is a pain in the ass.

And once again: this isn't to directly rip WordPress. This is the engineering trade off using it. But if you have other, simpler options for your needs, they should really be considered. One of the most the common "other options" is to use a static website generator.

A static website generator is just what it sounds like: rather than your website being built at runtime, a static site generator builds a site from theme files and post/pages files into a complete, HTML/CSS website which you can then upload to your web server. These sites are super fast since it's basically the figurative "compile-time" option, and they are also really portable and relatively easy to manage. For technical users, even if they aren't web programmers, the learning curve is pretty low to make a decent website.

The problem is though that static site generators are definitely more of a learning curve than WordPress. WordPress is basically an idiot-proof, drag-and-drop builder, whereas most static site generators require setting up a rather complicated folder structure of themes, assets, pages, and posts. For me personally, this isn't super annoying, but learning how to create the config files can be unnecessarily complicated in my opinion. The big turnoff for me is that many site generators drag in a massive mound of dependencies. My favorite existing site generator is Pelican, which is Python based and relatively lightweight. The problem is that it's a little bit of a pain to customize, and getting the themes to work is questionable at best.


## The Solution

Maybe this comes partly from a point of pride, but my solution was to just roll my own static web site generator. Although it sounds complicated, it's actually not as bad as you would think. I first downloaded my existing WordPress website in the Jekyll website generator format, and then used those files as the base of my new website. I then designed a template for what I wanted it to look like, and finally created a relatively simple Python script to bind it all together and generate the final product, which is what you see here.

I will be honest: I've used Pelican enough to know how to use it and trust it (until the blog roll breaks...), but I really wanted something that was my own for my personal website. Maintaining a big website by hand really wasn't an option. When I started this, this blog was 1.5 years old, and there were close to 50 posts and around 20 pages, so manually converting all of those to HTML would have been a massive pain and waste of time. Thanks to my compiler background, I've gotten good at parsing and processing text, so rolling a Python generator was pretty easy. In fact, getting the actual generator to work was easy; fine-tuning it and going through all 50 posts and 20 pages was the long part.

To my surprise though, this generator actually worked rather well and produced a mostly good looking website. There are certainly still bugs, but it ended up working far better than I suspected. Of course, the above average result certainly doesn't mean it's great. The Markdown parsing isn't great, there is no syntax highlighting, very little control over what it can actually do, and so forth, but those are things we can improve over time. Eventually, I'll probably turn the generator into it's own static website generator project, but for now it will remain part of my website sources.

If you're curious, the sources can be found here: [https://hg.sr.ht/~pflynn157/patrickflynn.xyz](https://hg.sr.ht/~pflynn157/patrickflynn.xyz). Which leads to the next part...


## Source Code Hosting

As you know, I'm a heavy Github user with a lot of stuff on there. And as you probably also know if you've been looking at this site or my Github profile recently, there has been a slow change in my projects.

Github, and by consequence, Git, is definitely the dominant version control and source code hosting solution. And this is for good reason: Git is a fabulous tool and has changed the way we work with software. By further consequence, Github is also an amazing tool which has worked extremely well with Git in both popularizing it and making it easier to work with.

I believe though there has been a negative consequence to this. To Git itself, while I love the tool, I feel like it's become so common and almost so universal that it has come close to driving out all the competition. It's an analogous equivalent to Blink, the web engine of Google Chrome. There used to be a bunch of different web engines- Opera's Pesto, the IE engine (Trident?), the old MS Edge engine, and others, but now virtually every browser except Mozilla's Firefox uses Blink. Chrome obviously does, but so does Opera, the new Microsoft Edge, Brave, Vivaldi, and many others. You can argue that this points to the superiority of this project, and that's certainly true, but it also stifles competition. In the early days of the Internet, Microsoft tried to dictate standards through Internet Explorer, but they failed because of stiff competition from other browsers (and some legal stuff, but definitely other browsers). As a result, the web is an open standard, but web browsers could compete with each other so long as they followed this standard. The result was a better product, and for web developers, they weren't boxed into a single technology. They made web pages, not Blink pages.

Adopting a technology as "the" technology is generally not useful or a good idea. It stifles innovation both among the competition and within the project itself, and substantially opens the project to bloat and useless features. While as an outside observer, Git seems to have avoided this so far, that doesn't mean this will last forever, especially when the time comes that the original maintainers aren't still there. We need diversity in all areas, including version control.

And while I've spoken about Git, I have mostly positive things to say about Git and mostly negative things to say about Github. Before it was bought out by Microsoft, Github was a great tool. But now, I feel like it has become a product of big technology: bloated, tons of useless features, and very questionable practices. While I really didn't care all that much for the first few years, since the whole Copilot thing last summer, I've been starting to really have my doubts about the ethics surrounding this service.

I believe very strongly in the mission of Open Source and freedom in general, and Github and any big tech for that matter does not echo that. Technology can be a liberating power, but when it is attached to big tech, it goes the opposite direction.

I'll write more about this later, but let's suffice it to say that I'm planning on migrating my personal projects away from Github within the coming year. I'm currently testing a service called SourceHut, which I'm really liking thus far. I chose this service because I believe the author behind it has strong moral principles (in the context I'm talking about here), and I agree with his mission. And on a practical level, it offers Mercurial hosting, which is something I want to try to use more. For those not familiar with Mercurial, it's a very strong competitor to Git- it's similar, but has some nice features, including and especially simplicity.


## Future Work

I've started doing more programming again, but my work is starting to take a specific, defined direction. I have a few larger goals in mind that I want to start doing with my projects, so be on the look out for that. It's really interesting, but I've come to realize that I've built quite a substantial tools collection over the past few years, so my projects have allowed me to take a more experimental role now that I have frameworks for doing things. And needless to say, this is very nice.

At this point in time, but main focus in my personal projects (keyword: personal, not necessarily my professional focus) is accessibility and experimentation. I'm a big believer in two things: 1) Just because something has always been done a certain way doesn't mean that it's the right way or best way to do something, and 2) software and computer science as a whole should be more universal.

But more on that later.

Thanks for reading!



