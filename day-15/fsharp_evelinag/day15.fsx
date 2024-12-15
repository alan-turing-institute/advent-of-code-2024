open System.IO

let input =
//     "##########
// #..O..O.O#
// #......O.#
// #.OO..O.O#
// #..O@..O.#
// #O#..O...#
// #O..O..O.#
// #.OO.O.OO#
// #....O...#
// ##########

// <vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
// vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
// ><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
// <<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
// ^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
// ^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
// >^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
// <><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
// ^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
// v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"
//     "########
// #..O.O.#
// ##@.O..#
// #...O..#
// #.#.O..#
// #...O..#
// #......#
// ########

// <^^>>>vv<v>>v<<"
    File.ReadAllText "day-15/fsharp_evelinag/input.txt"

let warehouse, moves, robotRow, robotCol =
    let parts = input.Split "\n\n"
    let warehouse = 
        parts.[0].Split "\n"
        |> Array.map (fun line -> line |> Seq.toArray)
    let robotRow, robotCol = 
        [ for i in 0..warehouse.Length-1 do
            for j in 0..warehouse.[0].Length-1 do
                if warehouse.[i].[j] = '@' then yield (i,j)]
        |> List.exactlyOne 

    warehouse,
    parts.[1].Replace("\n", "") |> Seq.toList,
    robotRow,
    robotCol


let rec move direction row col (warehouseMap: char[][]) =
    // intention to move from specified position in the specified direction
    let nextRow, nextCol = 
        match direction with
        | '^' -> row - 1, col
        | '>' -> row, col + 1
        | 'v' -> row + 1, col
        | '<' -> row, col - 1
    match warehouseMap.[nextRow].[nextCol] with
    | '#' -> false, warehouseMap, row, col
    | 'O' -> 
        let changed, newMap, _, _ = move direction nextRow nextCol warehouseMap
        if changed then
            newMap.[nextRow].[nextCol] <- newMap.[row].[col]
            true, newMap, nextRow, nextCol
        else
            false, warehouseMap, row, col

    | '.' | _ ->
        warehouseMap.[nextRow].[nextCol] <- warehouseMap.[row].[col]
        warehouseMap.[row].[col] <- '.'
        true, warehouseMap, nextRow, nextCol





let rec robotMove moves robotRow robotCol warehouseMap =
    match moves with
    | [] -> warehouseMap
    | m::ms ->
        let changed, warehouseMap', row,col = move m robotRow robotCol warehouseMap
        if changed then
            warehouseMap'.[robotRow].[robotCol] <- '.'
        robotMove ms row col warehouseMap'

let gps (warehouse: char[][]) = 
    [ for i in 1..warehouse.Length-2 do 
        for j in 1..warehouse.[0].Length-2 do
            if warehouse.[i].[j] = 'O' then 
                yield i * 100 + j]
    |> List.sum

let warehouse' = robotMove moves robotRow robotCol warehouse

gps warehouse'

for i in 0..warehouse'.Length-1 do
    let s = String.concat "" (warehouse'.[i] |> Array.map string)
    printfn "%A" s


