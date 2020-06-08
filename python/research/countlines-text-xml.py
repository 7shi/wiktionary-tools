import mediawiki_parse

target, spos, slen = mediawiki_parse.read()
getpages = mediawiki_parse.getpages_xml
lines = 0
with open(target, "rb") as f:
    f.seek(slen[0])
    for length in slen[1:-1]:
        for id, text in getpages(f.read(length)):
            for line in text():
                lines += 1
print(f"lines: {lines:,}")
