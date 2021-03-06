import bz2, io, xml.etree.ElementTree as ET

with open("streamlen.tsv") as f:
    target = f.readline().strip()
    slen = [int(line) for line in f.readlines()]

def getpages(bz2data):
    xml = bz2.decompress(bz2data).decode("utf-8")
    parser = ET.XMLPullParser()
    parser.feed("<pages>")
    parser.feed(xml)
    ns, id = 0, 0
    for ev, el in parser.read_events():
        if el.tag == "ns":
            ns = int(el.text)
            id = 0
        elif id == 0 and el.tag == "id":
            id = int(el.text)
        elif ns == 0 and el.tag == "text":
            with io.StringIO(el.text) as text:
                yield id, text

lines = 0
with open(target, "rb") as f:
    f.seek(slen[0])
    for length in slen[1:-1]:
        for id, text in getpages(f.read(length)):
            for line in text:
                lines += 1
print(f"lines: {lines:,}")
