open System.IO

let input = 
//     "89010123
// 78121874
// 87430965
// 96549874
// 45678903
// 32019012
// 01329801
// 10456732".Split "\n"
    File.ReadAllLines "day-10/fsharp_evelinag/input.txt"
    
let topomap = 
    let parsed = 
        input
        |> Array.map (fun line -> 
            line
            |> Seq.map (fun x -> 
                string x 
                |> fun x -> if x = "." then -1 else int x)
            |> Array.ofSeq)
    // padding
    Array.init (parsed.Length + 2) (fun row ->
        Array.init (parsed.[0].Length + 2) (fun col ->
            if row = 0 || col = 0 || row = parsed.Length+1 || col >= parsed.[0].Length+1 then
                    -1
            else
                parsed.[row-1].[col-1]))

let trailheads =
    [| for i in 0..topomap.Length - 1 do
        for j in 0..topomap.[0].Length-1 do
            if topomap.[i].[j] = 0 then yield (i,j) |]

// current position (row, col)
// elevation - expected elevation at the position
let rec trailSearch (row, col) elevation =
    match topomap.[row].[col] with
    | e when e = elevation ->
        if e = 9 then 
            [ (row, col) ]
        else
            // continue
            [   trailSearch (row-1, col) (e+1);
                trailSearch (row, col+1) (e+1);
                trailSearch (row+1,col) (e+1);
                trailSearch (row, col-1) (e+1) ]
            |> List.concat
            //|> List.distinct      // uncomment for part 1, comment out for part 2
    | _ -> [] // fail
                     
trailheads
|> Array.map (fun position -> 
    let reachablePeaks = trailSearch position 0
    reachablePeaks
    |> List.length )
|> Array.sum
