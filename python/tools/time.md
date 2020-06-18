# create DB

```
$ time python db-make.py ~/share/wiktionary/enwiktionary-20200501-pages-articles-multistream.xml.bz2
934,033,103 / 934,033,103 | 68,608
reading language codes...
checking language names...
writing DB files...

real    4m30.913s
user    9m36.641s
sys     0m44.141s
```
```
$ time sqlite3 enwiktionary.db ".read db.sql"
importing 'db-settings.tsv'...
importing 'db-streams.tsv'...
importing 'db-namespaces.tsv'...
importing 'db-pages.tsv'...
importing 'db-idlang.tsv'...
importing 'db-langname.tsv'...
Importing 'db-langcode.tsv'...

real    0m49.350s
user    0m36.375s
sys     0m11.313s
```
```
$ time sqlite3 enwiktionary.db ".read rank.sql" > rank.tsv

real    0m0.703s
user    0m0.547s
sys     0m0.109s
```

# tests

```
$ time python db-template.py enwiktionary.db
reading `settings`... 1 / 1
reading `streams`... 68,609 / 68,609
reading `namespaces`... 46 / 46
reading `pages`... 6,860,557 / 6,860,557
reading `idlang`... 6,916,807 / 6,916,807
reading `langname`... 3,978 / 3,978
reading `langcode`... 8,146 / 8,146

real    0m23.817s
user    0m21.891s
sys     0m1.313s
```
```
$ time python search-title.py enwiktionary.db
reading `pages`... 6,860,557 / 6,860,557

real    0m10.861s
user    0m10.156s
sys     0m0.547s
```

# extract

```
$ time python collect-title.py enwiktionary.db Lojban.txt "^Appendix:Lojban/"
reading `pages`... 6,860,557 / 6,860,557
Sorting...
writing `pages`... 3,493 / 3,493

real    0m17.376s
user    0m15.625s
sys     0m1.500s
```
```
$ time python collect-title.py enwiktionary.db Klingon.txt "^Appendix:Klingon/"
reading `pages`... 6,860,557 / 6,860,557
Sorting...
writing `pages`... 2,147 / 2,147

real    0m13.200s
user    0m12.125s
sys     0m0.969s
```
```
$ time python collect-title.py enwiktionary.db Toki_Pona.txt "^Appendix:Toki Pona/"
reading `pages`... 6,860,557 / 6,860,557
Sorting...
writing `pages`... 130 / 130

real    0m11.584s
user    0m10.703s
sys     0m0.781s
```
```
$ time python collect-lang.py enwiktionary.db English
reading positions... 928,987 / 928,987
optimizing... 49,835 -> 6,575
reading streams... 6,575 / 6,575
English: 928,988

real    1m55.532s
user    11m25.219s
sys     0m59.109s

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

real    0m35.931s
user    3m33.625s
sys     0m23.578s

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

real    0m52.407s
user    5m50.281s
sys     0m20.297s
```
