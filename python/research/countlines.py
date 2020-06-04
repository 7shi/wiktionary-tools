import bz2
target = "enwiktionary-20200501-pages-articles-multistream.xml.bz2"
lines = 0
with bz2.open(target, "rt", encoding="utf-8") as f:
    while (_ := f.readline()):
        lines += 1
print(f"lines: {lines:,}")
