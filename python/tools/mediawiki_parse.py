import io, sqlite3, xml.etree.ElementTree as ET

def target_spos_slen(db):
    with open(db, "rb") as f: pass
    with sqlite3.connect(db) as conn:
        cur = conn.cursor()
        target = cur.execute("SELECT value FROM settings WHERE key = 'target'").fetchone()[0]
        spos, slen = [], []
        for r in cur.execute("SELECT sid, spos, slen FROM streams"):
            spos.append(r[1])
            slen.append(r[2])
    return target, spos, slen

def getpages(data):
    with io.StringIO(data.decode("utf-8")) as t:
        title, ns, id = "", 0, 0
        while (line := t.readline()):
            line = line.lstrip()
            if line.startswith("<title>"):
                title = entity(line[7:line.find("<", 7)])
            elif line.startswith("<ns>"):
                ns = int(line[4:line.find("<", 4)])
                id = 0
            elif id == 0 and line.startswith("<id>"):
                id = int(line[4:line.find("<", 4)])
            elif line.startswith("<text "):
                p = line.find(">")
                if line[p - 1] == "/": continue
                first = line[p + 1:]
                def f():
                    line = first
                    while line:
                        if line.endswith("</text>\n"):
                            line = line[:-8]
                            if line: yield line
                            break
                        else:
                            yield line
                        line = t.readline()
                text = f()
                yield title, id, ns, text
                for _ in text: pass

def getpages_xml(data):
    xml = data.decode("utf-8")
    pages = ET.fromstring(f"<pages>{xml}</pages>")
    for page in pages:
        title = page.find("title").text
        ns = int(page.find("ns").text)
        id = int(page.find("id").text)
        with io.StringIO(page.find("revision/text").text) as text:
            yield title, id, ns, text

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

def entity(s):
    if s.find("&") < 0: return s
    return s.replace("&quot;", '"').replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
