import bz2, io

with open("streamlen.tsv") as f:
    target = f.readline().strip()
    slen = [int(line) for line in f.readlines()]

def getlines(bz2data):
    text = bz2.decompress(bz2data).decode("utf-8")
    with io.StringIO(text) as t:
        while (line := t.readline()):
            yield line
    yield ""

lines = 0
with open(target, "rb") as f:
    for length in slen:
        it = getlines(f.read(length))
        while (_ := next(it)):
            lines += 1
print(f"lines: {lines:,}")
