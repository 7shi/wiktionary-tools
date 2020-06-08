#load "MediaWikiParse.fsx"
open System.Collections.Generic
open System.IO

let target, sposlen = MediaWikiParse.read("")

let getlangs(pos, length) = async { return [
    use fs = new FileStream(target, FileMode.Open, FileAccess.Read)
    fs.Seek(pos, SeekOrigin.Begin) |> ignore
    for id, text in MediaWikiParse.getPages(fs, length) do
        for line in text do
            if line.Length >= 3 && line.[0] = '=' && line.[1] = '=' && line.[2] <> '=' then
                let lang = line.[2..].Trim()
                let mutable e = lang.Length - 1
                while e > 0 && lang.[e] = '=' do e <- e - 1
                yield id, lang.[..e].Trim() ]}

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
