import bz2, io, re

with open("streamlen.tsv") as f:
    target = f.readline().strip()
    slen = [int(line) for line in f.readlines()]

def getpages(bz2data):
    ns = 0
    id = 0
    revision = False
    with io.StringIO(bz2.decompress(bz2data).decode("utf-8")) as t:
        while (line := t.readline()):
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
                        line = t.readline()
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
                        line = t.readline()
                yield id, text

results, langs = [], {}
with open(target, "rb") as f:
    f.seek(slen[0])
    for length in slen[1:-1]:
        for id, text in getpages(f.read(length)):
            for line in text():
                if (m := re.match("==([^=].*)==", line)):
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
    ls = list(langs.items())
    ls.sort(key=lambda kv: kv[1])
    for k, v in ls:
        f.write(f"{v}\t{k}\n")
