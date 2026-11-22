#!/bin/sh
# Rebuild V4 (site/play4) from V3: copies only index.html and applies the V4 patches.
# V4's own assets (ghost sprites, pframe art) stay in place. Assets shared with V3 are copied without deleting.
set -e
cd "$(dirname "$0")/.."
rsync -a --exclude='_*.html' --exclude='index.html' --exclude='mobile.html' site/play3/ site/play4/
cp site/play3/index.html site/play4/index.html
python3 tools/v4_rivals.py site/play4/index.html
python3 tools/v4_view.py site/play4/index.html
python3 tools/v4_wardenclyffe.py site/play4/index.html
python3 tools/v4_fbi.py site/play4/index.html
python3 tools/v4_projects.py site/play4/index.html
python3 tools/v4_haarp.py site/play4/index.html
python3 tools/v4_peace.py site/play4/index.html
sed 's/<html lang="en">/<html lang="en" class="m">/' site/play4/index.html > site/play4/mobile.html
echo "V4 built"
