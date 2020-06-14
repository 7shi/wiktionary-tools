import bz2, io, os, re, sys, xml.etree.ElementTree as ET

try:
    target = sys.argv[1]
except:
    sys.stderr.write(f"usage: {sys.argv[0]} multistream.xml.bz2\n")
    exit(1)

def get_streams():
    size = 1024 * 1024  # 1MB
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
                yield slen, data2.decode("utf-8")
                slen  = 0
                data2 = b''
                decompressor = bz2.BZ2Decompressor()

spos       = 0
streams    = []
namespaces = {}
pages      = []
idlang     = []
langname   = {}
targetlen  = os.path.getsize(target)
pattern    = re.compile("==([^=].*)==")
for sid, (slen, data) in enumerate(get_streams()):
    streams.append((sid, spos, slen))
    spos += slen
    sys.stderr.write(f"\r{spos:,} / {targetlen:,} | {sid:,}")
    sys.stderr.flush()
    if sid == 0:
        xml = ET.fromstring(data[data.find("\n") + 1:])
        for namespace in xml.find("namespaces"):
            namespaces[int(namespace.attrib["key"])] = namespace.text
    elif len(data) < 20 and data.strip().startswith("</"):
        pass
    else:
        xml = ET.fromstring(f"<pages>{data}</pages>")
        for page in xml:
            title = page.find("title").text
            ns = int(page.find("ns").text)
            id = int(page.find("id").text)
            pages.append((id, sid, ns, title))
            if ns != 0: continue
            langs = set()
            with io.StringIO(page.find("revision/text").text) as t:
                for line in t:
                    if (m := pattern.match(line)):
                        lang = m[1].strip()
                        if lang in langs: continue
                        langs.add(lang)
                        if lang in langname:
                            lid = langname[lang]
                        else:
                            lid = len(langname) + 1
                            langname[lang] = lid
                        idlang.append((id, lid))
sys.stderr.write("\n")
with open("db.sql", "w", encoding="utf-8") as sql:
    sql.write(r"""
.mode ascii
.separator "\t" "\n"
""".lstrip())
    with open("db-settings.tsv", "w", encoding="utf-8") as f:
        f.write(f"target\t{target}\n")
    sql.write(r"""
.print importing \'db-settings.tsv\'...
CREATE TABLE settings(key TEXT PRIMARY KEY, value TEXT);
.import db-settings.tsv settings
""")
    with open("db-streams.tsv", "w", encoding="utf-8") as f:
        for sid, spos, slen in streams:
            f.write(f"{sid}\t{spos}\t{slen}\n")
    sql.write(r"""
.print importing \'db-streams.tsv\'...
CREATE TABLE streams(sid INTEGER PRIMARY KEY, spos INTEGER, slen INTEGER);
.import db-streams.tsv streams
""")
    with open("db-namespaces.tsv", "w", encoding="utf-8") as f:
        for ns, nsname in namespaces.items():
            f.write(f"{ns}\t{nsname}\n")
    sql.write(r"""
.print importing \'db-namespaces.tsv\'...
CREATE TABLE namespaces(ns INTEGER PRIMARY KEY, nsname TEXT);
.import db-namespaces.tsv namespaces
""")
    with open("db-pages.tsv", "w", encoding="utf-8") as f:
        for id, sid, ns, title in pages:
            f.write(f"{id}\t{sid}\t{ns}\t{title}\n")
    sql.write(r"""
.print importing \'db-pages.tsv\'...
CREATE TABLE pages(id INTEGER PRIMARY KEY, sid INTEGER, ns INTEGER, title TEXT);
.import db-pages.tsv pages
CREATE INDEX pages_sid_idx   ON pages(sid);
CREATE INDEX pages_ns_idx    ON pages(ns);
CREATE INDEX pages_title_idx ON pages(title);
""")
    with open("db-idlang.tsv", "w", encoding="utf-8") as f:
        for id, lid in idlang:
            f.write(f"{id}\t{lid}\n")
    sql.write(r"""
.print importing \'db-idlang.tsv\'...
CREATE TABLE idlang(id INTEGER, lid INTEGER, PRIMARY KEY(id, lid));
.import db-idlang.tsv idlang
CREATE INDEX idlang_id_idx  ON idlang(id);
CREATE INDEX idlang_lid_idx ON idlang(lid);
""")
    with open("db-langname.tsv", "w", encoding="utf-8") as f:
        for name, lid in langname.items():
            f.write(f"{lid}\t{name}\n")
    sql.write(r"""
.print importing \'db-langname.tsv\'...
CREATE TABLE langname(lid INTEGER PRIMARY KEY, name TEXT);
.import db-langname.tsv langname
CREATE INDEX langname_name_idx ON langname(name);
""")
