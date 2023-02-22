---
title: "Qt 102: Creating a Simple Editor"
date: "2022-05-30"
categories: 
  - "qt"
  - "tutorial"
---

Welcome back everyone! Around a month ago, we created a simple application in Qt to demonstrate the basics. However, our application wasn't very useful- only a label with a button. Today, we're going to create something a little more practical: a simple text editor.

My first non-trivial GUI application was a text editor (at the time, written in Java Swing). Since then, I've written several, including the main text/code editor I use for my everyday work. I continue to write simple editors, often as test programs for new languages and GUI frameworks I want to try out. Text editors are great programs for doing this (and learning GUI as a whole) because they don't require any unusual widgets or libraries. At the same time, they also demonstrate key core functionality. If you can write a text editor, you can easily write more advanced applications.

The text editor we're writing today will be simple, to say the least. It will have a single text widget with a menubar for the new/open/save/save-as functionalities. In other words, it will be very similar to Windows Notepad. This provides a good skeleton, however. You can easily extend it from there to add things like a toolbar, tabs, and more.

Because we covered project setup and window creation in the Qt101 post rather extensively, I'm not going to go over that again. I included the starting code below, which is from that post, except with the label and button removed. I will include the complete code at the end of this post.

[Download: starting-code](/assets/starting-code.zip)

## Adding the Text Edit

The first thing we're going to do is add the text edit widget. Qt has two widgets for this purpose: QTextEdit, and QPlainTextEdit. The former is an advanced widget which can do things like displaying images, rich text, and other advanced content. The QPlainTextEdit is only for plain text, although it can be used to highlight source code. For most practical purposes however, there isn't a huge difference. We're going to use QTextEdit simply because I have more experience with it :)

To add it, declare a widget in the header:

```
#pragma once

#include <QMainWindow>
#include <QFrame>
#include <QVBoxLayout>
#include <QLabel>
#include <QPushButton>
#include <QTextEdit>

// The class defining our main window
//
// We could use QWidget, but QMainWindow provides a lot
// more nice functions which make things easier, so unless you have
// a good reason it is better to use QMainWindow
//
class Window : public QMainWindow {
    Q_OBJECT
public:
    Window();
    ~Window();
private:
    QTextEdit *editor;
};
```

And then initialize it in the constructor. While we're at it, let's add it to the window.

```
// Init the editor
editor = new QTextEdit;
this->setCentralWidget(editor);
```

If you build and run, you should see something like this. Feel free to start typing in it:

![](images/editor1.png)

## Adding the Menubar

Excellent! Now we can start adding the menubar. In the menubar, we're going to have three menus: a File menu, an Edit menu, and a Help menu. In this section, we're only going to add the menubar with the menus to the window. We will connect everything in subsequent steps.

First, let's add the menubar to the menu with all the top level menus. We're not going to add the individual menu items just yet. Your window header will look like this:

```
#pragma once

#include <QMainWindow>
#include <QFrame>
#include <QVBoxLayout>
#include <QLabel>
#include <QPushButton>
#include <QTextEdit>
#include <QMenuBar>
#include <QMenu>

// The class defining our main window
//
// We could use QWidget, but QMainWindow provides a lot
// more nice functions which make things easier, so unless you have
// a good reason it is better to use QMainWindow
//
class Window : public QMainWindow {
    Q_OBJECT
public:
    Window();
    ~Window();
private:
    QTextEdit *editor;
    QMenuBar *menubar;
    QMenu *fileMenu, *editMenu, *helpMenu;
};
```

Notice the new classes near the bottom of the "private" section. Okay, now head over to the window source. Here, we will initialize everything in the constructor:

```
// Init the menubar
menubar = new QMenuBar;
this->setMenuBar(menubar);
    
fileMenu = new QMenu("File");
editMenu = new QMenu("Edit");
helpMenu = new QMenu("Help");
    
menubar->addMenu(fileMenu);
menubar->addMenu(editMenu);
menubar->addMenu(helpMenu);
```

Alright, now build and run. If you did everything correctly, you should see something like this:

![](images/step2.png)

Excellent! Our program is starting to look like something. Now, let's add actions (or sub-menus) to all the menubar items. Modify your header to look like this:

```
#pragma once

#include <QMainWindow>
#include <QFrame>
#include <QVBoxLayout>
#include <QLabel>
#include <QPushButton>
#include <QTextEdit>
#include <QMenuBar>
#include <QMenu>

// The class defining our main window
//
// We could use QWidget, but QMainWindow provides a lot
// more nice functions which make things easier, so unless you have
// a good reason it is better to use QMainWindow
//
class Window : public QMainWindow {
    Q_OBJECT
public:
    Window();
    ~Window();
private:
    QTextEdit *editor;
    QMenuBar *menubar;
    QMenu *fileMenu, *editMenu, *helpMenu;
    
    // File menu
    QAction *newFile, *openFile, *saveFile, *saveFileAs, *quitApp;
    
    // Edit menu
    QAction *cut, *copy, *paste, *selectAll;
    
    // Help Menu
    QAction *about, *aboutQt;
};
```

