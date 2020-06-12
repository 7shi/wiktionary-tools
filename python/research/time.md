Environment

* OS : Windows 10 1909
* CPU: AMD Ryzen 5 2500U with Radeon Vega Mobile Gfx (4 cores)
* Python 3.8.2 (WSL1)

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

real    3m34.911s
user    3m33.625s
sys     0m1.188s
```
```
$ time python countlines-BytesIO.py
lines: 215,082,554

real    3m37.827s
user    3m36.250s
sys     0m1.547s
```
```
$ time python countlines-StringIO.py
lines: 215,082,554

real    3m18.568s
user    3m16.438s
sys     0m2.047s
```

# XML parse test

```
$ time python countlines-text.py
lines: 76,501,897

real    4m6.555s
user    4m4.203s
sys     0m2.328s
```
```
$ time python countlines-text-xml.py
lines: 76,501,897

real    5m50.826s
user    5m47.047s
sys     0m3.531s
```
```
$ time python countlines-text-xmlpull.py
lines: 76,501,897

real    6m4.553s
user    6m1.047s
sys     0m3.375s
```
```
$ time python countlines-text-xmliter.py
lines: 76,501,897

real    6m29.298s
user    6m24.734s
sys     0m4.359s
```
```
$ time python countlines-text-xmlparser.py
lines: 76,501,897

real    6m46.163s
user    6m43.703s
sys     0m2.391s
```

# create the language table

```
$ time python checklang.py

real    4m35.440s
user    4m29.844s
sys     0m4.672s
```
```
$ time python checklang-ch.py

real    4m37.771s
user    4m33.219s
sys     0m4.281s
```
```
$ time python checklang-re.py

real    4m31.855s
user    4m26.375s
sys     0m5.250s
```
```
$ time python checklang-re-not-compile.py

real    5m16.428s
user    5m11.281s
sys     0m5.078s
```
```
$ time python checklang-xml.py

real    10m12.721s
user    10m6.813s
sys     0m5.875s
```
```
$ time python checklang-xml-re.py

real    9m59.988s
user    9m53.484s
sys     0m6.297s
```
```
$ time python checklang-xml-re-not-compile.py

real    11m2.035s
user    10m55.203s
sys     0m6.656s
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

real    1m7.106s
user    8m12.281s
sys     0m8.953s
```
```
$ time python checklang-parallel-re-not-compile.py

real    1m19.153s
user    9m46.391s
sys     0m9.016s
```
```
$ time python checklang-parallel-xml.py

real    1m49.075s
user    13m33.594s
sys     0m13.922s
```
```
$ time python checklang-parallel-xml-re.py

real    1m49.981s
user    13m38.625s
sys     0m14.688s
```
```
$ time python checklang-parallel-xml-re-not-compile.py

real    2m1.814s
user    15m12.047s
sys     0m14.391s
```
