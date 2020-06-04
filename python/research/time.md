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
$ time python countlines-yield.py
lines: 215,082,554

real    3m46.114s
user    3m43.766s
sys     0m2.297s
```
```
$ time python countlines-text.py
lines: 76,501,897

real    4m45.896s
user    4m43.578s
sys     0m2.078s
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

real    5m14.153s
user    5m9.203s
sys     0m4.734s
```
```
$ time python checklang-re.py

real    6m11.350s
user    6m6.141s
sys     0m5.063s
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

real    1m15.603s
user    9m19.672s
sys     0m9.094s
```
```
$ time python checklang-parallel-re.py

real    1m27.347s
user    10m57.672s
sys     0m9.313s
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
