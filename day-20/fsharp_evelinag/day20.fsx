open System.IO

let input = 
//     "###############
// #...#...#.....#
// #.#.#.#.#.###.#
// #S#...#.#.#...#
// #######.#.#.###
// #######.#.#...#
// #######.#.###.#
// ###..E#...#...#
// ###.#######.###
// #...###...#...#
// #.#####.#.###.#
// #.#...#.#.#...#
// #.#.#.#.#.#.###
// #...#...#...###
// ###############".Split "\n"
    File.ReadAllLines "day-20/fsharp_evelinag/input.txt"


// plan 
// 1. find path, for every step along the way keep how many steps it take to reach E from there
//    dictionary: position -> distance to E
// 2. for every step along the path, in all directions (quite a lot of them) change two locations to '.'
// 3. See how many steps it takes from the new location (after 1 or 2 steps). New distance: from start + 1-2 + to end

// check - recalculate the path


open System.Collections.Generic

let searchPath (startRow, startCol)  =
    // priority queue of score - path so far
    let q = Queue<(int*int) list>()

    q.Enqueue([(startRow,startCol)])
    let mutable found = None
    let mutable (visited: (int * int) list) = [(startRow, startCol)]

    while q.Count > 0 && found.IsNone do
        let pathSoFar= q.Dequeue()
        let (x, y) = pathSoFar.Head
        if input.[x].[y] = 'E' then
            found <- Some(pathSoFar |> List.rev)
        else 
            [
                x + 1, y
                x - 1, y
                x, y + 1
                x, y - 1
            ]
            |> List.filter (fun (row,col) -> input.[row].[col] <> '#')
            |> List.filter (fun pos -> not (List.contains pos visited))
            |> List.iter (fun pos ->
                visited <- pos::visited
                q.Enqueue((pos::pathSoFar)))
    found


let start = 
    [ for i in 0..input.Length-1 do
        for j in 0..input.[0].Length-1 do
            if input.[i].[j] = 'S' then yield i,j ]
    |> List.exactlyOne
let path = searchPath start  |> Option.get
let pathLength = path.Length-1
// Actual input : 9476


let distances = Dictionary<(int*int), int>()
path
|> List.iteri (fun i location -> distances.Add(location, i))


let next (x: int, y: int) =
    [   x + 1, y
        x - 1, y 
        x, y + 1
        x, y - 1 ]

let cheatPositions (row, col) =
    let nextPositions =             
        next (row, col)
        |> List.filter (fun (x,y) -> input.[x].[y] = '#')
    
    let nextNext = 
        nextPositions
        |> List.collect (fun p -> 
            next p
            |> List.filter (fun (x,y) -> 
                x >= 0 && x < input.Length 
                && y >= 0 && y < input.[0].Length 
                && (x <> row || y <> col) 
                && input.[x].[y] <> '#')
        )
    
    nextNext

let savings2 =
    path
    |> List.collect (fun position -> 
        let cheats = 
            cheatPositions position
        // filter only those that shorten the path     
        let fromStart = distances.[position] 
        cheats 
        |> List.choose (fun cheat ->
                let toEnd = pathLength - distances.[cheat] 
                let saved = pathLength - (fromStart + toEnd + 2)
                if saved > 0 then Some (saved) else None )
        )

// savings
// |> List.countBy id
// |> List.sortBy fst
// |> printfn "%A"

savings2 
|> List.filter (fun x -> x >= 100)
|> List.length


let reachable (row, col) = 
    // all positions reachable in 20 steps 
    // circle in Manhattan distance

    [ for x in 0..input.Length-1 do
        for y in 0..input.[0].Length-1 do
            let steps = abs(x - row) + abs(y - col)
            if steps <= 20 then   
                yield (x,y), steps ]
        |> List.filter (fun ((x,y), steps) -> 
            x >= 0 && x < input.Length 
            && y >= 0 && y < input.[0].Length 
            && (x <> row || y <> col) 
            && input.[x].[y] <> '#')

let savings20 =
    path
    |> List.collect (fun position -> 
        let cheats = 
            reachable position
        // filter only those that shorten the path     
        let fromStart = distances.[position] 
        cheats 
        |> List.choose (fun (cheat, steps) ->
                let toEnd = pathLength - distances.[cheat] 
                let saved = pathLength - (fromStart + toEnd + steps)
                if saved > 0 then Some (saved) else None )
        )

// savings20 
// |> List.filter (fun x -> x >= 50)
// |> List.countBy id
// |> List.sortBy fst
// |> printfn "%A"

savings2 
|> List.filter (fun x -> x >= 100)
|> List.length

