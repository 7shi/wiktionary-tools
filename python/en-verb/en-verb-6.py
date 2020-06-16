import sys
verbs = {}
for line in sys.stdin:
    verb, *forms = line.strip().split("\t")
    if verb in verbs: continue
    verbs[verb] = forms
verbs2 = []
for v1 in verbs.items():
    contains = False
    for v2 in verbs.items():
        if v1[0] != v2[0] and v1[0].endswith(v2[0]):
            c = True
            for f1, f2 in zip(v1[1], v2[1]):
                if not f1.endswith(f2):
                    c = False
                    break
            if c:
                contains = True
                break
    if not contains:
        print("\t".join([v1[0]] + v1[1]))
