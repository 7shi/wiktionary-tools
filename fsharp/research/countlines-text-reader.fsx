#r "AR.Compression.BZip2.dll"
open System
open System.IO
open System.IO.Compression
open System.Xml

let target =
    use sr = new StreamReader("streamlen.tsv")
    sr.ReadLine()

let getPages(stream) = seq {
    use bs = new BZip2Stream(stream, CompressionMode.Decompress)
    use xr = XmlReader.Create(bs)
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

let mutable lines = 0
do
    use fs = new FileStream(target, FileMode.Open)
    for _, text in getPages(fs) do
        for _ in text do
            lines <- lines + 1
Console.WriteLine("lines: {0:#,0}", lines)
