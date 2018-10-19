Description
===========

These scripts fetch and display the comments of an AUR package.

Two versions are provided: Bash and Python.
The Python version is faster and has better comments formatting.

Usage
=====

- Python version: `$ ./aur_talk.py <package-name>`
- Bash version: `$ ./aur_talk.sh <package-name>`

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
