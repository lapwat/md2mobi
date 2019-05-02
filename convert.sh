#!/bin/sh
./pandoc --metadata title="$2" --metadata author="$3" --metadata lang=en $1 -o ebook.epub
./kindlegen ebook.epub > kindle.log
