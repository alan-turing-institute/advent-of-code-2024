open System.IO

let input = 
//     "###############
// #.......#....E#
// #.#.###.#.###.#
// #.....#.#...#.#
// #.###.#####.#.#
// #.#.#.......#.#
// #.#.#####.###.#
// #...........#.#
// ###.#.#####.#.#
// #...#.....#.#.#
// #.#.#.###.#.#.#
// #.....#...#.#.#
// #.###.#.#.#.#.#
// #S..#.....#...#
// ###############".Split "\n"
    File.ReadAllLines "day-16/fsharp_evelinag/input.txt"


open System.Collections.Generic

type Direction = East | West | North | South
type Turn = Clockwise | Counterclockwise

let startRow, startCol = input.Length-2, 1


let goAhead (row, col, heading) =
    match heading with
    | East -> (row, col + 1, heading), 1
    | West -> (row, col - 1, heading), 1
    | North -> (row - 1, col, heading), 1
    | South -> (row + 1, col, heading), 1

let turn90 (row, col, heading) turnDirection = 
    match heading with
    | East -> 
        match turnDirection with
        | Clockwise -> (row, col, South), 1000
        | Counterclockwise -> (row, col, North), 1000
    | West ->
        match turnDirection with
        | Clockwise -> (row, col, North), 1000
        | Counterclockwise -> (row, col, South), 1000
    | North ->
        match turnDirection with
        | Clockwise -> (row, col, East), 1000
        | Counterclockwise -> (row, col, West), 1000
    | South ->
        match turnDirection with
        | Clockwise -> (row, col, West), 1000
        | Counterclockwise -> (row, col, East), 1000
    


let nextStates state =
    // options
    // - go ahead
    // - turn 90 degress clockwise
    // - turn 90 degrees counterclockwise
    [ 
        goAhead state
        turn90 state Clockwise
        turn90 state Counterclockwise
    ]
    |> List.filter (fun ((r, c, _), _ ) -> input.[r].[c] <> '#')


let bfs startRow startCol =
    // priority queue of score - path so far
    let pq = PriorityQueue<((int*int*Direction) list * int), int>()

    pq.Enqueue(([startRow, startCol, East], 0), 0)
    let mutable found = None
    let mutable (visited: (int * int * Direction) list) = []

    while pq.Count > 0 && found.IsNone do
        let pathSoFar, cost = pq.Dequeue()
        let (row, col, direction) = pathSoFar.Head
        if input.[row].[col] = 'E' then
            found <- Some(pathSoFar, cost)
        else 
            nextStates (row, col, direction)
            |> List.filter (fun (state, _) -> not (List.contains state visited))
            |> List.iter (fun (state, price) ->
                visited <- state::visited
                pq.Enqueue((state::pathSoFar, cost+ price), cost + price))

    found.Value

let result = bfs startRow startCol

// all best paths
let targetCost = snd result

let bfs2 startRow startCol targetCost =
    // priority queue of score - path so far
    let pq = PriorityQueue<((int*int*Direction) list * int), int>()

    pq.Enqueue(([startRow, startCol, East], 0), 0)

    let mutable finished = false
    let mutable (foundPaths: ((int*int*Direction) list) list) = []
    let visited = Dictionary<(int*int*Direction), int>() // closest distance

    while pq.Count > 0 && not finished do
        let pathSoFar, cost = pq.Dequeue()

        if cost > targetCost then 
            finished <- true
        else
            let (row, col, direction) = pathSoFar.Head
            if input.[row].[col] = 'E' then
                if cost <= targetCost then
                    foundPaths <- pathSoFar::foundPaths
            else 
                nextStates (row, col, direction)
                |> List.iter (fun ((x,y,d), value) -> 
                    if visited.ContainsKey((x,y,d)) then
                        // don't go further if visited before with lower cost
                        if visited.[(x,y,d)] >= cost + value then
                            visited.[(x,y,d)] <- cost + value
                            pq.Enqueue(((x,y,d)::pathSoFar, cost + value), cost + value)
                    else
                        visited.Add((x,y,d), value + cost)
                        pq.Enqueue(((x,y,d)::pathSoFar, cost + value), cost + value)

                    )

    foundPaths

let paths = bfs2 startRow startCol targetCost

let tiles = 
    paths
    |> List.concat 
    |> List.map (fun (x,y, _ ) -> x, y)
    |> List.distinct
    |> List.length