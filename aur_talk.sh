#!/bin/sh -
set -o errexit -o pipefail -o noclobber -o nounset

OPTIONS=an:plw:fh
LONGOPTS=all,num-comments:,pinned-only,latest-only,width,free-format,help
PARSED=$(getopt --options=$OPTIONS --longoptions=$LONGOPTS --name "$0" -- "$@") || exit 1
eval set -- "$PARSED"
unset PARSED

print_help () {
    printf -- "Usage: %s [-h] [-a | -n NUM_COMMENTS] [-p | -l] [-w WIDTH | -f] <PACKAGE-NAME>\n" "$0"
    printf -- "Display AUR comments for PACKAGE-NAME.\n\n"
    printf -- "-h, --help            show this help message and exit\n"
    printf -- "-a, --all             Fetch all comments.\n"
    printf -- "-n NUM_COMMENTS, --num-comments NUM_COMMENTS\n"
    printf -- "                      Number of comments to fetch. Pinned comments are\n"
    printf -- "                      always fetched.\n"
    printf -- "-p, --pinned-only     Display the pinned comments only.\n"
    printf -- "-l, --latest-only     Display the latest comments only.\n"
    printf -- "-w WIDTH, --width WIDTH\n"
    printf -- "                      Number of columns for formatting comments. Default\n"
    printf -- "                      is 80.\n"
    printf -- "-f, --free-format     Print without any width restrictions.\n"
}

a=n n=10 p=n l=n w=80 f=n
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
        -f|--free-format)
            f=y
            w=1024
            shift;
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
    printf "Only one of -p and -l can be used at the same time.\n"
    exit 1
elif [ "$a" = "y" ] && [ "$n" != "1000" ]; then
    printf "Only one of -a and -n can be used at the same time.\n"
    exit 1
elif [ "$f" = "y" ] && [ "$w" != "1024" ]; then
    printf "Only one of -f and -w can be used at the same time.\n"
    exit 1
fi

print_section () {
    i=1
    while [ $i -le 1000 ]; do
        author=$(printf '%s' "$page" | hq "div.comments:nth-child($1) > .comment-header:nth-of-type($i)" text | xargs)
        [ -z "$author" ] && break || printf "\e[4m%s\e[0m\n" "$author"
        printf '%s' "$page" | hq "div.comments:nth-child($1) > div.article-content:nth-of-type($((i+1)))" data | lynx -width=$(($2+8)) -stdin -dump -nolist | sed -e 's/^ *//'
        printf "\n"
        i=$((i+1))
    done
}

page=$(curl 2>/dev/null "https://aur.archlinux.org/packages/$1/?O=0&PP=$n")
is_pinned=$(printf '%s' "$page" | hq "div.comments:nth-child(9)" data)
if [ "$p" = "y" ] || [ "$l" = "n" ]; then
    if [ -n "$is_pinned" ]; then
        printf "===================\n= PINNED COMMENTS =\n===================\n\n"
    else
        printf "No pinned comments.\n"
        exit
    fi
    print_section 7 $w
fi
if [ "$p" != "y" ] || [ "$l" = "y" ]; then
    if [ -n "$is_pinned" ]; then
        printf "===================\n= LATEST COMMENTS =\n===================\n\n"
        print_section 9 $w
    else
        print_section 7 $w
    fi
fi
