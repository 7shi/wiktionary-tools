import mediawiki_parse, re

target, _, slen = mediawiki_parse.read()
getpages = mediawiki_parse.getpages
results, langs = [], {}
with open(target, "rb") as f:
    pattern = re.compile("==([^=].*)==")
    f.seek(slen[0])
    for length in slen[1:-1]:
        for id, text in getpages(f.read(length)):
            for line in text:
                if (m := pattern.match(line)):
                    lang = m[1].strip()
                    if lang in langs:
                        lid = langs[lang]
                    else:
                        lid = len(langs) + 1
                        langs[lang] = lid
                    results.append((id, lid))

with open("output1.tsv", "w", encoding="utf-8") as f:
    for id, lid in results:
        f.write(f"{id}\t{lid}\n")

with open("output2.tsv", "w", encoding="utf-8") as f:
    for k, v in langs.items():
        f.write(f"{v}\t{k}\n")
