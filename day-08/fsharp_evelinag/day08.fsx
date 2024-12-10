open System.IO

// let input = 
//     "T.........
// ...T......
// .T........
// ..........
// ..........
// ..........
// ..........
// ..........
// ..........
// ..........".Split '\n'

let input = File.ReadAllLines "day-08/fsharp_evelinag/input.txt"

let antennas = 
    [| for i in 0..input.Length-1 do
        for j in 0..input.[0].Length-1 do 
            if input.[i].[j] <> '.' then 
                yield (input.[i].[j], (i,j)) |]

let getAntinodes (locations: (int*int)[]) =     
    [| for i in 0..locations.Length-1 do
        for j in i+1..locations.Length-1 do
            yield locations.[i], locations.[j] |]
    |> Array.collect (fun ((x1,y1), (x2, y2)) ->
            let antinode1 = x1 + (x1 - x2), y1 + (y1 - y2)
            let antinode2 = x2 + (x2 - x1), y2 + (y2 - y1)
            [| antinode1; antinode2 |]
        )  
    |> Array.filter (fun (x,y) -> 
        x >= 0 && x < input.Length && y >= 0 && y < input.[0].Length)     

let antinodeLocations = 
    antennas
    |> Array.groupBy fst
    |> Array.collect (fun (antenna, xs) ->
        let locations = Array.map snd xs
        getAntinodes locations
        )

let part1 = antinodeLocations |> Array.distinct |> Array.length    

// part 2

let getMoreAntinodes (locations: (int*int)[]) =     
    [| for i in 0..locations.Length-1 do
        for j in i+1..locations.Length-1 do
            yield locations.[i], locations.[j] |]
    |> Array.collect (fun ((x1,y1), (x2, y2)) ->
            let maxK = (max input.Length input.[0].Length)
            [|
                for k in -maxK..maxK do
                    yield x1 + k * (x1 - x2), y1 + k * (y1 - y2)
                    yield x2 + k * (x2 - x1), y2 + k * (y2 - y1)
            |]
        )  
    |> Array.filter (fun (x,y) -> 
        x >= 0 && x < input.Length && y >= 0 && y < input.[0].Length)     
    |> Array.append locations

let antinodeLocations2 = 
    antennas
    |> Array.groupBy fst
    |> Array.collect (fun (antenna, xs) ->
        let locations = Array.map snd xs
        getMoreAntinodes locations
        )

let part2 = 
    antinodeLocations2 |> Array.distinct |> Array.length


