#!/bin/sh
# play/mobile.html = play/index.html with the mobile layout switched on (<html class="m">). Run after every change to index.html.
cd "$(dirname "$0")/../site/play" && sed 's/<html lang="en">/<html lang="en" class="m">/' index.html > mobile.html && echo "mobile.html updated"
