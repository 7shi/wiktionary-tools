import mediawiki_parse, re

getpages = mediawiki_parse.getpages

def getlangs(args):
    target, pos, length = args
    with open(target, "rb") as f:
        f.seek(pos)
        bz2data = f.read(length)
    result = []
    for id, text in getpages(bz2data):
        entities = set()
        for line in text():
            if (m := re.search("&([A-Za-z]+);", line)):
                entities.add(m[1])
        for entity in entities:
            result.append((id, entity))
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

    with open("entity1.tsv", "w", encoding="utf-8") as f:
        for id, lid in results:
            f.write(f"{id}\t{lid}\n")

    with open("entity2.tsv", "w", encoding="utf-8") as f:
        for k, v in langs.items():
            f.write(f"{v}\t{k}\n")
