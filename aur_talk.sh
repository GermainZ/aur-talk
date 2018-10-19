#!/bin/bash -

print_section () {
    for i in {1..1000}; do
        author=$(hq "div.comments:nth-child($1) > .comment-header:nth-of-type($i)" text <<< "$page" | xargs)
        [ -z "$author" ] && break || echo -e "\e[4m$author\e[0m"
        hq "div.comments:nth-child($1) > div.article-content:nth-of-type($((i+1)))" data <<< "$page" | lynx -width=88 -stdin -dump -nolist | sed -e 's/^ *//'
        echo
    done
}

page=$(curl 2>/dev/null "https://aur.archlinux.org/packages/$1/?O=0&PP=1000")
is_pinned=$(hq "div.comments:nth-child(9)" data <<< "$page")
[ -n "$is_pinned" ] && echo -e "===================\n= PINNED COMMENTS =\n===================\n"
print_section 7
[ -n "$is_pinned" ] && echo -e "\n===================\n= LATEST COMMENTS =\n===================\n" || exit
print_section 9
