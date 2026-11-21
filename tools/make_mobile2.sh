#!/bin/sh
# V2: play2/mobile.html = play2/index.html with the mobile layout switched on
cd "$(dirname "$0")/../site/play2" && sed 's/<html lang="en">/<html lang="en" class="m">/' index.html > mobile.html && echo "play2/mobile.html updated"
