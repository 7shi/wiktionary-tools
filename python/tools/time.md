# create DB

```
$ time python db-make.py enwiktionary-20200501-pages-articles-multistream.xml.bz2
934,033,103 / 934,033,103 | 68,608
writing DB files...

real    4m20.995s
user    9m22.906s
sys     0m42.172s
```
```
$ time sqlite3 enwiktionary.db ".read db.sql"
importing 'db-settings.tsv'...
importing 'db-streams.tsv'...
importing 'db-namespaces.tsv'...
importing 'db-pages.tsv'...
importing 'db-idlang.tsv'...
importing 'db-langname.tsv'...

real    0m46.785s
user    0m34.641s
sys     0m10.578s
```
```
$ time sqlite3 enwiktionary.db ".read langcode.sql"
Importing 'langcode.tsv'...

real    0m0.082s
user    0m0.016s
sys     0m0.078s
```

# tests

```
$ time python db-template.py enwiktionary.db
reading `settings`... 1 / 1
reading `streams`... 68,609 / 68,609
reading `namespaces`... 46 / 46
reading `pages`... 6,860,637 / 6,860,637
reading `idlang`... 6,916,807 / 6,916,807
reading `langname`... 3,978 / 3,978

real    0m19.100s
user    0m17.891s
sys     0m0.938s
```
```
$ time python search-title.py enwiktionary.db
reading `pages`... 6,860,637 / 6,860,637

real    0m9.812s
user    0m9.234s
sys     0m0.500s
```

# extract

```
$ time python collect-title.py enwiktionary.db Lojban.txt "^Appendix:Lojban/"
reading `pages`... 6,860,637 / 6,860,637
Sorting...
writing `pages`... 3,493 / 3,493

real    0m15.689s
user    0m14.141s
sys     0m1.359s
```
```
$ time python collect-title.py enwiktionary.db Klingon.txt "^Appendix:Klingon/"
reading `pages`... 6,860,637 / 6,860,637
Sorting...
writing `pages`... 2,147 / 2,147

real    0m13.050s
user    0m11.703s
sys     0m1.172s
```
```
$ time python collect-title.py enwiktionary.db Toki_Pona.txt "^Appendix:Toki Pona/"
reading `pages`... 6,860,637 / 6,860,637
Sorting...
writing `pages`... 130 / 130

real    0m10.301s
user    0m9.641s
sys     0m0.578s
```
```
$ time python collect-lang.py enwiktionary.db English
reading positions... 928,987 / 928,987
optimizing... 49,835 -> 6,575
reading streams... 6,575 / 6,575
English: 928,988

real    2m8.564s
user    12m14.250s
sys     1m8.875s

$ wc -l English.txt
14461960 English.txt

$ wc --bytes English.txt
452471057 English.txt
```
```
$ time python collect-lang.py enwiktionary.db Russian
reading positions... 394,340 / 394,340
optimizing... 16,190 -> 6,887
reading streams... 6,887 / 6,887
Russian: 394,340

real    0m37.653s
user    3m38.031s
sys     0m23.781s

$ wc -l Russian.txt
4720984 Russian.txt

$ wc --bytes Russian.txt
109618281 Russian.txt
```
```
$ time python collect-lang.py enwiktionary.db Arabic Estonian Hebrew Hittite Ido Interlingua Interlingue Novial "Old English" "Old High German" "Old Saxon" Phoenician Vietnamese Volapük Yiddish
reading positions... 143,926 / 143,926
optimizing... 25,073 -> 10,386
reading streams... 10,386 / 10,386
Arabic: 50,380
Estonian: 8,756
Hebrew: 9,845
Hittite: 392
Ido: 19,978
Interlingua: 3,271
Interlingue: 638
Novial: 666
Old English: 10,608
Old High German: 1,434
Old Saxon: 1,999
Phoenician: 129
Vietnamese: 25,588
Volapük: 3,918
Yiddish: 6,324

real    0m51.764s
user    5m44.953s
sys     0m20.922s
```
