import io, re, sqlite3, xml.etree.ElementTree as ET

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

pattern1 = re.compile('<([a-z]+).*?>(.+)</')
pattern2 = re.compile('<redirect title="(.+?)"')

def getpages(data):
    with io.StringIO(data.decode("utf-8")) as t:
        title, ns, id, rd = "", 0, 0, None
        while (line := t.readline()):
            line = line.lstrip()
            if (m := pattern1.match(line)):
                tag = m[1]
                if tag == "title":
                    title = entity(m[2])
                elif tag == "ns":
                    ns = int(m[2])
                    id = 0
                    rd = None
                elif id == 0 and tag == "id":
                    id = int(m[2])
                elif tag == "text":
                    yield title, ns, id, rd, iter([m[2]])
            elif (m := pattern2.match(line)):
                rd = entity(m[1])
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
                yield title, ns, id, rd, text
                for _ in text: pass

def getpages_xml(data):
    xml = data.decode("utf-8")
    pages = ET.fromstring(f"<pages>{xml}</pages>")
    for page in pages:
        title = page.find("title").text
        redir = page.find("redirect")
        rd = redir.attrib["title"] if redir else None
        ns = int(page.find("ns").text)
        id = int(page.find("id").text)
        with io.StringIO(page.find("revision/text").text) as text:
            yield title, ns, id, rd, text

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
    return (s.replace("&quot;", '"')
             .replace("&lt;", "<")
             .replace("&gt;", ">")
             .replace("&amp;", "&")
             .replace("&#039;", "'"))

def removens(t):
    i = t.find(":")
    return t if i < 0 else t[i + 1:]

pcomment = re.compile("<!--.*?-->")
pbracket = re.compile("{{{.+?}}}")
plink    = re.compile(r"\[\[(.+?)\]\]")

def replace(templates, s):
    s = pcomment.sub("", s)
    s = pbracket.sub("", s)
    while (m := plink.search(s)):
        s = s[:m.start()] + m[1].split("|")[-1] + s[m.end():]
    def f(s):
        start = s.find("{{")
        if start < 0: return s
        s2 = f(s[start + 2:])
        end = s2.find("}}")
        if end < 0:
            return s[:start + 2] + s2
        s3 = s2[:end].split("|")
        if len(s3) > 1:
            s4 = s3[-1]
        else:
            t = templates.get(s3[0], None)
            if t:
                s4 = replace(templates, t)
            else:
                start += 2
                s4 = s2[:end + 2]
        return s[:start] + s4 + f(s2[end + 2:])
    return f(s)
