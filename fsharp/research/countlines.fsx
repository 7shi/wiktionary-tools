#r "AR.Compression.BZip2.dll"
open System
open System.IO
open System.IO.Compression

let target = "enwiktionary-20200501-pages-articles-multistream.xml.bz2"
let mutable lines = 0
do
    use fs = new FileStream(target, FileMode.Open)
    use bs = new BZip2Stream(fs, CompressionMode.Decompress)
    use sr = new StreamReader(bs)
    while not (isNull (sr.ReadLine())) do
        lines <- lines + 1
Console.WriteLine("lines: {0:#,0}", lines)
