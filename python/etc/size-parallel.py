import bz2, io

def getlength(args):
    target, pos, length = args
    with open(target, "rb") as f:
        f.seek(pos)
        bz2data = f.read(length)
    data  = bz2.decompress(bz2data)
    text  = data.decode("utf-8")
    lines = 0
    with io.StringIO(text) as f:
        while (_ := f.readline()):
            lines  += 1
    return { "bytes": len(data), "chars": len(text), "lines": lines }

if __name__ == "__main__":
    import concurrent.futures

    spos, slen = [], []
    with open("streamlen.tsv") as f:
        target = f.readline().strip()
        pos = 0
        while (line := f.readline()):
            length = int(line)
            spos.append(pos)
            slen.append(length)
            pos += length
    split = 10
    poslens = [(target, spos[i], sum(slen[i : i + split]))
               for i in range(0, len(slen), split)]

    sums = { "streams": len(spos) }
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for result in executor.map(getlength, poslens):
            for k, v in result.items():
                if not k in sums: sums[k] = 0
                sums[k] += v
    print(", ".join([f"{k}: {v:,}" for k, v in sums.items()]))
