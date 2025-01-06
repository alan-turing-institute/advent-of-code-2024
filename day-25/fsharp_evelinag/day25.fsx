open System.IO

let input = 
//     "#####
// .####
// .####
// .####
// .#.#.
// .#...
// .....

// #####
// ##.##
// .#.##
// ...##
// ...#.
// ...#.
// .....

// .....
// #....
// #....
// #...#
// #.#.#
// #.###
// #####

// .....
// .....
// #.#..
// ###..
// ###.#
// ###.#
// #####

// .....
// .....
// .....
// #....
// #.#..
// #.#.#
// #####"
    File.ReadAllText "day-25/fsharp_evelinag/input.txt"

let items = 
    input.Split "\n\n"
    |> Array.map (fun x -> x.Split "\n")

let locks = 
    items
    |> Array.filter (fun lines ->
        lines.[0] |> Seq.filter ((=) '#') |> Seq.length |> (=) lines.[0].Length)

let keys = 
    items
    |> Array.filter (fun lines ->
        lines.[0] |> Seq.filter ((=) '.') |> Seq.length |> (=) lines.[0].Length)

let toColumns (pins: string []) = 
    [| for i in 0..pins.[0].Length-1 ->
        pins
        |> Array.map (fun p -> p.[i])
        |> Array.sumBy (fun x -> if x = '#' then 1 else 0) |] 

let lockCodes = 
    locks
    |> Array.map (fun lock ->
        toColumns lock.[1..])

let keyCodes =
    keys
    |> Array.map (fun key -> toColumns key.[..key.Length-2])       

let fits =
    [ for lock in lockCodes do
        for key in keyCodes do
            let overlaps = 
                Seq.zip lock key
                |> Seq.fold (fun overlaps (x, y) -> overlaps || (x + y) > 5) false
            if not overlaps then 
                yield (lock, key) ]
    |> List.distinct
    |> List.length
            