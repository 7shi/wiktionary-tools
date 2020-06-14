import mediawiki_parse, bz2, io, re, xml.etree.ElementTree as ET

def langtext(args):
    langs, target, pos, length = args
    with open(target, "rb") as f:
        f.seek(pos)
        bz2data = f.read(length)
    pattern = re.compile("==([^=].*)==")
    result = {}
    for lang in langs: result[lang] = []
    for title, id, ns, text in mediawiki_parse.getpages_xml(bz2.decompress(bz2data)):
        if not text: continue
        for lang, text2 in mediawiki_parse.splittext(pattern, text):
            if lang in langs:
                result[lang].append((title, "".join(text2).strip()))
    return result

if __name__ == "__main__":
    import concurrent.futures, sqlite3, sys

    try:
        db, *langs = sys.argv[1:]
        if not langs: raise Exception
    except:
        sys.stderr.write(f"usage: {sys.argv[0]} db Language ...\n")
        exit(1)

    with open(db, "rb") as f: pass
    with sqlite3.connect(db) as conn:
        cur = conn.cursor()

        lids, notfound = [], []
        for lang in langs:
            lid = cur.execute("SELECT lid FROM langname WHERE name = ?", (lang,)).fetchone()
            if lid:
                lids.append(lid[0])
            else:
                notfound.append(lang)
        if notfound:
            sys.stderr.write(f"not found: {', '.join(notfound)}\n")
            exit(1)

        target = cur.execute("SELECT value FROM settings WHERE key = 'target'").fetchone()[0]

        sql = """
            SELECT %%s FROM streams
            INNER JOIN pages ON streams.sid = pages.sid
            INNER JOIN idlang ON pages.id = idlang.id
            WHERE lid IN (%s)
            """ % ",".join("?" * len(lids))
        count = cur.execute(sql % "COUNT(*)", lids).fetchone()[0]
        sids = {}
        for i, r in enumerate(cur.execute(sql % "streams.sid, spos, slen", lids), start=1):
            if i == 1 or i % 10000 == 0 or i == count:
                sys.stderr.write(f"\rreading positions... {i:,} / {count:,}")
                sys.stderr.flush()
            if not r[0] in sids:
                sids[r[0]] = r

        sys.stderr.write(f"\noptimizing... {len(sids):,} ->")
        poslens = []
        cur, pos, length = 0, 0, 0
        for sid, r in sorted(sids.items(), key=lambda x:x[0]):
            if cur != sid or length > 10_000_000:
                poslens.append((langs, target, pos, length))
                pos = r[1]
                length = 0
            length += r[2]
            cur = sid + 1
        if length: poslens.append((langs, target, pos, length))
        sys.stderr.write(f" {len(poslens):,}\n")

    langdata = {}
    for lang in langs: langdata[lang] = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for i, result in enumerate(executor.map(langtext, poslens), start=1):
            sys.stdout.write(f"\rreading streams... {i:,} / {len(poslens):,}")
            sys.stdout.flush()
            for lang in langs:
                for r in result[lang]:
                    word = r[0].lower().replace("-", "")
                    langdata[lang].append((word, r))
    print()
    for lang in langs:
        ld = langdata[lang]
        print(f"{lang}: {len(ld):,}")
        ld.sort(key=lambda x:x[0])
        with open(f"{lang}.txt", "w", encoding="utf-8") as f:
            for i, (_, (title, text)) in enumerate(ld):
                if i > 0: f.write("\n")
                f.write(f"<!-- <title>{title}</title> -->\n\n{text}\n")
