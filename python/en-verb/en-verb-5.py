import sys
for line in sys.stdin:
    id, *forms = line.strip().split("\t")
    if len(forms) == 4: forms.append(forms[3])
    verb, _, _, past, pp = [f.replace("'", "").replace("-", "") for f in forms]
    if past == pp:
        if not past: continue
        if past.endswith("ed"):
            if verb.endswith("e") and verb + "d" == past: continue
            if verb.endswith("y") and verb[:-1] + "ied" == past: continue
            if verb + "ed" == past: continue
            if verb + verb[-1] + "ed" == past: continue
            if verb[-1] == "c" and verb + "ked" == past: continue
    forms = "\t".join(forms)
    print(f"{id}\t{forms}")
