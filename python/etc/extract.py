import bz2, getopt, sys

try:
    opts, args = getopt.getopt(sys.argv[1:], "o:")
    block  = int(args[0])
    output = None
    for opt, optarg in opts:
        if opt == "-o": output = optarg
except Exception as e:
    print(e)
    print("usage: %s [-o file] block" % sys.argv[0])
    print("    -o: output raw compressed data to file")
    exit(1)

with open("streamlen.tsv") as f:
    target = f.readline().strip()
    slen = [int(line) for line in f.readlines()]

try:
    length = slen[block]
except Exception as e:
    print(e)
    print(f"range 0 to {len(slen) - 1}")
    exit(1)

with open(target, "rb") as f:
    f.seek(sum(slen[:block]))
    data = f.read(length)

if output:
    with open(output, "wb") as f:
        f.write(data)
else:
    print(bz2.decompress(data).decode("utf-8"))
