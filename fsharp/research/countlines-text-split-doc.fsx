#r "AR.Compression.BZip2.dll"
#load "StreamUtils.fsx"
open System
open System.IO
open System.IO.Compression
open System.Xml
open StreamUtils

let target, slen =
    use sr = new StreamReader("streamlen.tsv")
    sr.ReadLine(),
    [|  while not <| sr.EndOfStream do
        yield sr.ReadLine() |> Convert.ToInt32 |]

let getPages(stream, length) = seq {
    use ss = new SubStream(stream, length)
    use cs = new ConcatStream([
        new MemoryStream("<pages>"B)
        new BZip2Stream(ss, CompressionMode.Decompress)
        new MemoryStream("</pages>"B) ])
    use xr = XmlReader.Create(cs)
    let doc = XmlDocument()
    doc.Load(xr)
    for page in doc.ChildNodes.[0].ChildNodes do
        let ns = Convert.ToInt32(page.SelectSingleNode("ns").InnerText)
        if ns = 0 then
            let id = Convert.ToInt32(page.SelectSingleNode("id").InnerText)
            let text = page.SelectSingleNode("revision/text").InnerText
            use sr = new StringReader(text)
            yield id, seq {
                while sr.Peek() <> -1 do
                    yield sr.ReadLine() }}

let mutable lines = 0
do
    use fs = new FileStream(target, FileMode.Open)
    fs.Seek(int64 slen.[0], SeekOrigin.Begin) |> ignore
    for lengths in Seq.chunkBySize 100 slen.[1 .. slen.Length - 2] do
        for _, text in getPages(fs, Array.sum lengths) do
            for _ in text do
                lines <- lines + 1
Console.WriteLine("lines: {0:#,0}", lines)
