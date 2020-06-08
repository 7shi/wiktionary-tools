CPU: AMD Ryzen 5 2500U with Radeon Vega Mobile Gfx (4 cores)

# count lines

```
$ cd .; time ./countlines.exe
lines: 215,082,554

real    2m40.270s
```

## split by streams

```
$ time ./countlines-split.exe
lines: 215,082,554

real    5m23.122s
```
```
$ time ./countlines-split-10.exe
lines: 215,082,554

real    2m50.913s
```
```
$ time ./countlines-split-100.exe
lines: 215,082,554

real    2m40.727s
```
```
$ time ./countlines-split-string.exe
lines: 215,082,554

real    7m50.915s
```
```
$ time ./countlines-split-string-10.exe
lines: 215,082,554

real    3m55.453s
```
```
$ time ./countlines-split-string-100.exe
lines: 215,082,554

real    3m23.417s
```

# XML parse test

```
$ time ./countlines-text-split.exe
lines: 76,501,897

real    4m5.507s
```
```
$ time ./countlines-text-split-slice.exe
lines: 76,501,897

real    4m14.069s
```
```
$ time ./countlines-text-split-StartsWith.fsx
lines: 76,501,897

real    4m42.877s
```
```
$ time ./countlines-text-split-doc.exe
lines: 76,501,897

real    6m21.588s
```
```
$ time ./countlines-text-split-reader.exe
lines: 76,501,897

real    3m17.916s
```
```
$ time ./countlines-text-reader.exe
lines: 76,501,897

real    3m16.122s
```

# create the language table

```
$ time ./checklang.exe

real    3m24.302s

$ time mono checklang.exe

real    4m22.330s
user    4m20.797s
sys     0m2.625s
```
```
$ time ./checklang-StartsWith.exe

real    3m43.965s

$ time mono checklang-StartsWith.exe

real    5m21.839s
user    5m20.813s
sys     0m2.156s
```
```
$ time ./checklang-try.exe

real    3m27.241s
```
```
$ time ./checklang-array.exe

real    3m32.713s
```
```
$ time ./checklang-cslist.exe

real    3m28.725s
```
```
$ time ./checklang-re.exe

real    3m46.270s

$ time mono checklang-re.exe

real    4m51.236s
user    4m49.969s
sys     0m2.422s
```

# parallelize

```
$ time ./checklang-parallel.exe

real    1m3.941s

$ time mono checklang-parallel.exe

real    2m39.716s
user    18m9.109s
sys     0m46.813s
```
```
$ time ./checklang-parallel-re.exe

real    1m7.009s

$ time mono checklang-parallel-re.exe

real    3m28.074s
user    24m51.109s
sys     0m31.531s
```
