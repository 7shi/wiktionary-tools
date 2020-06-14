import re, sqlite3, sys

try:
    db = sys.argv[1]
except:
    sys.stderr.write(f"usage: {sys.argv[0]} db\n")
    exit(1)

titles = {}
with open(db, "rb") as f: pass
with sqlite3.connect(db) as conn:
    cur = conn.cursor()
    count = cur.execute("SELECT COUNT(*) FROM pages").fetchone()[0]
    for i, (id, title) in enumerate(cur.execute(
            "SELECT id, title FROM pages"), start=1):
        if i == 1 or i % 10000 == 0 or i == count:
            sys.stderr.write(f"\rreading `pages`... {i:,} / {count:,}")
            sys.stderr.flush()
        if (i1 := title.find(":")) < 0 or title.find(":", i1 + 1) > i1: continue
        if (i2 := title.find("/")) < 0 or title.find("/", i2 + 1) > i2: continue
        if i1 > i2: continue
        title2 = title[:i2 + 1]
        if not title2 in titles: titles[title2] = 0
        titles[title2] += 1
sys.stderr.write("\n")
with open("search-title.tsv", "w", encoding="utf-8") as f:
    for title, count in sorted(titles.items(), key=lambda x: -x[1]):
        if count >= 20:
            f.write(f"{count}\t{title}\n")
