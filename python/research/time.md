Environment

* OS : Windows 10 1909
* CPU: AMD Ryzen 5 2500U with Radeon Vega Mobile Gfx (4 cores)
* .NET Framework 4.8.03752
* Mono 6.4.0 (WSL1)

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

real    4m26.421s
user    4m21.344s
sys     0m4.891s
```
```
$ time python checklang-ch.py

real    4m30.566s
user    4m26.188s
sys     0m4.297s
```
```
$ time python checklang-re.py

real    5m9.869s
user    5m5.625s
sys     0m4.047s
```
```
$ time python checklang-xml.py

real    9m55.814s
user    9m49.188s
sys     0m6.438s
```
```
$ time python checklang-xml-re.py

real    10m41.234s
user    10m34.906s
sys     0m6.266s
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

real    1m19.372s
user    9m44.422s
sys     0m9.203s
```
```
$ time python checklang-parallel-xml.py

real    1m52.676s
user    13m57.469s
sys     0m13.797s
```
```
$ time python checklang-parallel-xml-re.py

real    2m6.217s
user    16m0.172s
sys     0m14.203s
```
