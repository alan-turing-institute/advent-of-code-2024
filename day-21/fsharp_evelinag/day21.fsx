open System.IO
open System.Collections.Generic

let codes = 
//     "029A
// 980A
// 179A
// 456A
// 379A".Split "\n"
    File.ReadAllLines "day-21/fsharp_evelinag/input.txt"

let numericalKeypad = 
  [
    '0', (0,1)
    'A', (0,2)
    '1', (1,0)
    '2', (1,1)
    '3', (1,2)
    '4', (2,0)
    '5', (2,1)
    '6', (2,2)
    '7', (3,0)
    '8', (3,1)
    '9', (3,2)
    ] 

let directionalKeypad = 
    [
        '<', (0,0)
        'v', (0,1)
        '>', (0,2)
        '^', (1,1)
        'A', (1,2)
    ] 
    
let paths (keypad: (char*(int*int)) list) (forbiddenCoords: (int*int)) =
    (keypad, keypad)
    ||> List.allPairs
    |> List.map (fun ((x, (xRow, xCol)), (y, (yRow, yCol))) ->
            let colDist = yCol - xCol
            let rowDist = yRow - xRow

            let instructions = 
                [   // Getting this order right is a headache!
                    if colDist < 0 then yield! List.init (abs colDist) (fun _ -> "<")
                    if rowDist < 0 then yield! List.init (abs rowDist) (fun _ -> "v")
                    if rowDist > 0 then yield! List.init rowDist (fun _ -> "^")
                    if colDist > 0 then yield! List.init colDist (fun _ -> ">")
                ]
            let validInstructions = 
                // this part is probably not correct here!
                if forbiddenCoords = (xRow, yCol) || forbiddenCoords = (yRow, xCol) then
                    instructions |> List.rev    
                else
                    instructions 
            let path = 
                validInstructions |> String.concat "" 
                |> fun s -> s + "A"
            ((x, y), path)
        )
    |> dict

let numPaths = paths numericalKeypad (0,0)
let dirPaths = paths directionalKeypad (1,0)


let cache = Dictionary<(int * string), int64>()


let rec pathLength depth (code: string) =
    if depth = 0 then   
        let result = code.Length |> int64
        if not (cache.ContainsKey (depth, code)) then 
            cache.Add((depth, code), result)
        result
    else
        "A" + code 
        |> Seq.windowed 2 
        |> Seq.map (fun w -> 
            let x = w.[0]
            let y = w.[1]
            let path = 
                if (x >= '0' && x <= '9') || (y >= '0' && y <= '9') then 
                    numPaths.[x,y]
                else
                    dirPaths.[x,y]
            if cache.ContainsKey(depth, path) then 
                cache.[depth, path]
            else
                let result = pathLength (depth-1) path
                cache.Add((depth, path), result)
                result)
        |> Seq.sum


// depth = 3  for part 1
//       = 26 for part 2

cache.Clear()

codes
|> Array.map (fun code -> 
    let l = pathLength 26 code
    printfn "%A -> %A" code l
    l * int64 code.[..code.Length-2])
|> Array.sum

