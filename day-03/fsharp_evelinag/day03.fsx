open System.IO
open System.Text.RegularExpressions

let memory = //"xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
    File.ReadAllText("day-03/fsharp_evelinag/day03.txt")

let regexMul = Regex("mul\(([0-9]{1,3}),([0-9]{1,3})\)")
let matchesMul = regexMul.Matches(memory)

let getMulValue (m: Match) = 
    m.Groups
    |> Seq.skip 1
    |> Seq.map (fun g -> int g.Value)
    |> Seq.fold (*) 1

let result1 = 
    matchesMul
    |> Seq.map getMulValue

    |> Seq.sum

let regexAll = Regex("mul\(([0-9]{1,3}),([0-9]{1,3})\)|do\(\)|don't\(\)")
let matchesAll = regexAll.Matches(memory) |> Seq.toList

let rec evaluate (ms: Match list) acc enabled = 
    match ms with 
    | [] -> acc
    | m::ms' when m.Value.StartsWith("mul(") ->
        if enabled then 
            evaluate ms' (acc + getMulValue m) true
        else
            evaluate ms' acc false
    | m::ms' when m.Value = "do()" ->
        evaluate ms' acc true
    | m::ms' when m.Value = "don't()" ->
        evaluate ms' acc false

evaluate matchesAll 0 true
