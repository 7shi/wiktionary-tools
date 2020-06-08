open System
open System.IO

type SubStream(stream: Stream, length) =
    inherit Stream()
    let mutable position = 0
    override __.CanRead  = true
    override __.CanWrite = false
    override __.CanSeek  = false
    override __.Length   = int64 length
    override __.Flush()  = raise <| NotSupportedException()
    override __.Position with get() = int64 position
                         and  set _ = raise <| NotSupportedException()
    override __.Seek(_, _)     = raise <| NotSupportedException()
    override __.SetLength(_)   = raise <| NotSupportedException()
    override __.Write(_, _, _) = raise <| NotSupportedException()
    override __.Read(array, offset, count) =
        if position >= length then 0 else
        let rlen = min count (length - position)
        let ret  = stream.Read(array, offset, rlen)
        position <- position + ret
        ret

type ConcatStream(streams: Stream seq, leaveOpen: bool) =
    inherit Stream()
    let enumerator = streams.GetEnumerator()
    let mutable eos = not <| enumerator.MoveNext()
    let mutable position = 0L
    new(streams) = new ConcatStream(streams, false)
    override __.Dispose disposing =
        if not leaveOpen && disposing then
            while not eos do
                enumerator.Current.Dispose()
                eos <- not <| enumerator.MoveNext()
        base.Dispose disposing
    override __.CanRead  = true
    override __.CanWrite = false
    override __.CanSeek  = false
    override __.Length   = raise <| NotSupportedException()
    override __.Flush()  = raise <| NotSupportedException()
    override __.Position with get() = position
                         and  set _ = raise <| NotSupportedException()
    override __.Seek(_, _)     = raise <| NotSupportedException()
    override __.SetLength(_)   = raise <| NotSupportedException()
    override __.Write(_, _, _) = raise <| NotSupportedException()
    override __.Read(array, offset, count) =
        let mutable ret = 0
        while not eos && ret = 0 do
            ret <- enumerator.Current.Read(array, offset, count)
            if ret = 0 then
                if not leaveOpen then enumerator.Current.Dispose()
                eos <- not <| enumerator.MoveNext()
        position <- position + int64 ret
        ret

do
    let frames = Diagnostics.StackTrace().GetFrames()
                 |> Array.map (fun frame -> frame.GetMethod().Name)
    if frames.[0] <> "main@" || Array.contains "EvalParsedSourceFiles" frames then () else
    do
        use ms  = new MemoryStream([|'a'B..'z'B|])
        use ss1 = new SubStream(ms, 10)
        use ss2 = new SubStream(ms, 10)
        use sr1 = new StreamReader(ss1)
        use sr2 = new StreamReader(ss2)
        use sr3 = new StreamReader(ms)
        printfn "%s" (sr1.ReadToEnd())
        printfn "%s" (sr2.ReadToEnd())
        printfn "%s" (sr3.ReadToEnd())
    do
        use cs = new ConcatStream([
            new MemoryStream([|'0'B..'4'B|])
            new MemoryStream([|'A'B..'Z'B|])
            new MemoryStream([|'5'B..'9'B|])
        ])
        use sr = new StreamReader(cs)
        printfn "%s" (sr.ReadToEnd())
    do
        use ms1 = new MemoryStream([|'A'B..'Z'B|])
        use ms2 = new MemoryStream([|'0'B..'4'B|])
        ms1.Position <- 10L
        use ss = new SubStream(ms1, 10)
        use cs = new ConcatStream([ss; ms2])
        use sr = new StreamReader(cs)
        printfn "%s" (sr.ReadToEnd())
