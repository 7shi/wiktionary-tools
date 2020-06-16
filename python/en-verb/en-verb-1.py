import re, sys
pattern = re.compile("<!-- <title>(.*)</title> -->")
title = ""
for line in sys.stdin:
    if (m := pattern.match(line)):
        title = m[1]
    elif line.startswith("{{en-verb"):
        if not (" " in title or "-" in title):
            print(f"{title}\t{line.strip()}")
