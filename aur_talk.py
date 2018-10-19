#!/usr/bin/env python3
'''aur_talk.py <package-name>: fetch and display and AUR package's comments.'''

import textwrap
from urllib.request import urlopen
from urllib.error import HTTPError
import sys

import lxml.html
from lxml import etree
import html2text

URL = 'https://aur.archlinux.org/packages/{}/?O=0&PP=1000'
COLS = 79
# Setup HTML to Markdown converter.
MARKDOWN_CONVERTER = html2text.HTML2Text()
MARKDOWN_CONVERTER.ignore_links = False
MARKDOWN_CONVERTER.mark_code = True
MARKDOWN_CONVERTER.body_width = COLS
MARKDOWN_CONVERTER.ul_item_mark = '-'


def fetch_package_comments(package_name):
    '''Return an AUR package's comments section as a list of HtmlElements.'''
    url = URL.format(package_name)
    try:
        with urlopen(url) as resp:
            html = lxml.html.parse(resp)
    except HTTPError:
        print('Package "{}" not found.'.format(package_name))
        exit(1)
    return html.xpath(
        '/html/body/div[2]/div[@class="comments package-comments"]')


def print_author_and_date(element):
    '''Format and display a comment's author/date.'''
    text = element.text_content().strip()
    text = textwrap.fill(text, COLS)
    print('\033[4m{}\033[0m'.format(text))


def print_comment_body(element):
    '''Format and display a comment's body.'''
    text = etree.tostring(element).decode('utf-8')
    text = MARKDOWN_CONVERTER.handle(text).strip()
    # html2text does not wrap list items, so we're gonna have to do it
    # manually.
    lines = []
    for line in text.split('\n'):
        # If it's a list item, wrap it and indent it correctly.
        if line.strip().startswith('-'):
            num_spaces = len(line) - len(line.lstrip(' '))
            lines_ = textwrap.wrap(line.strip(), COLS - num_spaces)
            lines.append(lines_[0])
            for line_ in lines_[1:]:
                lines.append('{}{}'.format(' ' * num_spaces, line_))
        else:
            lines.append(line)
    text = '\n'.join(lines)
    print('{}\n'.format(text))


def print_package_comments(package_name):
    '''Fetch and display an AUR package's comments.'''
    comments_sections = fetch_package_comments(package_name)
    # Handle the comment sections ("Pinned" and/or "Latest Comments").
    for section in comments_sections:
        # Only print the section's title if there are multiple sections.
        if len(comments_sections) > 1:
            title = section[0].xpath('h3/span[@class="text"]/text()')[0]
            title = textwrap.fill(title, COLS)
            line = '=' * COLS
            print('{}\n= {:^{cols}} =\n{}\n'.format(line, title, line,
                                                    cols=COLS-4))
        # Print the comments.
        for element in section[1:]:
            if element.tag == 'h4':
                print_author_and_date(element)
            else:
                print_comment_body(element)


if __name__ == '__main__':
    if len(sys.argv) != 2 or sys.argv[1].startswith('-'):
        print('Syntax: aur_talk.py <package-name>')
        exit(1)
    print_package_comments(sys.argv[1])
