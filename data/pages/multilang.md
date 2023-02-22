---
title: "Multilang"
date: "2023-02-01"
template:page
output:multilang
menu: false
---

Multilang is a natural language project I dd back over Christmas break to fullfill a personal need and what I think is a larger need for language learners. When you are learning a language, one of the most essential components is a language to language dictionary, ie a French-English-French dictionary. And of course, while these are great tools, they can be big and daunting. For me at least, this is an annoying problem- to constantly have to flip through a dictionary.

A theme-based dictionary, such as an English-French theme dictionary, is one idea of improvement. Its based on two premises. First, the majority of everyday spoken language is comparetively small to the language as a whole. Of any given language, only about one to two thousand words make up the bulk of what you need to know. Secondly, it is often helpful to think in these. Words can be grouped into different categories, and if you're trying to translate a work, you can narrow things down significantly if you know what category your word belongs to. Even if you're not a language learner per se, having this theme division can be interesting for comparing languages.

My multilang project builds on this idea. In this project, I devised a list of thirty or so categories, and then group the 1000 most used English words into these categories. With this done, we can then translate these sorted words into other languages.

On a technical level, this backbone of this is a large CSV file. The file contains the word list, which is sorted by category. The categories are defined by their abbreviations. From there, we can add a column per language. A Python processing script generates a latex file for each language, which can then be compiled into the final PDF.

I believe in the freedom of information, and the freedom and power of learning, so this entire project is free. There are dictionaries for two languages- French and Ido- and in-process dictionaries for two more: Hindi and Italian.

Note that this project is very much subject to improvement, so I welcome any suggestions aabout the organization or the project as a whole.

Here are the downloads:

[Download: English to Ido](/assets/english_ido_dict.pdf)

[Download: Ido to English](/assets/ido_english_dict.pdf)

[Download: Ido (Complete)](/assets/Ido.pdf)

[Download: French (Complete)](/assets/French.pdf)

[Download: Hindi (Partial)](/assets/Hindi.pdf)

[Download: Italian (Very partial)](/assets/Italian.pdf)


