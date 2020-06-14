import mediawiki_parse

target, _, slen = mediawiki_parse.read()
getpages = mediawiki_parse.getpages
results, langs = [], {}
with open(target, "rb") as f:
    f.seek(slen[0])
    for length in slen[1:-1]:
        for id, text in getpages(f.read(length)):
            for line in text:
                if line.startswith("==") and not line.startswith("==="):
                    lang = line[2:].strip()
                    e = len(lang) - 1
                    while e > 0 and lang[e] == '=': e -= 1
                    lang = lang[: e + 1].strip()
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
