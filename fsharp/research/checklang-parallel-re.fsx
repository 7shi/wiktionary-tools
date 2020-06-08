#load "MediaWikiParse.fsx"
open System.Collections.Generic
open System.IO
open System.Text.RegularExpressions

let target, sposlen = MediaWikiParse.read("")

let getlangs(pos, length) = async { return [
    let r = Regex "^==([^=].*)=="
    use fs = new FileStream(target, FileMode.Open, FileAccess.Read)
    fs.Seek(pos, SeekOrigin.Begin) |> ignore
    for id, text in MediaWikiParse.getPages(fs, length) do
        for line in text do
            let m = r.Match line
            if m.Success then
                yield id, m.Groups.[1].Value.Trim() ]}

let results =
    sposlen.[1 .. sposlen.Length - 2]
    |> Seq.chunkBySize 100
    |> Seq.map Array.unzip
    |> Seq.map (fun (ps, ls) -> Array.min ps, Array.sum ls)
    |> Seq.map getlangs
    |> Async.Parallel
    |> Async.RunSynchronously
    |> List.concat
let langs = Dictionary<string, int>()
do
    use sw = new StreamWriter("output1.tsv")
    sw.NewLine <- "\n"
    for id, lang in results do
        let lid =
            if langs.ContainsKey lang then langs.[lang] else
            let lid = langs.Count + 1
            langs.[lang] <- lid
            lid
        fprintfn sw "%d\t%d" id lid
do
    use sw = new StreamWriter("output2.tsv")
    sw.NewLine <- "\n"
    for kv in langs do
        fprintfn sw "%d\t%s" kv.Value kv.Key
