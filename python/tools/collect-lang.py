import mediawiki, io, re, sys

try:
    target, output, lang = sys.argv[1:]
except:
    sys.stderr.write(f"usage: {sys.argv[0]} db output lang\n")
    exit(1)

db = mediawiki.DB(target)
if not (lid := db.langid(lang)):
    sys.stderr.write(f"can not find: {lang}\n")
    exit(1)

pages = []
count = db.cur.execute(
    "SELECT COUNT(*) FROM idlang WHERE lid = ?", (lid,)).fetchone()[0]
for i, (id, title) in enumerate(db.cur.execute("""
        SELECT pages.id, title FROM pages
        INNER JOIN idlang ON pages.id = idlang.id AND lid = ?
        """, (lid,)), start=1):
    if i == 1 or i % 1000 == 0 or i == count:
        sys.stderr.write(f"\rreading `pages`... {i:,} / {count:,}")
        sys.stderr.flush()
    pages.append((title.strip().lower().replace("-", ""), id))

sys.stderr.write("\nSorting...\n")
pages.sort(key=lambda x:x[0])

pattern = re.compile("==([^=].*)==")
with open(output, "w", encoding="utf-8") as f:
    count = len(pages)
    for i, (_, id) in enumerate(pages, start=1):
        sys.stderr.write(f"\rwriting `pages`... {i:,} / {count:,}")
        sys.stderr.flush()
        page = db[id]
        text = page.text
        for item, lines in mediawiki.split_text(pattern, io.StringIO(text)):
            if item == lang:
                text = "".join(lines).strip()
                break
        if i > 1: f.write("\n")
        f.write(f"<!-- <title>{page.title}</title> -->\n\n{text}\n")
sys.stderr.write("\n")
