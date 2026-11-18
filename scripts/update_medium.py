"""Rewrite the writing section of index.html with the latest Medium posts."""
import html
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from pathlib import Path

FEED = "https://medium.com/feed/@emokhles"
LIMIT = 10
INDEX = Path(__file__).resolve().parent.parent / "index.html"

req = urllib.request.Request(FEED, headers={"User-Agent": "Mozilla/5.0 (mokh.xyz feed updater)"})
root = ET.fromstring(urllib.request.urlopen(req, timeout=30).read())
items = list(root.iter("item"))[:LIMIT]
if not items:
    sys.exit("feed returned no posts; leaving index.html unchanged")

rows = []
for it in items:
    date = parsedate_to_datetime(it.findtext("pubDate")).strftime("%b %Y").lower()
    title = html.escape(it.findtext("title").strip())
    link = html.escape(it.findtext("link").split("?")[0])
    rows.append(f'<div class="row"><span class="m">{date}</span><a href="{link}">{title}</a></div>')

src = INDEX.read_text()
out = re.sub(r"(<!-- medium:start -->\n).*?(<!-- medium:end -->)",
             lambda m: m.group(1) + "\n".join(rows) + "\n" + m.group(2), src, flags=re.S)
INDEX.write_text(out)
print(f"{len(rows)} posts written")
