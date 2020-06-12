import re, sys
pattern = re.compile("{{en-verb\\|(.*?)\\|*}}")
for line in sys.stdin:
    id, verb, forms = line.split("\t")
    if (m := pattern.match(forms)):
        forms = m[1].split("|")
        if len(forms) > 2 and forms[2] != "ing" and forms[2] != "ed":
            forms = "\t".join(forms)
            print(f"{id}\t{verb}\t{forms}")
