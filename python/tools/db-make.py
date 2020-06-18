from mediawiki_parse import *
import bz2, re

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

def langcode(text):
    ret = {}
    pattern1 = re.compile(r'm\["(.+?)"\]')
    pattern2 = re.compile('"(.+?)"')
    while (line := entity(next(text, ""))):
        if (m1 := pattern1.match(line)):
            line = entity(next(text, ""))
            if (m2 := pattern2.search(line)):
                ret[m1[1]] = m2[1]
    return ret

NS_MAIN     =   0
NS_TEMPLATE =  10
NS_MODULE   = 828

def getlangs(arg):
    sid, data = arg
    pages, idlang, langdata, templates, redirects = [], [], {}, {}, []
    psub   = re.compile("==([^=].*)==")
    ptmpl1 = re.compile("<onlyinclude>(.*?)</onlyinclude>")
    ptmpl2 = re.compile("<noinclude>.*?</noinclude>")
    ptmpl3 = re.compile("<noinclude>.*")
    ptmpl4 = re.compile("</?includeonly>")
    for title, ns, id, rd, text in getpages(data):
        pages.append((id, sid, ns, title))
        if rd: redirects.append((id, ns, title, rd))
        if ns == NS_TEMPLATE:
            t = entity("".join(text)).replace("\n", "<br>").replace("\t", " ")
            if (m := ptmpl1.search(t)): t = m[1]
            t = ptmpl2.sub("", t)
            t = ptmpl3.sub("", t)
            t = ptmpl4.sub("", t)
            templates[removens(title)] = t
        elif ns == NS_MODULE and title.find(":languages/data") > 0:
            langdata[title] = langcode(text)
        if ns != NS_MAIN: continue
        langs = set()
        for line in text:
            if (m := psub.match(line)):
                lang = entity(m[1].strip())
                if not lang in langs:
                    langs.add(lang)
                    idlang.append((id, lang))
    return pages, idlang, langdata, templates, redirects

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
    def f(g):
        global spos
        for sid, slen, data in g:
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

    pages     = []
    titles    = {}
    idls      = []
    langdata  = {}
    templates = {}
    redirs    = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for pgs, idl, ld, tmpls, rds in executor.map(getlangs, f(getstreams(target))):
            pages += pgs
            for id, sid, ns, title in pgs:
                titles[title] = id
            idls += idl
            langdata .update(ld)
            templates.update(tmpls)
            redirs += rds
    sys.stderr.write("\n")

    sys.stderr.write("checking redirects...\n")
    redirects = {}
    for id, ns, title, rd in redirs:
        if (rdid := titles.get(rd, 0)):
            redirects[id] = rdid
            if ns == NS_TEMPLATE:
                if (t := templates.get(removens(rd), None)):
                    templates[removens(title)] = t

    sys.stderr.write("reading language codes...\n")
    langcode = {}
    templates2 = templates.copy()
    def addlangcode(page):
        if page in langdata:
            ld = langdata[page]
            langcode.update(ld)
            for code, name in ld.items():
                if not code in templates2:
                    templates2[code] = name
    module = namespaces[NS_MODULE]
    addlangcode(f"{module}:languages/data2")
    for i in range(ord("a"), ord("z") + 1):
        addlangcode(f"{module}:languages/data3/{chr(i)}")
    addlangcode(f"{module}:languages/datax")

    sys.stderr.write("checking language names...\n")
    idlang   = []
    langname = []
    langids  = {}
    aliases  = {}
    pcomment = re.compile("<!--.*?-->")
    pbracket = re.compile("{{{(.+?)}}}")
    ptempl   = re.compile("{{(.+?)}}")
    plink    = re.compile(r"\[\[(.+?)\]\]")
    prev     = 0
    lids     = set()
    for id, lang in idls:
        lid = aliases.get(lang, 0)
        if lid == 0:
            lang2 = replace(templates2, lang)
            if lang2 in langids:
                lid = langids[lang2]
            else:
                lid = len(langname) + 1
                langname.append([lang2])
                langids [lang2] = lid
            if lang != lang2:
                langname[lid - 1].append(lang)
            aliases[lang] = lid
        if prev != id:
            prev = id
            lids = set()
        if not lid in lids:
            lids.add(lid)
            idlang.append((id, lid))

    sys.stderr.write("writing DB files...\n")
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
            rd = redirects.get(id, 0)
            f.write(f"{id}\t{sid}\t{ns}\t{rd}\t{title}\n")
    with open("db-idlang.tsv", "w", encoding="utf-8") as f:
        for id, lid in idlang:
            f.write(f"{id}\t{lid}\n")
    with open("db-langname.tsv", "w", encoding="utf-8") as f:
        for lid, names in enumerate(langname):
            for no, name in enumerate(names):
                f.write(f"{lid + 1}\t{no}\t{name}\n")
    with open("db-langcode.tsv", "w", encoding="utf-8") as f:
        for code, name in langcode.items():
            f.write(f"{code}\t{name}\n")
    with open("db-templates.tsv", "w", encoding="utf-8") as f:
        for title, include in templates.items():
            f.write(f"{title}\t{include}\n")
