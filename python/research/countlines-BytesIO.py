import bz2, io

with open("streamlen.tsv") as f:
    target = f.readline().strip()
    slen = [int(line) for line in f.readlines()]

lines = 0
with open(target, "rb") as f:
    for length in slen:
        bz2data = f.read(length)
        with io.BytesIO(bz2data) as b:
            with bz2.open(b, "rt", encoding="utf-8") as t:
                while (_ := t.readline()):
                    lines += 1
print(f"lines: {lines:,}")
