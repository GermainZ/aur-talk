#!/usr/bin/env python3
'''aur_talk.py <PACKAGE-NAME>: fetch and display and AUR package's comments.'''

import argparse
import textwrap
import re
import shutil
from urllib.request import urlopen
from urllib.error import HTTPError

import lxml.html
from lxml import etree
import html2text

URL = 'https://aur.archlinux.org/packages/{}/?O=0&PP={}'
# Setup HTML to Markdown converter.
MARKDOWN_CONVERTER = html2text.HTML2Text()
MARKDOWN_CONVERTER.ignore_links = False
MARKDOWN_CONVERTER.ul_item_mark = '-'
RE_STRONG = re.compile('\033\\[1m')
RE_EMPHASIS = re.compile('\033\\[3m')


def fetch_package_comments(package_name, num_comments):
    '''Return an AUR package's comments section as a list of HtmlElements.'''
    url = URL.format(package_name, num_comments)
    try:
        with urlopen(url) as resp:
            html = lxml.html.parse(resp)
    except HTTPError:
        print('Package "{}" not found.'.format(package_name))
        exit(1)
    return html.xpath(
        '/html/body/div[2]/div[@class="comments package-comments"]')


def print_author_and_date(element, args):
    '''Format and display a comment's author/date.'''
    text = element.text_content().strip()
    text = text if args.width == 0 else textwrap.fill(text, args.width,
                                                      break_long_words=False)
    print('\033[1m{}\033[0m'.format(text))


def correct_ansi_escapes(text, regex, repl):
    '''Replace every 2nd ANSI escape code (regex) with a reset code (repl).'''
    offset = 0
    for match in list(re.finditer(regex, text))[1::2]:
        pos = match.span()[1] - 2 + offset
        text = text[:pos] + repl + text[pos + 1:]
        offset += 1
    return text


def print_comment_body(element, args):
    '''Format and display a comment's body.'''
    text = etree.tostring(element).decode('utf-8')
    text = MARKDOWN_CONVERTER.handle(text).strip().replace('\n\n\n', '\n')
    if args.bold:
        text = correct_ansi_escapes(text, RE_STRONG, '21')
    if args.italic:
        text = correct_ansi_escapes(text, RE_EMPHASIS, '23')
    # html2text does not wrap list items, so we're gonna have to do it
    # manually.
    if args.width:
        lines = []
        for line in text.split('\n'):
            # If it's a list item, wrap it and indent it correctly.
            if line.startswith('  - '):
                num_spaces = len(line) - len(line.lstrip(' '))
                lines_ = textwrap.wrap(line.strip(),
                                       max(1, args.width - num_spaces),
                                       break_long_words=False,
                                       initial_indent='  ',
                                       subsequent_indent='    ')
                lines.extend(lines_)
            else:
                lines.append(line)
        text = '\n'.join(lines)
    print('\033[2m{}\033[0m\n'.format(text))


def print_package_comments(args):
    '''Fetch and display an AUR package's comments.'''
    comments_sections = fetch_package_comments(args.package_name,
                                               args.num_comments)
    if not comments_sections:
        print('No comments.')
        return
    has_pinned_comments = comments_sections[0].xpath(
        'div/h3/span[@class="text"]/text()')[0] == 'Pinned Comments'
    if args.latest_only and len(comments_sections) > 1:
        comments_sections.pop(0)
    elif args.pinned_only and has_pinned_comments:
        comments_sections.pop(1)
    elif args.pinned_only and not has_pinned_comments:
        print('No pinned comments.')
        return
    # Handle the comment sections ("Pinned" and/or "Latest Comments").
    for section in comments_sections:
        # Only print the section's title if there are multiple sections.
        if len(comments_sections) > 1:
            title = section[0].xpath('h3/span[@class="text"]/text()')[0]
            title = ' {} '.format(title)
            print('\033[1m{:—^{cols}}\033[0m\n'.format(
                title, cols=80 if args.width == 0 else args.width))
        # Print the comments.
        for element in section[1:]:
            if element.tag == 'h4':
                print_author_and_date(element, args)
            else:
                print_comment_body(element, args)


def main():
    '''Parse command-line arguments and fetch/display comments.'''
    arg_parser = argparse.ArgumentParser(
        description='Display AUR comments for PACKAGE-NAME.')
    group = arg_parser.add_mutually_exclusive_group()
    group.add_argument('-a', '--all', dest='num_comments', default=10,
                       action='store_const', const=1000,
                       help='Fetch all comments.')
    group.add_argument('-n', '--num-comments', type=int,
                       help=('Number of comments to fetch. Pinned comments are'
                             ' always fetched. Default is 10.'))
    group = arg_parser.add_mutually_exclusive_group()
    group.add_argument('-p', '--pinned-only', action='store_true',
                       help='Display the pinned comments only.')
    group.add_argument('-l', '--latest-only', action='store_true',
                       help='Display the latest comments only.')
    arg_parser.add_argument('-w', '--width', type=int, default=0,
                            help=('Number of columns for formatting output. '
                                  'Default is full available width.'))
    arg_parser.add_argument('-b', '--bold', action='store_true',
                            help=('Render **bold** text. May not work '
                                  'depending on your terminal.'))
    arg_parser.add_argument('-i', '--italic', action='store_true',
                            help=('Render _italic_ text. May not work '
                                  'depending on your terminal.'))
    arg_parser.add_argument('package_name', metavar='PACKAGE-NAME',
                            help=argparse.SUPPRESS)
    args = arg_parser.parse_args()
    MARKDOWN_CONVERTER.body_width = args.width
    # We're replacing both the starting and ending mark with an ANSI "start"
    # escape code. We'll replace every 2nd one with an "end" escape code in
    # `print_comment_body()`.
    if args.bold:
        MARKDOWN_CONVERTER.strong_mark = '\033[1m'
    if args.italic:
        MARKDOWN_CONVERTER.emphasis_mark = '\033[3m'
    # We only want pinned comments, so only fetch the bare minimum of normal
    # comments. Pinned comments are always returned by the server.
    if args.pinned_only:
        args.num_comments = 1
    print_package_comments(args)


if __name__ == '__main__':
    main()
