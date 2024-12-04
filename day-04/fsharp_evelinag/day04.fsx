open System.IO


let input = File.ReadAllLines("day-04/fsharp_evelinag/input.txt")

// Pad the input so that I don't have to check bounds
let paddedInput = 
    Array.init (input.Length + 2) (fun i -> 
        if i < 1 || i >= input.Length + 1 then 
            Array.init (input.[0].Length + 2) (fun _ -> ".") |> String.concat ""
        else
            [| "."; input.[i-1]; "."|] 
            |> String.concat "")

let rec findWord (word: string) (i, j) getNextPosition acc =
    if acc = word then
        1
    else
        let nextLetter = string paddedInput.[i].[j]
        if acc + nextLetter = word.[..acc.Length] then
            // match, continue
            findWord word (getNextPosition i j) getNextPosition (acc + nextLetter)
        else    
            0

// all the ways to get next position, clockwise
let nextPositions = [|
    (fun i j -> i-1, j)
    (fun i j -> i-1, j+1)
    (fun i j -> i, j+1)
    (fun i j -> i+1, j+1)
    (fun i j -> i+1, j)
    (fun i j -> i+1, j-1)
    (fun i j -> i, j-1)
    (fun i j -> i-1, j-1)
|]

let countXMAS = 
    paddedInput
    |> Array.mapi (fun i row -> 
        row 
        |> Seq.mapi (fun j letter ->
            if letter = 'X' then
                nextPositions
                |> Array.map (fun getNextPosition ->
                    findWord "XMAS" (i,j) getNextPosition "")
                |> Array.sum
            else
                0)
        |> Seq.sum
        )
    |> Array.sum


// Part 2

let countX_MAS = 
    paddedInput
    |> Array.mapi (fun i row -> 
        row 
        |> Seq.mapi (fun j letter ->
            if letter = 'A' then
                let diag1 =
                    findWord "MAS" (i-1, j-1) (fun i j -> i+1, j+1) ""
                    + findWord "MAS" (i+1, j+1) (fun i j -> i-1, j-1) ""
                let diag2 = 
                    findWord "MAS" (i-1, j+1) (fun i j -> i+1, j-1) ""
                    + findWord "MAS" (i+1, j-1) (fun i j -> i-1, j+1) ""
                if diag1 + diag2 = 2 then
                    1
                else 
                    0
            else
                0)
        |> Seq.sum
        )
    |> Array.sum            