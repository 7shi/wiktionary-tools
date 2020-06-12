import re, sys
pattern1 = re.compile("{{(.*?)}}")
pattern2 = re.compile("[a-z0-9_]+?=")
for line in sys.stdin:
    if (m := pattern1.search(line)):
        data = [d for d in m[1].split("|") if not pattern2.match(d)]
        line = line[:m.start()] + "{{" + "|".join(data) + "}}\n"
    sys.stdout.write(line)