And in your constructor, add the following code under the last code we added:

```
// Init the file menu
newFile = new QAction("New");
openFile = new QAction("Open");
saveFile = new QAction("Save File");
saveFileAs = new QAction("Save File As");
quitApp = new QAction("Quit");
    
fileMenu->addAction(newFile);
fileMenu->addAction(openFile);
fileMenu->addAction(saveFile);
fileMenu->addAction(saveFileAs);
fileMenu->addAction(quitApp);
    
// Init the edit menu
cut = new QAction("Cut");
copy = new QAction("Copy");
paste = new QAction("Paste");
selectAll = new QAction("Select All");
    
editMenu->addAction(cut);
editMenu->addAction(copy);
editMenu->addAction(paste);
editMenu->addAction(selectAll);
    
// Init the help menu
about = new QAction("About");
aboutQt = new QAction("About Qt");
    
helpMenu->addAction(about);

helpMenu->addAction(aboutQt);
```

If all goes well, you should see something like this. The other menus should display their respective items.

![](images/step3.png)

## Connecting "Edit" and "Help"

Okay, now we can start making the menus do something. We're going to start by connecting the edit and help menus because these are the easiest. Connecting the files will require us to also implement the text editor functions. This step isn't hard, but I don't want to introduce too much at once. Let's get started.

First, in the header, add a section called "private slots", with the following function declarations:

```
private slots:
    // Edit menu slots
    void onCutClicked();
    void onCopyClicked();
    void onPasteClicked();
    void onSelectAllClicked();
```

Now, go to the source file, and add the following lines in the constructor between where we initialized the editor items, but before we add them to the menu:

```
connect(cut, &QAction::triggered, this, &Window::onCutClicked);
connect(copy, &QAction::triggered, this, &Window::onCopyClicked);
connect(paste, &QAction::triggered, this, &Window::onPasteClicked);
connect(selectAll, &QAction::triggered, this, &Window::onSelectAllClicked);
```

Now, scroll to the end of the source file, and add the following functions:

```
//
// The slots for handling the edit menu functions
//
void Window::onCutClicked() {
    editor->cut();
}

void Window::onCopyClicked() {
    editor->copy();
}

void Window::onPasteClicked() {
    editor->paste();
}

void Window::onSelectAllClicked() {
    editor->selectAll();
}
```

Perfect! Now we can add the help menu. The two help menu items will display dialogs. The first dialog ("About Qt") is part of the Qt framework, so using that is really easy. The second dialog ("About") is one we will construct ourselves, but it is still easy.

I want to go on a quick tangent to explain something here. You may be wondering why in the world we are adding an "About Qt" dialog. For a simple example application like this, it actually doesn't matter. But if you are doing any sort of real-world application released to the public using Qt, you are required under the open source licensing terms to state that you are using Qt, and where the sources and/or additional information can be found. Now to be honest, Qt won't go after you if you release a program without this information. You would have to be a big company or organization (like KDE) for them to care. However, it is both good practice and ethical to provide this information, and Qt makes it so easy there is almost no good reason not to.

Anyway. Like with the header file, add this line under "private slots":

```
// Help menu slots
void onHelpClicked();
```

Once again in the constructor, connect the menu items to their respective slots. Notice what we did for the "About Qt" item:

```
connect(about, &QAction::triggered, this, &Window::onHelpClicked);
connect(aboutQt, &QAction::triggered, qApp, &QApplication::aboutQt);
```

And finally, add the code for the "About" dialog. There are shorter ways you could do this, but I feel like this explains the concept more clearly:

```
//
// The slots for the help menu
//
void Window::onHelpClicked() {
    QMessageBox msg;
    msg.setWindowTitle("About Simple Editor");
    msg.setText("Simple Editor\\n"
                "A simple, cross-platform text editor written in C++ using the Qt libraries.\\n");
    msg.setDetailedText("License: Public Domain\\n");
    msg.setStandardButtons(QMessageBox::Ok);
    msg.exec();
}
```

If all goes well, you should see this when you click "About":

![](images/step4a.png)

And this when you click "About Qt":

![](images/step4b.png)

Excellent! We have made big progress. Next, we're going to add the file functions. In case you're lost at this point, here is our current code so far.

[Download: step4_code](/assets/step4_code.zip)

## Adding the File Menu

Let's start adding the file menu. Besides connecting these slots, this will allow us to implement our editor functions. Let's start off by adding the skeleton code for connecting the file menu slots.

