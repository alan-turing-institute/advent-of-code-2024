open System.IO

let input = 
//     "r, wr, b, g, bwu, rb, gb, br

// brwrr
// bggr
// gbbr
// rrbgbr
// ubwu
// bwurrg
// brgr
// bbrgwb"
    File.ReadAllText "day-19/fsharp_evelinag/input.txt"


let towels, designs =
    let parts = input.Split "\n\n"
    let towels = parts.[0].Split ", "
    let patterns = parts.[1].Split "\n"

    towels, patterns

let cache = System.Collections.Generic.Dictionary<string, bool>()


let rec isPossible design =
    match design with
    | "" -> true
    | pattern ->
        match cache.TryGetValue(pattern) with
        | true, value -> value
        | false, _ ->
            let result = 
                towels
                |> Array.filter (fun towel -> pattern.StartsWith(towel))
                |> Array.fold (fun isMatch towel ->
                    isMatch || isPossible design.[towel.Length..]) false
            cache.Add(pattern, result)
            result    

let part1 = 
    designs
    |> Array.map isPossible
    |> Array.filter id
    |> Array.length


let cache2 = System.Collections.Generic.Dictionary<string, int64>()


let rec countArrangements design =
    match design with
    | "" -> 1L
    | pattern ->
        match cache2.TryGetValue(pattern) with
        | true, value -> value
        | false, _ ->
            let result = 
                towels
                |> Array.filter (fun towel -> pattern.StartsWith(towel))
                |> Array.sumBy (fun towel -> countArrangements design.[towel.Length..])
            cache2.Add(pattern, result)
            result    

let part2 = 
    designs
    |> Array.map countArrangements
    |> Array.sum