import os, re, sys

idx = sys.argv[1] if len(sys.argv) > 1 else ""
if not idx.endswith("-index.txt"): idx = ""
if not idx:
    print("usage: %s index.txt" % sys.argv[0])
    exit(1)

fn = idx[:-10]
xmlbz2 = fn + ".xml.bz2"
try:
    bz2size = os.path.getsize(xmlbz2)
except:
    print("file not found: %s" % xmlbz2)
    exit(1)

prev = 0
i = 0
tsv1 = fn + "-index-1.tsv"
tsv2 = fn + "-index-2.tsv"
with open(idx, "r", encoding="utf-8") as f:
    with open(tsv1, "w", encoding="utf-8") as w1:
        with open(tsv2, "w", encoding="utf-8") as w2:
            while (line := f.readline()):
                if (m := re.match("([^:]+):([^:]+):(.+)", line.strip())):
                    p = int(m[1])
                    if p != prev:
                        w1.write("%d\t%d\t%d\n" % (i, prev, p - prev))
                        i += 1
                        prev = p
                    w2.write("%s\t%d\t%s\n" % (m[2], i, m[3]))
            w1.write("%d\t%d\t%d\n" % (i, prev, bz2size - prev))

with open(fn + "-index.sql", "w", encoding="utf-8") as f:
    write = lambda line: f.write(line + "\n")
    write(".mode ascii")
    write(r'.separator "\t" "\n"')
    write("CREATE TABLE settings(key TEXT, value TEXT);")
    write("INSERT INTO settings VALUES('xmlbz2', '%s');" % xmlbz2)
    write(r".print Importing \'%s\'..." % tsv1)
    write("CREATE TABLE blocks(block INTEGER PRIMARY KEY, start INTEGER, length INTEGER);")
    write(".import %s blocks" % tsv1)
    write(r".print Importing \'%s\'..." % tsv2)
    write("CREATE TABLE pages(id INTEGER PRIMARY KEY, block INTEGER, title TEXT);")
    write(".import %s pages" % tsv2)
    write("CREATE INDEX pages_title_idx ON pages(title);")
