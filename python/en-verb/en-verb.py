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

def en_verb(args):
    target, pos, length = args
    with open(target, "rb") as f:
        f.seek(pos)
        bz2data = f.read(length)
    pattern1 = re.compile("==([^=].*)==")
    pattern2 = re.compile("===+([^=].*?)===")
    result = []
    for id, title, text in getpages(bz2data):
        if " " in title or "-" in title: continue
        for lang, text2 in splittext(pattern1, text):
            if lang != "English": continue
            for subsub, text3 in splittext(pattern2, text2):
                if subsub != "Verb": continue
                for line in text3:
                    if line.startswith("{{en-verb"):
                        result.append((id, title, line.strip()))
                        break
    return result

if __name__ == "__main__":
    import concurrent.futures, sys

    target, spos, slen = read()
    slen.pop()
    split = 10
    poslens = [(target, spos[i], sum(slen[i : i + split]))
               for i in range(1, len(slen), split)]

    results = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for i, result in enumerate(executor.map(en_verb, poslens)):
            sys.stdout.write(f"\r{i + 1:,} / {len(poslens):,}")
            sys.stdout.flush()
            results += result
    print()

    with open("en-verb.tsv", "w", encoding="utf-8") as f:
        for id, title, forms in results:
            f.write(f"{id}\t{title}\t{forms}\n")
