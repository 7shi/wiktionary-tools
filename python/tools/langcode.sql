.mode ascii
.separator "\t" "\n"

.print Importing \'langcode.tsv\'...
CREATE TABLE langcode(code VARCHAR(16) PRIMARY KEY, name TEXT);
.import langcode.tsv langcode
CREATE INDEX langcode_name_idx ON langcode(name);
