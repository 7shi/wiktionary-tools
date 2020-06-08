import mediawiki_parse, bz2

target, spos, slen = mediawiki_parse.read()
lines = 0
with bz2.open(target, "rt", encoding="utf-8") as f:
    while (line := f.readline()):
        lines += 1
print(f"lines: {lines:,}")
