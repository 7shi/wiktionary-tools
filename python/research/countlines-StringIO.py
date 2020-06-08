import mediawiki_parse, bz2, io

target, spos, slen = mediawiki_parse.read()
lines = 0
with open(target, "rb") as f:
    for length in slen:
        text = bz2.decompress(f.read(length)).decode("utf-8")
        with io.StringIO(text) as t:
            while (line := t.readline()):
                lines += 1
print(f"lines: {lines:,}")
