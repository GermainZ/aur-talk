Description
===========

These scripts fetch and display the comments of an AUR package.

Two versions are provided: Shell and Python.
The Python version is faster and has better comments formatting.

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
                      is 80.
-f, --free-format     Print without any width restrictions.
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
