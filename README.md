Description
===========

These scripts fetch and display the comments of an AUR package.

Two versions are provided: Python and Shell.
The Python version is the recommended one. It is faster and has better comments
formatting. Additionally, the shell version does not support some options like
`-b` and `-i`.

This program is also available from the AUR:
[aur-talk-git](https://aur.archlinux.org/packages/aur-talk-git/). It will be
installed as `aur-talk` and can be used directly with
[aurutils](https://github.com/AladW/aurutils) 2.0+ as a
[contrib](https://github.com/AladW/aurutils/tree/master/contrib) script (e.g.
`aur talk aurutils -p`).

Usage
=====

- Python version: `$ ./aur_talk.py [...] <PACKAGE-NAME>`
- Shell version: `$ ./aur_talk.sh [...] <PACKAGE-NAME>`

```
Usage: aur_talk [-h] [-a | -n NUM_COMMENTS] [-p | -l] [-w WIDTH | -f] <PACKAGE-NAME>
Display AUR comments for PACKAGE-NAME.

-h, --help            show this help message and exit
-a, --all             Fetch all comments.
-n NUM_COMMENTS, --num-comments NUM_COMMENTS
                      Number of comments to fetch. Pinned comments are
                      always fetched.
-p, --pinned-only     Display the pinned comments only.
-l, --latest-only     Display the latest comments only.
-w WIDTH, --width WIDTH
                      Number of columns for formatting comments. Default
                      is full available width.
-b, --bold            Render **bold** text. May not work depending on your
                      terminal.
-i, --italic          Render _italic_ text. May not work depending on your
                      terminal.
```

Dependencies
============

`aur_talk.py` dependencies:

- [python 3](https://www.python.org/)
- [lxml](http://lxml.de/)
- [html2text](https://pypi.python.org/pypi/html2text/)

Arch users can install them from the main repo: `python`, `python-lxml` and
`python-html2text`.

`aur_talk.sh` dependencies:

- [curl](https://curl.haxx.se/)
- [hq](https://github.com/coderobe/hq)
- [lynx](https://lynx.browser.org/)

Arch users can install them from the main repo: `curl`, `hq` and `lynx`.

Example output
==============

![Screenshot](https://raw.githubusercontent.com/GermainZ/aur-talk/master/screenshot.png "Screenshot")
