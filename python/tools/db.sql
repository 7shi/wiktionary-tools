.mode ascii
.separator "\t" "\n"

.print importing \'db-settings.tsv\'...
CREATE TABLE settings(key TEXT PRIMARY KEY, value TEXT);
.import db-settings.tsv settings

.print importing \'db-streams.tsv\'...
CREATE TABLE streams(sid INTEGER PRIMARY KEY, spos INTEGER, slen INTEGER);
.import db-streams.tsv streams

.print importing \'db-namespaces.tsv\'...
CREATE TABLE namespaces(ns INTEGER PRIMARY KEY, nsname TEXT);
.import db-namespaces.tsv namespaces

.print importing \'db-pages.tsv\'...
CREATE TABLE pages(id INTEGER PRIMARY KEY, sid INTEGER, ns INTEGER, title TEXT);
.import db-pages.tsv pages
CREATE INDEX pages_sid_idx   ON pages(sid);
CREATE INDEX pages_ns_idx    ON pages(ns);
CREATE INDEX pages_title_idx ON pages(title);

.print importing \'db-idlang.tsv\'...
CREATE TABLE idlang(id INTEGER, lid INTEGER, PRIMARY KEY(id, lid));
.import db-idlang.tsv idlang
CREATE INDEX idlang_id_idx  ON idlang(id);
CREATE INDEX idlang_lid_idx ON idlang(lid);

.print importing \'db-langname.tsv\'...
CREATE TABLE langname(lid INTEGER PRIMARY KEY, name TEXT);
.import db-langname.tsv langname
CREATE INDEX langname_name_idx ON langname(name);
