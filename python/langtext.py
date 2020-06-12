import bz2, io, re, xml.etree.ElementTree as ET

def read(tsv="streamlen.tsv"):
    spos, slen = [], []
    with open(tsv) as f:
        target = f.readline().strip()
        pos = 0
        while (line := f.readline()):
            length = int(line)
            spos.append(pos)
            slen.append(length)
            pos += length
    return target, spos, slen

def getpages(bz2data):
    xml = bz2.decompress(bz2data).decode("utf-8")
    pages = ET.fromstring(f"<pages>{xml}</pages>")
    for page in pages:
        if int(page.find("ns").text) == 0:
            title = page.find("title").text
            id = int(page.find("id").text)
            with io.StringIO(page.find("revision/text").text) as text:
                yield id, title, text

def splittext(pattern, text):
    line = next(text, "")
    while line:
        m = pattern.match(line)
        line = next(text, "")
        if m:
            def g():
                nonlocal line
                while line and not pattern.match(line):
                    yield line
                    line = next(text, "")
            yield m[1].strip(), g()

def langtext(args):
    langs, target, pos, length = args
    with open(target, "rb") as f:
        f.seek(pos)
        bz2data = f.read(length)
    pattern = re.compile("==([^=].*)==")
    result = {}
    for lang in langs: result[lang] = []
    for id, title, text in getpages(bz2data):
        for lang, text2 in splittext(pattern, text):
            if lang in langs:
                result[lang].append((title, list(text2)))
    return result

if __name__ == "__main__":
    import concurrent.futures, sys

    if len(sys.argv) <= 1:
        print(f"usage: {sys.argv[0]} Language")
        exit(1)
    langs = sys.argv[1:]

    target, spos, slen = read()
    slen.pop()
    split = 10
    poslens = [(langs, target, spos[i], sum(slen[i : i + split]))
               for i in range(1, len(slen), split)]

    class LangData:
        def __init__(self):
            self.words = {}
            self.texts = []
    langdata = {}
    for lang in langs: langdata[lang] = LangData()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for i, result in enumerate(executor.map(langtext, poslens)):
            sys.stdout.write(f"\r{i + 1:,} / {len(poslens):,}")
            sys.stdout.flush()
            for lang in langs:
                ld = langdata[lang]
                rs = result[lang]
                index = len(ld.texts)
                ld.texts += rs
                for i, r in enumerate(rs):
                    word = r[0].lower().replace("-", "")
                    ld.words[word] = index + i
    print()
    for lang in langs:
        ld = langdata[lang]
        print(f"{lang}: {len(ld.texts):,}")
        with open(f"{lang}.txt", "w", encoding="utf-8") as f:
            for i, w in enumerate(sorted(ld.words.keys())):
                if i > 0: f.write("\n")
                word, text = ld.texts[ld.words[w]]
                f.write(f"=={word}==\n\n")
                first = True
                nl = 0
                for line in text:
                    if line == "\n":
                        nl += 1
                    else:
                        if nl > 0:
                            if first:
                                first = False
                            else:
                                f.write("\n" * nl)
                            nl = 0
                        f.write(line)
                        if not line.endswith("\n"):
                            f.write("\n")
