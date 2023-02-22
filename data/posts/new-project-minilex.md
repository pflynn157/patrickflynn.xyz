---
title: "New Project: MiniLex"
date: "2022-05-25"
categories: 
  - "project-updates"
---

I recently published a new project: MiniLex.

MiniLex is a simple, minimalist lexical analyzer generator. It began life once again due to my laziness. Regardless of what language you are parsing, lexical analyzers are very similar. The only difference is what elements are considered keywords, symbols, literals, and so forth. Because of these similarities, lexical analyzers can be generated rather easily.

Because of the similarities of lexical analyzers, I found myself recycling a very stable one I wrote a while back for the [Orka project](/orka.html). While copying and changing the code for each new project isn’t that big of a deal, its tedious, error-prone, and a little time consuming. When I began some new projects over spring break, I got to thinking that I could probably write a generator rather easily. And thus the project was born.

MiniLex generates a C++ lexical analyzer based on the original one from Orka. The analyzer itself is written in Python. This is one area where I think Python really outdoes itself. Python makes quick file parsing tasks surprisingly easy, and its sufficiently expressive to work with a variety of list types. While I’m not usually a Python fan, this is one area where I do like it.

Feel free to check it out [here](/minilex.html)!
