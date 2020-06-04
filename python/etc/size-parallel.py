import bz2, concurrent.futures, io, sys, threading

para = 1
if len(sys.argv) > 1:
    para = min(256, max(1, int(sys.argv[1])))

slen = []
with open("streamlen.tsv") as f:
    target = f.readline().strip()
    while (line := f.readline()):
        slen.append(int(line))

with open(target, "rb") as f:
    lock = threading.Lock()
    def getstream():
        lock.acquire()
        ret = f.read(slen.pop(0)) if slen else None
        lock.release()
        return ret

    def getlength():
        streams = 0
        bytes   = 0
        chars   = 0
        lines   = 0
        while (bz2data := getstream()):
            data = bz2.decompress(bz2data)
            text = data.decode("utf-8")
            streams += 1
            bytes   += len(data)
            chars   += len(text)
            with io.StringIO(text) as f:
                while (line := f.readline()):
                    lines  += 1
        return {"streams": streams,
                "bytes"  : bytes,
                "chars"  : chars,
                "lines"  : lines}

    executor = concurrent.futures.ThreadPoolExecutor()
    futures = [executor.submit(getlength) for _ in range(para)]
    results = [future.result() for future in futures]
    executor.shutdown()
    print(results)
    sums = {}
    for r in results:
        for k, v in r.items():
            if not k in sums: sums[k] = 0
            sums[k] += v
    print(", ".join([f"{k}: {v:,}" for k, v in sums.items()]))
