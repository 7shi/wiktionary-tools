import bz2, xml.etree.ElementTree as ET

with open("streamlen.tsv") as f:
    target = f.readline().strip()
    slen = [int(line) for line in f.readlines()]

class XMLTarget:
    def __init__(self):
        self._ns   = 0
        self._id   = 0
        self._data = []
        self.pages = []

    def start(self, tag, attrib):
        self._data = []

    def data(self, data):
        self._data.append(data)

    def end(self, tag):
        if tag == "ns":
            self._ns = int(self._data[0])
            self._id = 0
        elif self._id == 0 and tag == "id":
            self._id = int(self._data[0])
        elif self._ns == 0 and tag == "text":
            text = []
            cur = ""
            for d in self._data:
                if d == "\n":
                    text.append(cur)
                    cur = ""
                else:
                    cur += d
            if cur: text.append(cur)
            self.pages.append((self._id, text))
        self._data = []

def getpages(bz2data):
    target = XMLTarget()
    parser = ET.XMLParser(target=target)
    parser.feed("<pages>")
    parser.feed(bz2.decompress(bz2data).decode("utf-8"))
    return target.pages

lines = 0
with open(target, "rb") as f:
    f.seek(slen[0])
    for length in slen[1:-1]:
        for id, text in getpages(f.read(length)):
            for line in text:
                lines += 1
print(f"lines: {lines:,}")
