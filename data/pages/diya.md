---
title: "Diya"
date: "2023-02-11"
template:page
output:diya
menu: false
---

This is one of my newer projects and my first non-compiler project in a while. Diya is a static website generator, specifically the one I built for generating this website right now.


### Why?

As you probably know, there are several static website generators out there, many of which are really good- and I will be the first to acknowledge that. And if you don't want to deal with the complexity of setting up a static website, there is WordPress, which is one of the best website creators out there. So what motivated me to create my own?

The first reason was simply for learning purposes. I wanted to make my personal website my own, but coding the entire thing and moving the 20ish pages and 50+ posts from the past few years would have been a _ton_ of work. I'm pretty familiar with Python, and thanks to my compiler background, parsing and processing text isn't an issue for me, so I figured I could put together a fairly decent-looking website and build a decent site generator without much work. And depending on how you look at it, I was right. This certainly isn't the greatest looking site out there, but it works well enough, and I'm happy with it.

The second reason, and the reason I made this a separate project, is like many software projects out there, I have a problem with the complexity of that which currently exists. The Pelican website generator is the best in my opinion, but I really don't like the themes, and I find it hard to work with. The most popular, Jekyll, has better themes, but dragging in the massive mess of Ruby is more than I care to deal with. There are other generators, for example Hugo, but besides their implementation languages, I really don't see any different between them and the ones I've already tried. I decided to fork the generator that I had written for this site, and make it a separate project, and to keep it deliberately simple and easy to use, so others could easily come behind me and fork it and use it for their needs.


### Documentation

This section contains all the documentation on how to use Diya.

#### Configuration

The config file: config.py.

The only required field in the "config" file is "name". All the fields available are:

- name = <string>
- custom\_links = \[ (name, link), ... \]
- output = <string>
- base = <string>
- pages = <string>
- post = <string>

The default folder structure is as follows:

- ./base -> The base theme folder, contains the HTML files for each part of the website
- ./data/assets -> For files and photos that are not processed but copied directly for the site's use
- ./data/pages -> Site pages
- ./data/posts -> Site posts
- ./output -> Where the generated website goes.


#### Pages

The structure of a page is as follows:

```
\-\-\-
title: Page Title
date: "2023-02-11"
template: page
output: mypage
menu: false
\-\-\-

Content... And content... and more content
```

Any content between the "---" markers are page metadata. The fields are as follows:

- title -> The page title, as displayed on the actual page.
- date -> The date in year-month-day format (not actually used at the moment, but required to be included).
- template -> The template from the "base" directory to use.
- output -> The name of the output html file (without the ".html" extension).
- menu -> Whether the page should be included on the navigation menu.


#### Posts

The structure of a post is as follows:

```
\-\-\-
title: "New Site"
date: "2021-06-16"
\-\-\-
```

As with pages, content between the "---" markers are metadata. The only two metadata items required for posts are "title" and "date", which should be fairly self-explanatory...



### Technical Details

The dependecies are very minimal. All you need is Python 3, and the Python-HTTP library.

Creating a custom theme is easy. Every theme must contain this structure (assuming you're in a theme directory, which defaults to "base"):

- ./css -> For stylesheets
- ./js -> Any Javascript
- ./base.html -> The base of all website pages
- ./blog.html -> The blog page (where all posts are displayed)
- ./blog\_roll\_item.html -> A snippet for the blog roll items within the list on the blog.html page
- ./page.html -> The base for all pages
- ./post.html -> The base for all posts

You can add additional template files for pages. The default "template: page" metadata item tells the generator to default to "page.html". However, if you change this and provide an appropriate html template file to go with it, you can have alternate page types.

The pages are marked by specific HTML comments. These comments tell the generator where to put certain items, such as text content, titles, navigation items, and so forth. If you create your own theme, each page must have these respective items:

#### base.html

- NAME -> The website title, which goes in the HTML <title></title> tags.
- NAME\_NAVBAR -> The website title, as displayed in the website navigation menu.
- NAVBAR -> The location for internal page links within the navigation menu (as specified by the "menu" metadata item).
- CUSTOM\_NAVBAR -> The location for custom, user-defined links within the navigation menu.
- TEMPLATE -> The main body area, where derived template content goes (ie, page content, post content, etc).

#### blog.html

- PREVIEW_ITEM -> The location for blog post previews within the blog-roll list.

#### blog\_roll\_item.html

Note that anything here should be a list item.

- PREVIEW\_TITLE -> The post title.
- PREVIEW\_DATE -> The post published date.
- PREVIEW -> The post excerpt text.

#### page.html

- PAGE\_TITLE -> The page title.
- PAGE\_CONTENT -> The page content.

#### post.html

- POST\_TITLE -> The post title.
- POST\_CONTENT -> The post content.

