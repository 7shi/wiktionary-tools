import mediawiki, re, sys

try:
    target, output, regex = sys.argv[1:]
except:
    sys.stderr.write(f"usage: {sys.argv[0]} db output regex\n")
    exit(1)

pattern = re.compile(regex)
db = mediawiki.DB(target)

pages = []
count = db.cur.execute("SELECT COUNT(*) FROM pages").fetchone()[0]
for i, (id, title) in enumerate(db.cur.execute(
        "SELECT id, title FROM pages"), start=1):
    if i == 1 or i % 10000 == 0 or i == count:
        sys.stderr.write(f"\rreading `pages`... {i:,} / {count:,}")
        sys.stderr.flush()
    if pattern.search(title):
        pages.append((title.strip().lower().replace("-", ""), id))
sys.stderr.write("\n")
if not pages:
    sys.stderr.write("no pages\n")
    exit(0)

sys.stderr.write("Sorting...\n")
pages.sort(key=lambda x:x[0])

with open(output, "w", encoding="utf-8") as f:
    count = len(pages)
    for i, (_, id) in enumerate(pages, start=1):
        if i == 1 or i % 100 == 0 or i == count:
            sys.stderr.write(f"\rwriting `pages`... {i:,} / {count:,}")
            sys.stderr.flush()
        page = db[id]
        text = page.text.strip()
        if i > 1: f.write("\n")
        f.write(f"<!-- <title>{page.title}</title> -->\n\n{text}\n")
sys.stderr.write("\n")
