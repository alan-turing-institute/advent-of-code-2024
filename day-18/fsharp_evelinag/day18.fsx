open System.IO

let input =
//     "5,4
// 4,2
// 4,5
// 3,0
// 2,1
// 6,3
// 2,4
// 1,5
// 0,6
// 3,3
// 2,6
// 5,1
// 1,2
// 5,5
// 2,5
// 6,5
// 1,4
// 0,4
// 6,4
// 1,1
// 6,1
// 1,0
// 0,5
// 1,6
// 2,0"    .Split "\n"
//     |> Array.take 12

    File.ReadAllLines "day-18/fsharp_evelinag/input.txt"

let allPositions =
    input
    |> Array.map (fun line -> 
        let parts = line.Split ","
        int parts.[0], int parts.[1])

let positions count =
    allPositions
    |> Array.take count
    |> Set

let width, height = 71,71

// let printGrid (path: (int*int) list) =
//     [ for row in 0..height-1 ->
//        [ for col in 0..width-1 do
//             if positions.Contains ((col, row)) then 
//                 yield "#"
//             else if List.contains (col, row) path then
//                 yield "O"
//             else
//                 yield "."
//        ] 
//        |> String.concat ""]
//     |> String.concat "\n"
//     |> fun s -> printfn "%A\n" s

open System.Collections.Generic

let bfs xStart yStart blocked =
    // priority queue of score - path so far
    let q = Queue<(int*int) list>()

    q.Enqueue([(xStart,yStart)])
    let mutable found = None
    let mutable (visited: (int * int) list) = [(xStart, yStart)]

    while q.Count > 0 && found.IsNone do
        let pathSoFar= q.Dequeue()
        // printGrid pathSoFar
        let (x, y) = pathSoFar.Head
        if x = width-1 && y = height - 1 then
            found <- Some(pathSoFar)
        else 
            [
                x + 1, y
                x - 1, y
                x, y + 1
                x, y - 1
            ]
            |> List.filter (fun (col,row) -> col >= 0 && col < width && row >= 0 && row < height && not (Set.contains (col,row) blocked))
            |> List.filter (fun pos -> not (List.contains pos visited))
            |> List.iter (fun pos ->
                visited <- pos::visited
                q.Enqueue((pos::pathSoFar)))

    found


// part 1
let path = bfs 0 0 (positions 1024)   
path.Value.Length - 1

let rec firstBlocked n =
    if n >= allPositions.Length then
        None
    else
        let result = bfs 0 0 (positions n) 
        if result.IsNone then 
            Some(n-1)
        else
            firstBlocked (n+1)
    
let part2 = firstBlocked 1024
