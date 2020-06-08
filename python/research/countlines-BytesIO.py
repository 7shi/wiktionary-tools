import mediawiki_parse, bz2, io

target, spos, slen = mediawiki_parse.read()
lines = 0
with open(target, "rb") as f:
    for length in slen:
        with io.BytesIO(f.read(length)) as b:
            with bz2.open(b, "rt", encoding="utf-8") as t:
                while (line := t.readline()):
                    lines += 1
print(f"lines: {lines:,}")
