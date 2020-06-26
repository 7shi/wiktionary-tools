mediawiki="python ../../python/tools/mediawiki.py" 
db="../../python/tools/enwiktionary.db"
if [ ! -d mediawiki-extensions-Scribunto ]; then
    git clone https://github.com/wikimedia/mediawiki-extensions-Scribunto.git
fi
function mediawiki() {
    file="$2.$1"
    page="$2"
    if [ ! -f "$file" ]; then
        echo "$file"
        $mediawiki -o "$file" $db "$page"
    fi
}
function mediawiki_data() {
    ext="$1"
    page="$2"
    mediawiki "$ext" "$page"
    mkdir -p "$page"
    mediawiki "$ext" "$page/data"
}
mediawiki lua "Module:ugly hacks"
mediawiki lua "Module:en-headword"
mediawiki lua "Module:languages"
mkdir -p "Module:languages"
mediawiki lua "Module:languages/data2"
mediawiki lua "Module:parameters"
mediawiki lua "Module:string"
mediawiki lua "Module:table"
mediawiki lua "Module:debug"
mediawiki_data lua "Module:headword"
mediawiki lua "Module:utils"
mediawiki_data lua "Module:scripts"
mediawiki_data lua "Module:palindromes"
mediawiki_data lua "Module:links"
mediawiki_data lua "Module:script utilities"
mediawiki_data lua "Module:utilities"
