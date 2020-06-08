import bz2, io

with open("streamlen.tsv") as f:
    target = f.readline().strip()
    slen = [int(line) for line in f.readlines()]

lines = 0
with open(target, "rb") as f:
    for length in slen:
        text = bz2.decompress(f.read(length)).decode("utf-8")
        with io.StringIO(text) as t:
            while (line := t.readline()):
                lines += 1
print(f"lines: {lines:,}")
