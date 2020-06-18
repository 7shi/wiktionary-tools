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
CREATE TABLE pages(id INTEGER PRIMARY KEY, sid INTEGER, ns INTEGER, redirect INTEGER, title TEXT);
.import db-pages.tsv pages
CREATE INDEX pages_sid_idx      ON pages(sid);
CREATE INDEX pages_ns_idx       ON pages(ns);
CREATE INDEX pages_redirect_idx ON pages(redirect);
CREATE INDEX pages_title_idx    ON pages(title);

.print importing \'db-idlang.tsv\'...
CREATE TABLE idlang(id INTEGER, lid INTEGER, PRIMARY KEY(id, lid));
.import db-idlang.tsv idlang
CREATE INDEX idlang_id_idx  ON idlang(id);
CREATE INDEX idlang_lid_idx ON idlang(lid);

.print importing \'db-langname.tsv\'...
CREATE TABLE langname(lid INTEGER, no INTEGER, name TEXT, PRIMARY KEY(lid, no));
.import db-langname.tsv langname
CREATE INDEX langname_lid_idx  ON langname(lid);
CREATE INDEX langname_name_idx ON langname(name);

.print Importing \'db-langcode.tsv\'...
CREATE TABLE langcode(code VARCHAR(16) PRIMARY KEY, name TEXT);
.import db-langcode.tsv langcode
CREATE INDEX langcode_name_idx ON langcode(name);

.print Importing \'db-templates.tsv\'...
CREATE TABLE templates(title TEXT PRIMARY KEY, include TEXT);
.import db-templates.tsv templates
CREATE INDEX templates_include_idx ON templates(include);
