#r "AR.Compression.BZip2.dll"
#load "StreamUtils.fsx"
open System
open System.IO
open System.IO.Compression
open System.Text
open StreamUtils

let target, slen =
    use sr = new StreamReader("streamlen.tsv")
    sr.ReadLine(),
    [|  while not <| sr.EndOfStream do
        yield sr.ReadLine() |> Convert.ToInt32 |]

let mutable lines = 0
do
    use fs = new FileStream(target, FileMode.Open)
    for lengths in Seq.chunkBySize 100 slen do
        let text =
            use ss = new SubStream(fs, Array.sum lengths)
            use bs = new BZip2Stream(ss, CompressionMode.Decompress)
            use ms = new MemoryStream()
            bs.CopyTo(ms)
            Encoding.UTF8.GetString(ms.ToArray())
        use sr = new StringReader(text)
        while not (isNull (sr.ReadLine())) do
            lines <- lines + 1
Console.WriteLine("lines: {0:#,0}", lines)
