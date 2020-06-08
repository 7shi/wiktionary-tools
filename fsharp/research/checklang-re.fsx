#load "MediaWikiParse.fsx"
open System.Collections.Generic
open System.IO
open System.Text.RegularExpressions

let target, sposlen = MediaWikiParse.read("")
let _, slen = Array.unzip sposlen

let langs = Dictionary<string, int>()
let results = [
    let r = Regex "^==([^=].*)=="
    use fs = new FileStream(target, FileMode.Open)
    fs.Seek(int64 slen.[0], SeekOrigin.Begin) |> ignore
    for lengths in Seq.chunkBySize 100 slen.[1 .. slen.Length - 2] do
        for id, text in MediaWikiParse.getPages(fs, Array.sum lengths) do
            for line in text do
                let m = r.Match line
                if m.Success then
                    let lang = m.Groups.[1].Value.Trim()
                    let lid =
                        if langs.ContainsKey lang then langs.[lang] else
                        let lid = langs.Count + 1
                        langs.[lang] <- lid
                        lid
                    yield id, lid ]
do
    use sw = new StreamWriter("output1.tsv")
    sw.NewLine <- "\n"
    for id, lid in results do
        fprintfn sw "%d\t%d" id lid
do
    use sw = new StreamWriter("output2.tsv")
    sw.NewLine <- "\n"
    for kv in langs do
        fprintfn sw "%d\t%s" kv.Value kv.Key
