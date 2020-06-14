import mediawiki, io, re, sys

try:
    target = sys.argv[1]
except:
    print(f"usage: {sys.argv[0]} db")
    exit(1)

db = mediawiki.DB(target)
langs = {}
pattern1 = re.compile(r'm\["(.+?)"\]')
pattern2 = re.compile('"(.+?)"')

def read(title):
    with io.StringIO(db[title].text) as f:
        while (line := next(f, "")):
            if (m1 := pattern1.match(line)):
                line = next(f, "")
                if (m2 := pattern2.search(line)):
                    langs[m1[1]] = m2[1]

read("Module:languages/data2")
for i in range(ord("a"), ord("z") + 1):
    read(f"Module:languages/data3/{chr(i)}")
read("Module:languages/datax")

with open("langcode.tsv", "w", encoding="utf-8") as f:
    for code, name in langs.items():
        f.write(f"{code}\t{name}\n")
