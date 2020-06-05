open System
open System.Collections.Generic
open System.IO
open System.Xml

let args = Environment.GetCommandLineArgs()
let xml = args.[args.Length - 1]
if Path.GetExtension xml <> ".xml" then
    printfn "usage: CheckTag xml"
    exit 1

type Node(name:string) =
    let mutable count = 0
    let children = Dictionary<string, Node>()
    let getChild name =
        if children.ContainsKey name then
            children.[name]
        else
            let node = Node name
            children.[name] <- node
            node
    let isEnd (xr:XmlReader) =
        xr.NodeType = XmlNodeType.EndElement && xr.Name = name
    member __.Parse (xr:XmlReader) =
        count <- count + 1
        if xr.IsEmptyElement then () else
        while xr.Read() && not <| isEnd xr do
            if xr.NodeType = XmlNodeType.Element then
                (getChild xr.Name).Parse xr
    member __.Show() =
        for kv in children do kv.Value.Show("")
    member __.Show(indent) =
        Console.WriteLine("{0}{1} {2:#,0}", indent, name, count)
        for kv in children do kv.Value.Show(indent + "| ")

do
    use sr = new StreamReader(xml)
    use xr = XmlReader.Create(sr)
    let root = Node ""
    root.Parse xr
    printfn "%s" xml
    printfn ""
    root.Show()
