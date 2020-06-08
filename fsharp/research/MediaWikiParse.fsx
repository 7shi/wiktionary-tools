#r "AR.Compression.BZip2.dll"
#load "StreamUtils.fsx"
open System
open System.IO
open System.IO.Compression
open System.Xml
open StreamUtils

let read(tsv) =
    let tsv = if tsv = "" then "streamlen.tsv" else tsv
    use sr = new StreamReader(tsv)
    let mutable pos = 0L
    sr.ReadLine(),
    [|  while not <| sr.EndOfStream do
        let len = sr.ReadLine() |> Convert.ToInt32
        yield pos, len
        pos <- pos + int64 len |]

let getPages(stream, length) = seq {
    use ss = new SubStream(stream, length)
    use cs = new ConcatStream([
        new MemoryStream("<pages>"B)
        new BZip2Stream(ss, CompressionMode.Decompress)
        new MemoryStream("</pages>"B) ])
    use xr = XmlReader.Create(cs)
    let mutable ns, id = 0, 0
    while xr.Read() do
        if xr.NodeType = XmlNodeType.Element then
            match xr.Name with
            | "ns" ->
                if xr.Read() then ns <- Convert.ToInt32 xr.Value
                id <- 0
            | "id" ->
                if id = 0 && xr.Read() then id <- Convert.ToInt32 xr.Value
            | "text" ->
                if ns = 0 && not xr.IsEmptyElement && xr.Read() then
                    yield id, seq {
                        use sr = new StringReader(xr.Value)
                        while sr.Peek() <> -1 do
                            yield sr.ReadLine() }
            | _ -> () }
