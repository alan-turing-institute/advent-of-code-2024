open System.IO

let reports = 
    File.ReadAllLines("day-02/fsharp_evelinag/day-02.txt")
    |> Array.map (fun line -> 
            line.Split(' ') 
            |> Array.map int)

let isIncreasing (levels : int []) =
    levels
    |> Array.pairwise
    |> Array.fold (fun state (x1, x2) -> 
        state && (x2 > x1 && x2 - x1 >= 1 && x2 - x1 <= 3)) true

let isDecreasing = Array.rev >> isIncreasing

let safeCount = 
    reports
    |> Array.sumBy (fun report -> 
        if isIncreasing report || isDecreasing report then 1 else 0)

let isIncreasingWithDampener (levels: int []) =
    levels
    |> Array.mapi (fun i _ -> 
        let levels' = Array.append levels.[..i-1] levels.[i+1..]
        isIncreasing levels')
    |> Array.fold (fun state x -> state || x) false


let isDecreasingWithDampener = Array.rev >> isIncreasingWithDampener

let safeCountWithDampener = 
    reports
    |> Array.sumBy (fun report -> 
        if isIncreasingWithDampener report || isDecreasingWithDampener report then 1 else 0)