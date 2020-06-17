import sqlite3, os, sys

try:
    db = sys.argv[1]
except:
    sys.stderr.write(f"usage: {sys.argv[0]} db\n")
    exit(1)

with open(db, "rb") as f: pass
with sqlite3.connect(db) as conn:
    cur = conn.cursor()

    count = cur.execute("SELECT COUNT(*) FROM settings").fetchone()[0]
    for i, (key, value) in enumerate(cur.execute(
            "SELECT key, value FROM settings"), start=1):
        sys.stderr.write(f"\rreading `settings`... {i:,} / {count:,}")
        sys.stderr.flush()
    sys.stderr.write("\n")

    count = cur.execute("SELECT COUNT(*) FROM streams").fetchone()[0]
    for i, (sid, spos, slen) in enumerate(cur.execute(
            "SELECT sid, spos, slen FROM streams"), start=1):
        if i == 1 or i % 10000 == 0 or i == count:
            sys.stderr.write(f"\rreading `streams`... {i:,} / {count:,}")
            sys.stderr.flush()
    sys.stderr.write("\n")

    count = cur.execute("SELECT COUNT(*) FROM namespaces").fetchone()[0]
    for i, (ns, nsname) in enumerate(cur.execute(
            "SELECT ns, nsname FROM namespaces"), start=1):
        sys.stderr.write(f"\rreading `namespaces`... {i:,} / {count:,}")
        sys.stderr.flush()
    sys.stderr.write("\n")

    count = cur.execute("SELECT COUNT(*) FROM pages").fetchone()[0]
    for i, (id, sid, ns, title) in enumerate(cur.execute(
            "SELECT id, sid, ns, title FROM pages"), start=1):
        if i == 1 or i % 10000 == 0 or i == count:
            sys.stderr.write(f"\rreading `pages`... {i:,} / {count:,}")
            sys.stderr.flush()
    sys.stderr.write("\n")

    count = cur.execute("SELECT COUNT(*) FROM idlang").fetchone()[0]
    for i, (id, lid) in enumerate(cur.execute(
            "SELECT id, lid FROM idlang"), start=1):
        if i == 1 or i % 10000 == 0 or i == count:
            sys.stderr.write(f"\rreading `idlang`... {i:,} / {count:,}")
            sys.stderr.flush()
    sys.stderr.write("\n")

    count = cur.execute("SELECT COUNT(*) FROM langname").fetchone()[0]
    for i, (lid, name) in enumerate(cur.execute(
            "SELECT lid, name FROM langname"), start=1):
        sys.stderr.write(f"\rreading `langname`... {i:,} / {count:,}")
        sys.stderr.flush()
    sys.stderr.write("\n")

    count = cur.execute("SELECT COUNT(*) FROM langcode").fetchone()[0]
    for i, (code, name) in enumerate(cur.execute(
            "SELECT code, name FROM langcode"), start=1):
        sys.stderr.write(f"\rreading `langcode`... {i:,} / {count:,}")
        sys.stderr.flush()
    sys.stderr.write("\n")
