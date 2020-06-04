import bz2, io

def getlines(bz2data):
    text = bz2.decompress(bz2data).decode("utf-8")
    with io.StringIO(text) as t:
        while (line := t.readline()):
            yield line
    yield ""

def getpages(bz2data):
    ns = 0
    id = 0
    revision = False
    lines = getlines(bz2data)
    while (line := next(lines)):
        line = line.lstrip()
        if line.startswith("<ns>"):
            ns = int(line[4:line.find("<", 4)])
        elif not revision and line.startswith("<id>"):
            id = int(line[4:line.find("<", 4)])
        elif line.startswith("<revision>"):
            revision = True
        elif line.startswith("<text "):
            revision = False
            p = line.find(">")
            if line[p - 1] == "/": continue
            if ns != 0:
                while not line.endswith("</text>\n"):
                    line = next(lines)
                continue
            first = line[p + 1:]
            def text():
                line = first
                while line:
                    if line.endswith("</text>\n"):
                        line = line[:-8]
                        if line: yield line
                        break
                    else:
                        yield line
                    line = next(lines)
            yield id, text

def getlangs(args):
    target, pos, length = args
    with open(target, "rb") as f:
        f.seek(pos)
        bz2data = f.read(length)
    result = []
    for id, text in getpages(bz2data):
        for line in text():
            if line.startswith("==") and not line.startswith("==="):
                lang = line[2:].strip()
                e = len(lang) - 1
                while e > 0 and lang[e] == '=': e -= 1
                result.append((id, lang[: e + 1].strip()))
    return result

if __name__ == "__main__":
    import concurrent.futures

    spos, slen = [], []
    with open("streamlen.tsv") as f:
        target = f.readline().strip()
        pos = 0
        while (line := f.readline()):
            length = int(line)
            spos.append(pos)
            slen.append(length)
            pos += length
    slen.pop()
    split = 10
    poslens = [(target, spos[i], sum(slen[i : i + split]))
               for i in range(1, len(slen), split)]

    results, langs = [], {}
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for i, result in enumerate(executor.map(getlangs, poslens)):
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
