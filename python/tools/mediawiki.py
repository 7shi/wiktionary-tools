import bz2, functools, getopt, io, os, sqlite3, sys, xml.etree.ElementTree as ET

options = "o:xi"
def usage():
    print("[usage] %s [-o file] [-x] [-i] db (-s | title)" % sys.argv[0])
    print("    -o output to file")
    print("    -x XML <page>")
    print("    -s XML <siteinfo>")
    print("    -i search by id")
    exit(1)

class DB:
    def __init__(self, db):
        with open(db, "rb") as f: pass
        self.conn   = sqlite3.connect(db)
        self.cur    = self.conn.cursor()
        self.target = self.setting("target")
        self.ns     = {}
        self.max    = self.cur.execute("SELECT MAX(id ) FROM pages  ").fetchone()[0]
        self.bmax   = self.cur.execute("SELECT MAX(sid) FROM streams").fetchone()[0] - 1
        for ns in self.pages(0).find("siteinfo/namespaces"):
            key = ns.get("key")
            if key: self.ns[int(key)] = ns.text

    def setting(self, key: str) -> str:
        result = self.cur.execute(
            "SELECT value FROM settings WHERE key = ?", (key,)).fetchone()
        if not result: raise Exception(f'Can not find "{key}" in DB.')
        return result[0]

    @functools.lru_cache
    def langcode(self, code):
        result = self.cur.execute(
            "SELECT name FROM langcode WHERE code = ?", (code,)).fetchone()
        return result[0] if result else None

    @functools.lru_cache
    def langid(self, lang):
        result = self.cur.execute(
            "SELECT lid FROM langname WHERE name = ?", (lang,)).fetchone()
        return result[0] if result else None

    @functools.lru_cache(maxsize=10000)
    def index_block(self, title):
        result = self.cur.execute(
            "SELECT id, sid FROM pages WHERE title = ?", (title,)).fetchone()
        return result if result else (None, None)

    @functools.lru_cache(maxsize=10000)
    def block_title(self, id):
        result = self.cur.execute(
            "SELECT sid, title FROM pages WHERE id = ?", (id,)).fetchone()
        return result if result else (None, None)

    @functools.lru_cache(maxsize=1000)
    def pages(self, blockid):
        result = self.cur.execute(
            "SELECT spos, slen FROM streams WHERE sid = ?", (blockid,)).fetchone()
        if not result: return None
        start, length = result
        with open(self.target, "rb") as f:
            f.seek(start)
            block = f.read(length)
        data = bz2.decompress(block)
        xml = data.decode(encoding="utf-8")
        if blockid == 0: xml = xml[xml.find("\n"):]
        xml = "<mediawiki>" + xml + "</mediawiki>"
        return ET.fromstring(xml)

    @functools.lru_cache(maxsize=10000)
    def __getitem__(self, id_or_title):
        if type(id_or_title) is int:
            id = id_or_title
            block, title = self.block_title(id)
        else:
            title = id_or_title
            id, block = self.index_block(title)
        if not block: return None
        return Page(self, self.pages(block).find("page/[id='%s']" % id), id, title)

class Page:
    def __init__(self, db, page, id=None, title=None):
        self.id        = id or int(page.find("id"   ).text)
        self.title     = title or  page.find("title").text
        self.xml       = page
        self.text      = page.find("revision/text").text or ""
        self.ns        = int(page.find("ns").text)
        self.namespace = db.ns[self.ns]

def to_xml(elem):
    with io.BytesIO() as f:
        tree = ET.ElementTree(elem)
        tree.write(f, encoding="utf-8")
        return f.getvalue().decode(encoding="utf-8")

if __name__ == "__main__":
    index = None
    xml = False
    try:
        opts, [f, title] = getopt.getopt(sys.argv[1:], options)
    except Exception as e:
        print(e)
        usage()
    output = None
    idmode = False
    for opt, optarg in opts:
        if   opt == "-o": output = optarg
        elif opt == "-x": xml    = True
        elif opt == "-i": idmode = True
    db = DB(f)
    if title == "-s":
        text = to_xml(db.pages(0))
    else:
        page = db[int(title) if idmode else title]
        if not page:
            print("page not found:", title)
            exit(1)
        text = to_xml(page.xml) if xml else page.text
    if text and not text.endswith("\n"): text += "\n"
    if output:
        with open(output, "w", encoding="utf-8") as f:
            f.write(text)
    else:
        sys.stdout.write(text)
