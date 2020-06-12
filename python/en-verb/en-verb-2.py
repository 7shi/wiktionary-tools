import re, sys
pattern1 = re.compile("\[\[(.+?)\]\]")
pattern2 = re.compile("<!--(.*?)-->")
for line in sys.stdin:
    while (m := pattern1.search(line)):
        data = m[1].split("|")
        line = line[:m.start()] + data[-1] + line[m.end():]
    sys.stdout.write(pattern2.sub("", line))
