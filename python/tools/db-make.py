import mediawiki_parse, bz2, re

def getstreams(target):
    size = 1024 * 1024  # 1MB
    sid = 0
    with open(target, "rb") as f:
        decompressor = bz2.BZ2Decompressor()
        slen  = 0
        data1 = b''
        data2 = b''
        while data1 or (data1 := f.read(size)):
            len1 = len(data1)
            data2 += decompressor.decompress(data1)
            data1  = decompressor.unused_data
            slen  += len1 - len(data1)
            if decompressor.eof:
                yield sid, slen, data2
                sid  += 1
                slen  = 0
                data2 = b''
                decompressor = bz2.BZ2Decompressor()

def getlangs(arg):
    sid, data = arg
    pages, idlang = [], []
    pattern = re.compile("==([^=].*)==")
    for title, id, ns, text in mediawiki_parse.getpages(data):
        pages.append((id, sid, ns, title))
        if not text: continue
        langs = set()
        for line in text:
            if (m := pattern.match(line)):
                lang = m[1].strip()
                if not lang in langs:
                    langs.add(lang)
                    idlang.append((id, lang))
    return pages, idlang

if __name__ == "__main__":
    import concurrent.futures, os, sys, xml.etree.ElementTree as ET

    try:
        target = sys.argv[1]
    except:
        sys.stderr.write(f"usage: {sys.argv[0]} multistream.xml.bz2\n")
        exit(1)

    spos       = 0
    targetlen  = os.path.getsize(target)
    streams    = []
    namespaces = {}
    pages      = []
    idlang     = []
    langname   = {}

    def f():
        global spos
        for sid, slen, data in getstreams(target):
            streams.append((sid, spos, slen))
            spos += slen
            sys.stderr.write(f"\r{spos:,} / {targetlen:,} | {sid:,}")
            sys.stderr.flush()
            if sid == 0:
                text = data.decode("utf-8")
                xml = ET.fromstring(text[text.find("\n") + 1:])
                for namespace in xml.find("namespaces"):
                    namespaces[int(namespace.attrib["key"])] = namespace.text
            elif slen > 100:
                yield sid, data

    with concurrent.futures.ProcessPoolExecutor() as executor:
        for pgs, idl in executor.map(getlangs, f()):
            pages += pgs
            for id, lang in idl:
                if lang in langname:
                    lid = langname[lang]
                else:
                    lid = len(langname) + 1
                    langname[lang] = lid
                idlang.append((id, lid))

    sys.stderr.write("\nwriting DB files...\n")

    with open("db-settings.tsv", "w", encoding="utf-8") as f:
        f.write(f"target\t{target}\n")

    with open("db-streams.tsv", "w", encoding="utf-8") as f:
        for sid, spos, slen in streams:
            f.write(f"{sid}\t{spos}\t{slen}\n")

    with open("db-namespaces.tsv", "w", encoding="utf-8") as f:
        for ns, nsname in namespaces.items():
            f.write(f"{ns}\t{nsname}\n")

    with open("db-pages.tsv", "w", encoding="utf-8") as f:
        for id, sid, ns, title in pages:
            f.write(f"{id}\t{sid}\t{ns}\t{title}\n")

    with open("db-idlang.tsv", "w", encoding="utf-8") as f:
        for id, lid in idlang:
            f.write(f"{id}\t{lid}\n")

    with open("db-langname.tsv", "w", encoding="utf-8") as f:
        for name, lid in langname.items():
            f.write(f"{lid}\t{name}\n")
