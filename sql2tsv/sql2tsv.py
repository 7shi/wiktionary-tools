test = False

def read_string(src, pos):
    length = len(src)
    if pos >= length or src[pos] != "'": return None
    pos += 1
    ret = ""
    while pos < length and src[pos] != "'":
        if src[pos] == "\\":
            pos += 1
            end = pos >= length
            if end or not src[pos] in "\"'\\":
                ret += "\\"
            if end: break
        ret += src[pos]
        pos += 1
    if pos < length and src[pos] == "'": pos += 1
    return (ret, pos)

if test:
    src = r"'a,b','c\'d'"
    pos = 0
    while pos < len(src):
        s, p = read_string(src, pos)
        print("read_string", (src, pos), "->", (s, p))
        pos = p + 1

def read_value(src, pos):
    length = len(src)
    if pos >= length: return None
    sp = read_string(src, pos)
    if sp: return sp
    p = pos
    while p < length and src[p] != "," and src[p] != ")":
        p += 1
    return (src[pos:p], p)

if test:
    for src in ["1,2,3", r"1,'a,b','c\'d'"]:
        pos = 0
        while (value := read_value(src, pos)):
            s, p = value
            print("read_value", (src, pos), "->", (s, p))
            pos = p + 1

def read_values(src, pos):
    length = len(src)
    if pos >= length or src[pos] != "(": return None
    pos += 1
    ret = []
    if pos < length and src[pos] != ")":
        while (value := read_value(src, pos)):
            s, pos = value
            ret.append(s)
            if pos >= length or src[pos] != ",": break
            pos += 1
    if pos < length and src[pos] == ")": pos += 1
    return (ret, pos)

if test:
    for src in [r"(1,2,3)", r"(1,'a,b','c\'d')"]:
        print("read_values", (src, 0), "->", read_values(src, 0))

def read_all_values(src, pos):
    length = len(src)
    while (sp := read_values(src, pos)):
        s, pos = sp
        yield s
        if pos >= length or src[pos] != ",": break
        pos += 1

if test:
    src = r"(1,2,3),(1,'a,b','c\'d')"
    print("read_all_values", (src, 0), "->", list(read_all_values(src, 0)))

def read_sql(stream):
    while (line := stream.readline()):
        if line.startswith("INSERT INTO "):
            p = line.find("VALUES (")
            if p >= 0: yield from read_all_values(line, p + 7)

if test:
    import io
    src = r"""
INSERT INTO `table` VALUES (1,2,3),(4,5,6);
INSERT INTO `table` VALUES (1,'a,b','c\'d');
""".strip()
    print("read_sql", (src,))
    print("->", list(read_sql(io.StringIO(src))))

if __name__ == "__main__":
    import gzip, sys
    try:
        target = sys.argv[1]
        openf = None
        if target.endswith(".sql"   ): openf =      open
        if target.endswith(".sql.gz"): openf = gzip.open
        if not openf: raise Exception("not supported: " + target)
    except Exception as e:
        print(e)
        print("usage: %s sql[.gz]" % sys.argv[0])
        exit(1)
    tsv = target[:target.rfind(".sql")] + ".tsv"
    with openf(target, "rt", encoding="utf-8", errors="replace") as fr:
        with open(tsv, "w", encoding="utf-8") as fw:
            for values in read_sql(fr):
                fw.write("\t".join(values))
                fw.write("\n")
