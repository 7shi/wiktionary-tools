# create DB

```
$ time python db-make.py ../enwiktionary-20200501-pages-articles-multistream.xml.bz2
934,033,103 / 934,033,103 | 68,608

real    19m4.516s
user    18m40.453s
sys     0m14.375s
```
```
$ time sqlite3 enwiktionary.db ".read db.sql"
importing 'db-settings.tsv'...
importing 'db-streams.tsv'...
importing 'db-namespaces.tsv'...
importing 'db-pages.tsv'...
importing 'db-idlang.tsv'...
importing 'db-langname.tsv'...

real    0m46.009s
user    0m33.875s
sys     0m10.828s
```
```
$ time sqlite3 enwiktionary.db ".read langcode.sql"
Importing 'langcode.tsv'...

real    0m0.082s
user    0m0.047s
sys     0m0.000s
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
$ time python collect-lang.py enwiktionary.db Estonian.txt Estonian
reading `pages`... 8,756 / 8,756
Sorting...
writing `pages`... 8,756 / 8,756

real    1m22.247s
user    1m14.797s
sys     0m6.406s
```
```
$ time python langtext.py Estonian
6,861 / 6,861
Estonian: 8,756

real    1m50.057s
user    13m49.750s
sys     0m20.344s
```
```
$ time python langtext.py Arabic Estonian Hebrew Hittite Ido Interlingua Interlingue Novial "Old English" "Old High German" "Old Saxon" Phoenician Vietnamese Volapük Yiddish
6,861 / 6,861
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

real    1m56.919s
user    14m23.703s
sys     0m16.141s
```
