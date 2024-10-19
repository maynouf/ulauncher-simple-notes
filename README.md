# ulauncher-simple-notes

This is a simple [Ulauncher](https://ulauncher.io/) extension meant to create notes quickly.

![gif showing how the extension works](https://github.com/maynouf/ulauncher-simple-notes/blob/main/images/ulauncher-simple-notes.gif)

I encourage the reader to [report any bugs or problems that you might find](https://github.com/maynouf/ulauncher-simple-notes/issues) using the extension.


## How does it work?

`Ulauncher key` + `note` + `your note's text` + `Enter`

1. You press your Ulauncher launcher key, 
2. You type in your keyword (`note` by default, changeable in preferences), 
3. You type in a note and you press `Enter`. 
4. Your note is saved in your specified path* (`~/note.md` by default, changeable in preferences). 

Simple as.

\*If you don't have writing permission in the path you've specified, an error notification should pop up.

### Want to open your notes?

`Ulauncher key` + `note` +  `open`* + `Enter`. 

\*You can change it in your preferences.

### Want to have timestamps?

Check your preferences.


## Dependencies

The only Python modules it uses are `os`,  `subprocess` and `datetime`, which apparently are included by default with Python installations.

It uses `notify-send` for the error notifications in case your path is unaccessible. ChatGPT tells me that if it's not installed, you can add it using your package manager. For example:

On Ubuntu/Debian:

```bash
sudo apt install libnotify-bin
```
On Fedora:

```bash
sudo dnf install libnotify
```
On Arch Linux:

```bash
sudo pacman -S libnotify
```

Sorry, no idea how to do make it work in Red Star OS or TempleOS.


## Whats the use case of this extension?

You are working / on a meeting / watching a Youtube video / pondering about deep metaphysical questions in front of your PC. 

You suddenly get an idea or an inspiration, you are reminded of a task or an event.

You could open your favourite note-taking app a GUI. It might take some seconds to load, though. Maybe you have to open a new note. Maybe you have to save it somewhere, find the path, choose a name. You would probably have to use the mouse for some of that though...

You could open a terminal and use your preferred screen-based text editor program / `echo` something somewhere in bash. You'd have to close the terminal afterwards, though...

Instead, you can simply `Ulauncher key` + `note` + `your note's text` + `Enter`. 

You can use those extra seconds you just gained to doomscroll your favourite feed/s.

No, but really, it is useful to write down things you cannot classify, categorize, or properly organize at a particular moment.


## Why did I do this?

Just started using Ulauncher and find it really useful. I found some similar note-taking extensions, but I wanted something really, really simple, and also to learn the ropes of making Ulauncher extensions to do more ambitious things in the future.
