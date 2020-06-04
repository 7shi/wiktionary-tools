import bz2, io

with open("streamlen.tsv") as f:
    target = f.readline().strip()
    slen = [int(line) for line in f.readlines()]

lines = 0
with open(target, "rb") as f:
    for length in slen:
        bz2data = f.read(length)
        text = bz2.decompress(bz2data).decode("utf-8")
        with io.StringIO(text) as t:
            while (_ := t.readline()):
                lines += 1
print(f"lines: {lines:,}")
