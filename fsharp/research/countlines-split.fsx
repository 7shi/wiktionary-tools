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

let mutable lines = 0
do
    use fs = new FileStream(target, FileMode.Open)
    for length in slen do
        use ss = new SubStream(fs, length)
        use bs = new BZip2Stream(ss, CompressionMode.Decompress)
        use sr = new StreamReader(bs)
        while not (isNull (sr.ReadLine())) do
            lines <- lines + 1
Console.WriteLine("lines: {0:#,0}", lines)
