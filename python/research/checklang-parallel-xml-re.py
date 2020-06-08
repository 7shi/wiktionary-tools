import mediawiki_parse, re

getpages = mediawiki_parse.getpages_xml

def getlangs(args):
    target, pos, length = args
    with open(target, "rb") as f:
        f.seek(pos)
        bz2data = f.read(length)
    result = []
    for id, text in getpages(bz2data):
        for line in text():
            if (m := re.match("==([^=].*)==", line)):
                result.append((id, m[1].strip()))
    return result

if __name__ == "__main__":
    import concurrent.futures

    target, spos, slen = mediawiki_parse.read()
    slen.pop()
    split = 10
    poslens = [(target, spos[i], sum(slen[i : i + split]))
               for i in range(1, len(slen), split)]

    results, langs = [], {}
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for result in executor.map(getlangs, poslens):
            for id, lang in result:
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
        ls = list(langs.items())
        ls.sort(key=lambda kv: kv[1])
        for k, v in ls:
            f.write(f"{v}\t{k}\n")
