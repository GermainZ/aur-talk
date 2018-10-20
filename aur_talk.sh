#!/bin/sh -
set -o errexit -o noclobber -o nounset

OPTIONS=an:plw:h
LONGOPTS=all,num-comments:,pinned-only,latest-only,width,help
PARSED=$(getopt --options=$OPTIONS --longoptions=$LONGOPTS --name "$0" -- "$@") || exit 1
eval set -- "$PARSED"
unset PARSED

print_help () {
    printf -- 'Usage: %s [-h] [-a | -n NUM_COMMENTS] [-p | -l] [-w WIDTH | -f] <PACKAGE-NAME>\n' "$0"
    printf -- 'Display AUR comments for PACKAGE-NAME.\n\n'
    printf -- '-h, --help            show this help message and exit\n'
    printf -- '-a, --all             Fetch all comments.\n'
    printf -- '-n NUM_COMMENTS, --num-comments NUM_COMMENTS\n'
    printf -- '                      Number of comments to fetch. Pinned comments are\n'
    printf -- '                      always fetched. Default is 10.\n'
    printf -- '-p, --pinned-only     Display the pinned comments only.\n'
    printf -- '-l, --latest-only     Display the latest comments only.\n'
    printf -- '-w WIDTH, --width WIDTH\n'
    printf -- '                      Number of columns for formatting comments. Default\n'
    printf -- '                      is full available width.\n'
}

a=n n=10 p=n l=n w=1024
while true; do
    case "$1" in
        -a|--all)
            a=y
            n=1000
            shift
            ;;
        -n|--num-comments)
            n="$2"
            shift 2
            ;;
        -p|--pinned-only)
            p=y
            shift;
            ;;
        -l|--latest-only)
            l=y
            shift;
            ;;
        -w|--width)
            w="$2"
            shift 2;
            ;;
        -h|--help)
            print_help
            exit
            ;;
        --)
            shift
            break
            ;;
        *)
            exit 2
            ;;
    esac
done

if [ "$#" -lt 1 ]; then
    print_help
    exit 1
elif [ "$p" = "y" ] && [ "$l" = "y" ]; then
    printf 'Only one of -p and -l can be used at the same time.\n'
    exit 1
elif [ "$a" = "y" ] && [ "$n" != "1000" ]; then
    printf 'Only one of -a and -n can be used at the same time.\n'
    exit 1
fi

print_section () {
    i=1
    while [ $i -le 1000 ]; do
        author=$(printf '%s' "$page" | hq "div.comments:nth-child($1) > .comment-header:nth-of-type($i)" text | xargs)
        [ -z "$author" ] && break || printf '\033[1m%s\033[0m\n' "$author"
        comment=$(printf '%s' "$page" | hq "div.comments:nth-child($1) > div.article-content:nth-of-type($((i+1)))" data | lynx -width=$(($2+8)) -stdin -dump -nolist | sed -e 's/^ *//')
        printf '\033[2m%s\033[0m\n\n' "$comment"
        i=$((i+1))
    done
}

print_line() {
    i=1
    while [ $i -le "$1" ]; do
        printf '—'
        i=$((i+1))
    done
}

print_title() {
    [ "$1" -eq 1024 ] && lw=80 || lw="$1"
    line_width=$(((lw - ${#2}) / 2 - 2))
    printf '\033[1m'
    print_line $line_width
    printf ' %s ' "$2"
    print_line $line_width
    printf '\033[0m\n\n'
}

page=$(curl 2>/dev/null "https://aur.archlinux.org/packages/$1/?O=0&PP=$n")
is_pinned=$(printf '%s' "$page" | hq "div.comments:nth-child(9)" data)
if [ "$p" = "y" ] || [ "$l" = "n" ]; then
    if [ -z "$is_pinned" ]; then
        printf 'No pinned comments.\n'
        exit
    fi
    [ "$p" = "n" ] && print_title "$w" "PINNED COMMENTS"
    print_section 7 "$w"
fi
if [ "$p" != "y" ] || [ "$l" = "y" ]; then
    if [ -n "$is_pinned" ]; then
        [ "$l" = "n" ] && print_title "$w" "LATEST COMMENTS"
        print_section 9 "$w"
    else
        print_section 7 "$w"
    fi
fi
