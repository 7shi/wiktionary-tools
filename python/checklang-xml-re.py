import bz2, io, re, xml.etree.ElementTree as ET

with open("streamlen.tsv") as f:
    target = f.readline().strip()
    slen = [int(line) for line in f.readlines()]

def getpages(bz2data):
    xml = bz2.decompress(bz2data).decode("utf-8")
    pages = ET.fromstring(f"<pages>{xml}</pages>")
    for page in pages:
        if int(page.find("ns").text) == 0:
            id = int(page.find("id").text)
            with io.StringIO(page.find("revision/text").text) as t:
                def text():
                    while (line := t.readline()):
                        yield line
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
