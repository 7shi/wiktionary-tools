import bz2, io, xml.etree.ElementTree as ET

def target_spos_slen(tsv):
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
    with io.StringIO(bz2.decompress(bz2data).decode("utf-8")) as t:
        ns, id = 0, 0
        while (line := t.readline()):
            line = line.lstrip()
            if line.startswith("<ns>"):
                ns = int(line[4:line.find("<", 4)])
            elif not id and line.startswith("<id>"):
                id = int(line[4:line.find("<", 4)])
            elif line.startswith("<text "):
                p = line.find(">")
                if line[p - 1] != "/":
                    if ns != 0:
                        while not line.endswith("</text>\n"):
                            line = t.readline()
                        continue
                    first = line[p + 1:]
                    def text():
                        line = first
                        while line:
                            if line.endswith("</text>\n"):
                                line = line[:-8]
                                if line: yield line
                                break
                            else:
                                yield line
                            line = t.readline()
                    yield id, text
                id = 0

def getpages_xml(bz2data):
    xml = bz2.decompress(bz2data).decode("utf-8")
    pages = ET.fromstring(f"<pages>{xml}</pages>")
    for page in pages:
        if int(page.find("ns").text) == 0:
            id = int(page.find("id").text)
            with io.StringIO(page.find("revision/text").text) as t:
                def text():
                    while (line := t.readline()):
                        yield line
                yield id, text