First, add these lines under "private slots" in the header. Notice the "save" function. This goes right before the "private slots" in the "private" section. This function will do the actually saving- it will write to the file. Because the same code is needed for "Save" and "Save As", it is better to put it in its own function. Also notice the "path" variable. This is needed for all the functions to indicate the current file we are editing (if the string is empty, it is assumed to be untitled).

```
    // Indicates the current file
    QString path = "";    

    // Needed for the save slots
    void save();
private slots:
    // File menu slots
    void onNewFileClicked();
    void onOpenFileClicked();
    void onSaveFileClicked();
    void onSaveFileAsClicked();
```

Once again, add the "connect" calls in the constructor. Notice the one for the "Quit" menu. The "quit" function is not something we have to implement for simple programs (and even for some more advanced ones). It is defined as part of the Qt library, so we can use it in a similar way to the "About Qt".

```
connect(newFile, &QAction::triggered, this, &Window::onNewFileClicked);
connect(openFile, &QAction::triggered, this, &Window::onOpenFileClicked);
connect(saveFile, &QAction::triggered, this, &Window::onSaveFileClicked);
connect(saveFileAs, &QAction::triggered, this, &Window::onSaveFileAsClicked);
connect(quitApp, &QAction::triggered, qApp, &QApplication::exit);
```

Finally, add the skeleton for the functions we want to implement:

```
void Window::save(QString path) {

}

//
// The slots for handling the file menu
//
void Window::onNewFileClicked() {

}

void Window::onOpenFileClicked() {

}

void Window::onSaveFileClicked() {

}

void Window::onSaveFileAsClicked() {

}
```

Excellent! Now we can implement the individual functions. Let's start with the "New File" function. As you can see, this one is pretty straightforward:

```
// Creates a new file in the editor
void Window::onNewFileClicked() {
    path = "";
    editor->setText("");
}
```

Now, let's implement the "Open" function. This one is also fairly straightforward. Here, we prompt the user for a file, and then load it. One of the (many) nice things about Qt is that it is a whole framework, not just a GUI framework. While the C++ standard library functions for file IO are supposed to work on any systems, using the Qt equivalents is both somewhat easier and guaranteed to work on all systems. Here's the code:

```
// Opens a file and loads it to the editor
void Window::onOpenFileClicked() {
    QFileDialog dialog;
    dialog.setWindowTitle("Open");
    
    // If the dialog either doesn't run or doesn't have any selected
    // files, quietly return.
    //
    // In the real world, you would want to give the user an error message
    if (!dialog.exec() || dialog.selectedFiles().size() == 0) {
        return;
    }
    
    // This is a single-file editor, so only get the first selected file
    // The file dialog lets you select multiple files
    path = dialog.selectedFiles().at(0);
    
    // Now load the file
    QFile file(path);
    QString content = "";
    
    if (file.open(QFile::ReadOnly)) {
        QTextStream reader(&file);
        while (!reader.atEnd()) {
            content += reader.readLine() + "\\n";
        }
    }
    
    editor->setText(content);
}
```

Now, let's look at the click handlers for the "Save" and "Save As" items. Both of these are also fairly straightforward. In the "Save" function, if the current file is untitled, we need to jump to "Save As". Otherwise, the "Save As" function works fairly similar to the "Open" function.

```
// Saves the file
void Window::onSaveFileClicked() {
    QFile file(path);
    if (!file.exists()) {
        onSaveFileAsClicked();
        return;
    }
    
    save();
}

// Saves the file and prompts the user for a destination
void Window::onSaveFileAsClicked() {
    QFileDialog dialog;
    dialog.setDirectory(QDir::homePath());                // Set default location to $HOME
    dialog.setAcceptMode(QFileDialog::AcceptSave);        // This dialog is for saving
    dialog.setWindowTitle("Save File As");
    
    // If nothing was selected or the dialog didn't work, quiety return
    if (dialog.exec() != QFileDialog::Accepted) {
        return;
    }
    
    // Set the path and save the file
    path = dialog.selectedFiles().at(0);
    save();
}
```

Finally, we have the "save" function itself, which writes to the file:

```
// Saves the file
void Window::onSaveFileClicked() {
    QFile file(path);
    if (!file.exists()) {
        onSaveFileAsClicked();
        return;
    }
    
    save();
}
```

That's it! If all goes well, all the file menu options should work. At this point, you have a complete editor!

## Conclusion

This was a long post, but hopefully you made it through and found it interesting and helpful. At this point, we now have a complete editor, though admittedly it is a little crippled and not the most functional thing in the world. In a future post, we will build onto the editor some more to make it both look better and add more function.

Below is the final code for this project. All the code is in the public domain. Thanks for reading!

[Download: qt102](/assets/qt102.zip)


