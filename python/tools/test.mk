test:
	python db-make.py ~/share/wiktionary/enwiktionary-20200501-pages-articles-multistream.xml.bz2
	sqlite3 enwiktionary.db ".read db.sql"
	sqlite3 enwiktionary.db ".read rank.sql" > rank.tsv
	python db-template.py enwiktionary.db
	python search-title.py enwiktionary.db
	python collect-title.py enwiktionary.db Lojban.txt "^Appendix:Lojban/"
	python collect-title.py enwiktionary.db Klingon.txt "^Appendix:Klingon/"
	python collect-title.py enwiktionary.db Toki_Pona.txt "^Appendix:Toki Pona/"
	python collect-lang.py enwiktionary.db English
	python collect-lang.py enwiktionary.db Russian
	python collect-lang.py enwiktionary.db Arabic Estonian Hebrew Hittite Ido Interlingua Interlingue Novial "Old English" "Old High German" "Old Saxon" Phoenician Vietnamese Volapük Yiddish
