#r "AR.Compression.BZip2.dll"
#load "StreamUtils.fsx"
open System
open System.IO
open System.IO.Compression
open StreamUtils

let target, slen =
    use sr = new StreamReader("streamlen.tsv")
    sr.ReadLine(),
    [|  while not <| sr.EndOfStream do
        yield sr.ReadLine() |> Convert.ToInt32 |]

let inline startsWith (target:string) (value:string) =
    target.Length >= value.Length && target.Substring(0, value.Length) = value

let getPages(stream, length) = seq {
    use ss = new SubStream(stream, length)
    use bs = new BZip2Stream(ss, CompressionMode.Decompress)
    use sr = new StreamReader(bs)
    let mutable ns, id = 0, 0
    while sr.Peek() <> -1 do
        let mutable line = sr.ReadLine().TrimStart()
        if startsWith line "<ns>" then
            ns <- Convert.ToInt32 line.[4 .. line.IndexOf('<', 4) - 1]
            id <- 0
        elif id = 0 && startsWith line "<id>" then
            id <- Convert.ToInt32 line.[4 .. line.IndexOf('<', 4) - 1]
        elif startsWith line "<text " then
            let p = line.IndexOf '>'
            if line.[p - 1] = '/' then () else
            if ns <> 0 then
                while not <| line.EndsWith "</text>" do
                line <- sr.ReadLine()
            else
                line <- line.[p + 1 ..]
                yield id, seq {
                    while not <| isNull line do
                    if line.EndsWith "</text>" then
                        if line.Length > 7 then yield line.[.. line.Length - 8]
                        line <- null
                    else
                        yield line
                        line <- sr.ReadLine() }}

let mutable lines = 0
do
    use fs = new FileStream(target, FileMode.Open)
    fs.Seek(int64 slen.[0], SeekOrigin.Begin) |> ignore
    for lengths in Seq.chunkBySize 100 slen.[1 .. slen.Length - 2] do
        for _, text in getPages(fs, Array.sum lengths) do
            for _ in text do
                lines <- lines + 1
Console.WriteLine("lines: {0:#,0}", lines)
