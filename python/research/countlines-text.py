import bz2, io

with open("streamlen.tsv") as f:
    target = f.readline().strip()
    slen = [int(line) for line in f.readlines()]

def getpages(bz2data):
    with io.StringIO(bz2.decompress(bz2data).decode("utf-8")) as t:
        ns, id = 0, 0
        while (line := t.readline()):
            line = line.lstrip()
            if line.startswith("<ns>"):
                ns = int(line[4:line.find("<", 4)])
                id = 0
            elif id == 0 and line.startswith("<id>"):
                id = int(line[4:line.find("<", 4)])
            elif line.startswith("<text "):
                p = line.find(">")
                if line[p - 1] == "/": continue
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

lines = 0
with open(target, "rb") as f:
    f.seek(slen[0])
    for length in slen[1:-1]:
        for id, text in getpages(f.read(length)):
            for line in text():
                lines += 1
print(f"lines: {lines:,}")
