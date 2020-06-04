CPU: AMD Ryzen 5 2500U with Radeon Vega Mobile Gfx (4 cores)

# research stream lengths

```
$ time python streamlen.py > streamlen.tsv

real    2m53.684s
user    2m52.641s
sys     0m0.953s
```

# count lines

```
$ time python countlines.py
lines: 215,082,554

real    3m41.572s
user    3m40.031s
sys     0m1.469s
```
```
$ time python countlines-BytesIO.py
lines: 215,082,554

real    3m40.948s
user    3m39.359s
sys     0m1.578s
```
```
$ time python countlines-StringIO.py
lines: 215,082,554

real    3m19.107s
user    3m16.891s
sys     0m2.063s
```

# XML parse test

```
$ time python countlines-text.py
lines: 76,501,897

real    4m17.963s
user    4m15.969s
sys     0m1.891s
```
```
$ time python countlines-text-xml.py
lines: 76,501,897

real    6m6.185s
user    6m2.609s
sys     0m3.500s
```

# create the language table

```
$ time python checklang.py

real    4m42.539s
user    4m37.313s
sys     0m5.031s
```
```
$ time python checklang-re.py

real    5m22.396s
user    5m17.609s
sys     0m4.703s
```
```
$ time python checklang-xml.py

real    11m13.486s
user    11m6.516s
sys     0m6.563s
```
```
$ time python checklang-xml-re.py

real    11m56.370s
user    11m49.297s
sys     0m6.578s
```

# parallelize

```
$ time python checklang-parallel.py

real    1m16.566s
user    8m43.188s
sys     0m9.281s
```
```
$ time python checklang-parallel-re.py

real    1m21.199s
user    10m9.422s
sys     0m8.844s
```
```
$ time python checklang-parallel-xml.py

real    1m51.803s
user    14m4.406s
sys     0m14.000s
```
```
$ time python checklang-parallel-xml-re.py

real    2m6.238s
user    15m58.641s
sys     0m14.641s
```
