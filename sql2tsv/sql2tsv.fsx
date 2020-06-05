open System
open System.IO
open System.Text

let readString (src:string) pos =
    let length = src.Length
    if pos >= length || src.[pos] <> '\'' then None else
    let mutable pos = pos + 1
    let sb = StringBuilder()
    while pos < length && src.[pos] <> '\'' do
        if src.[pos] = '\\' then
            pos <- pos + 1
            let ch = if pos < length then src.[pos] else ' '
            if not (ch = '"' || ch = '\'' || ch = '\\') then
                sb.Append '\\' |> ignore
        if pos < length then
            sb.Append src.[pos] |> ignore
            pos <- pos + 1
    if pos < length && src.[pos] = '\'' then pos <- pos + 1
    Some (sb.ToString(), pos)

#if TEST
do
    let src = @"'a,b','c\'d'"
    let rec f pos =
        match readString src pos with
        | Some (s, p) ->
            printfn "readString %A %d -> %A" src pos (s, p)
            f (p + 1)
        | _ -> ()
    f 0
#endif

let readValue (src:string) pos =
    let length = src.Length
    if pos >= length then None else
    let sp = readString src pos
    if sp.IsSome then sp else
    let mutable p = pos
    while p < length && src.[p] <> ',' && src.[p] <> ')' do
        p <- p + 1
    Some (src.[pos .. p - 1], p)

#if TEST
for src in ["1,2,3"; @"1,'a,b','c\'d'"] do
    let rec f pos =
        match readValue src pos with
        | Some (s, p) ->
            printfn "read_value %A %d -> %A" src pos (s, p)
            f (p + 1)
        | _ -> ()
    f 0
#endif

let readValues (src:string) pos =
    let length = src.Length
    if pos >= length || src.[pos] <> '(' then None else
    let mutable pos = pos + 1
    let ret = [|
        if pos >= length || src.[pos] = ')' then () else
        let mutable loop = true
        while loop do
            match readValue src pos with
            | Some (s, p) ->
                yield s
                if p < length && src.[p] = ',' then pos <- p + 1 else
                pos  <- p
                loop <- false
            | _ -> loop <- false |]
    if pos < length && src.[pos] = ')' then pos <- pos + 1
    Some (ret, pos)

#if TEST
for src in ["(1,2,3)"; @"(1,'a,b','c\'d')"] do
    match readValues src 0 with
    | Some sp -> printfn "readValues %A %d -> %A" src 0 sp
    | _ -> ()
#endif

let readAllValues (src:string) pos = seq {
    let length = src.Length
    let mutable pos  = pos
    let mutable loop = true
    while loop do
        match readValues src pos with
        | Some (s, p) ->
            yield s
            if p < length && src.[p] = ',' then pos <- p + 1 else
            pos  <- p
            loop <- false
        | _ -> loop <- false }

#if TEST
do
    let src = @"(1,2,3),(1,'a,b','c\'d')"
    printfn "readAllValues %A %d -> %A" src 0 (readAllValues src 0)
#endif

let readSql (stream:TextReader) = seq {
    let mutable line = ""
    let read() =
        line <- stream.ReadLine()
        not (isNull line)
    while read() do
        if line.StartsWith("INSERT INTO ") then
            let p = line.IndexOf "VALUES ("
            if p >= 0 then yield! readAllValues line (p + 7) }

#if TEST
do
    let src = @"
INSERT INTO `table` VALUES (1,2,3),(4,5,6);
INSERT INTO `table` VALUES (1,'a,b','c\'d');".Trim()
    use sr = new StringReader(src)
    printfn "read_sql(%A)" src
    printfn "-> %A" (readSql sr)
#endif

open System.IO.Compression

let args = Environment.GetCommandLineArgs()
let target = Array.last args
if not (target.EndsWith ".sql" || target.EndsWith ".sql.gz") then
    printfn "usage: sql2tsv sql[.gz]"
    exit 1
let tsv = target.[.. target.LastIndexOf ".sql"] + "tsv"
do
    use sr =
        if target.EndsWith ".sql" then new StreamReader(target) else
        let fs = new FileStream(target, FileMode.Open)
        let gs = new GZipStream(fs, CompressionMode.Decompress)
        new StreamReader(gs)
    use sw = new StreamWriter(tsv)
    sw.NewLine <- "\n"
    for values in readSql sr do
        sw.WriteLine(String.concat "\t" values)
