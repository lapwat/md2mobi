#!/bin/bash
sed '1s/^/% '"$TITLE"'\n% '"$AUTHOR"'\n\n/' ebook.md > ebook_with_meta.md
pandoc ebook_with_meta.md -o ebook.epub
./kindlegen ebook.epub > kindle.log
cat ebook.mobi
