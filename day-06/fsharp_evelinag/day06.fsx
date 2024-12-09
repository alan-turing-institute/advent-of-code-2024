open System.IO

// let lab = 
//     "....#.....
// .........#
// ..........
// ..#.......
// .......#..
// ..........
// .#..^.....
// ........#.
// #.........
// ......#...".Split('\n')

let lab = File.ReadAllLines("day-06/fsharp_evelinag/input.txt")

let start =
    lab 
    |> Array.mapi (fun rowIdx line -> 
        match Seq.tryFindIndex ((=)'^') line with
        | Some(colIdx) -> Some(rowIdx, colIdx)
        | None -> None)
    |> Array.choose id
    |> Array.exactlyOne

let outside (row, col) =
    row < 0 || col < 0 || row >= lab.Length || col >= lab.[0].Length

type Direction = Up | Down | Right | Left

let turnRight direction =
    match direction with
    | (1,0) -> (0,-1)
    | (0,1) -> (1,0)
    | (-1, 0) -> (0, 1)
    | (0, -1) -> (-1, 0)    

let getDirection directions = 
    match directions with
    | (-1, 0) -> Up
    | (1,0) -> Down
    | (0,1) -> Right
    | (0, -1) -> Left        

let rec step (rowIdx, colIdx) (directionRow, directionCol) visited =
    let nextRow, nextCol = rowIdx + directionRow, colIdx + directionCol
    if outside (nextRow, nextCol) then 
        (rowIdx, colIdx)::visited
    else
        match lab.[nextRow].[nextCol] with
        | '.' | '^' -> step (nextRow, nextCol) (directionRow, directionCol) ((rowIdx, colIdx)::visited)
        | '#' ->
            let nextDirection = turnRight (directionRow, directionCol)
            // turn only
            step (rowIdx, colIdx) nextDirection visited

let visitedLocations = 
    step start (-1,0) []
    |> List.distinct
let visitedCount = 
    visitedLocations.Length

// part 2

// TODO:
// - try adding an obstruction, detect loops
// - loop = visited same position in the same direction before

let obstacles =
    [ for rowIdx in 0..lab.Length - 1 do
        for colIdx in 0..lab.[0].Length-1 do
            if lab.[rowIdx].[colIdx] = '#' then 
                yield (rowIdx, colIdx)
            ]


       

let rec step2 obstacles (rowIdx, colIdx) (directionRow, directionCol) visited  =
    let nextRow, nextCol = rowIdx + directionRow, colIdx + directionCol
    let direction = getDirection (directionRow, directionCol)
    if outside (nextRow, nextCol) then 
        false
    else if List.contains (rowIdx, colIdx, direction) visited then
        true
    else
        if List.contains (nextRow, nextCol) obstacles then
            let nextDirection = turnRight (directionRow, directionCol)
            // turn only
            step2 obstacles (rowIdx, colIdx) nextDirection ((rowIdx, colIdx, direction)::visited)
        else
            step2 obstacles (nextRow, nextCol) (directionRow, directionCol) ((rowIdx, colIdx,direction)::visited)

let possibleObstructions =
    visitedLocations.[..visitedLocations.Length-2] // discard starting position

open FSharp.Collections

let part2 = 
    possibleObstructions
    |> Array.ofList
    |> Array.Parallel.filter (fun o ->
        // possible optimisation - start just before the obstruction
        step2 (o::obstacles) start (-1,0) [])
    |> Array.length
