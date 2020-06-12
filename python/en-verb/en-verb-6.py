import sys
verbs = {}
for line in sys.stdin:
    id, verb, *forms = line.strip().split("\t")
    if verb in verbs: continue
    verbs[verb] = (id, forms)
verbs2 = []
for v1, (id, forms) in verbs.items():
    contains = False
    for v2, (_, f2) in verbs.items():
        if v1 != v2 and v1.endswith(v2):
            c = True
            for f1, f2 in zip(forms, f2):
                if not f1.endswith(f2):
                    c = False
                    break
            if c:
                contains = True
                break
    if not contains:
        forms = "\t".join(forms)
        print(f"{id}\t{v1}\t{forms}")
