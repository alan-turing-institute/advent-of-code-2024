open System.IO



let input = 
    File.ReadAllLines "day-22/fsharp_evelinag/input.txt"
    //[|1;2;3;2024|]
    |> Array.map int64

let mix value (secret: int64) = 
    secret ^^^ value

let prune (secret: int64) =
    secret % 16777216L   

let next (secret: int64) = 
    secret 
    |> mix (secret * 64L)
    |> prune
    |> fun s -> 
        let result =  s / 32L 
        mix result s
        |> prune
    |> fun s ->
        let result = s * 2048L
        mix result s
        |> prune

let rec generateNth n i secret = 
    if i = n then secret else generateNth n (i+1) (next secret)

let rec generate n i secret acc = 
    if n = i then
        secret::acc |> List.rev |> Array.ofList
    else
        let s' = next secret
        generate n (i+1) s' (secret::acc)

let part1 = 
    input
    |> Array.map (fun x -> generateNth 2000 0 x)
    |> Array.sum

let sequences = 
    input
    |> Array.map (fun x -> generate 2000 0 x [])

let prices = 
    sequences
    |> Array.map (fun secrets -> 
        secrets |> Array.map (fun x -> x % 10L |> int))

let changes = 
    prices
    |> Array.map (fun xs ->
        xs |> Array.windowed 2 |> Array.map (fun ys -> ys.[1] - ys.[0]))     

// best pattern is the most common one?
let bestPatternCandidates =
    let bestPrice = 
        prices
        |> Array.map (fun xs -> Array.max xs) 
    // find all the patterns that precede price of 9
    let maxIndices = 
        prices 
        |> Array.map (fun xs -> 
            xs |> Array.mapi (fun i x -> (i, x))
            |> Array.map fst)
    maxIndices
    |> Array.mapi (fun sequenceIdx maxIdx -> 
        [|
            for idx in maxIdx do
                if idx <= 3 then 
                    ()
                else
                    yield ( changes.[sequenceIdx].[idx-3..idx] )

        |]
        |> Array.distinct)
    |> Array.concat
    |> Array.countBy id 
    |> Array.sortByDescending snd


let bananas bestPattern = 
    changes
    |> Array.mapi (fun sequenceIdx xs ->
        xs
    //    |> Array.mapi (fun idx x -> (idx, x))
        |> Array.windowed 4 
        |> Array.mapi (fun i (ws) -> 
            (i, ws))
        |> Array.filter (fun (i, ws) -> ws = bestPattern)
        |> fun result -> 
            if result.Length = 0 then 0 
            else
            result.[0]
            |> fun (idx, _) ->
                    prices.[sequenceIdx].[idx + 4] )
    |> Array.sum

let part2 = 
    bestPatternCandidates
    |> Array.take 100
    |> Array.map (fun (pattern, count) ->
        let count = bananas pattern
        pattern, count)
    |> Array.maxBy snd
    |> snd