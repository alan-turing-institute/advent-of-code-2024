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
//     "#######
// #...#.#
// #.....#
// #..OO@#
// #..O..#
// #.....#
// #######

// <vv<<^^<<^^"
     File.ReadAllText "day-15/fsharp_evelinag/input.txt"

let warehouse, moves, robotRow, robotCol =
    let parts = input.Split "\n\n"
    let warehouse = 
        parts.[0].Split "\n"
        |> Array.map (fun line -> line |> Seq.toArray)
        |> Array.map (fun row ->
            [| for r in row do
                match r with
                | '.' -> yield '.'; yield '.'
                | '#' -> yield '#'; yield '#'
                | 'O' -> yield '['; yield ']'
                | '@' -> yield '@'; yield '.'
                |])
    let robotRow, robotCol = 
        [ for i in 0..warehouse.Length-1 do
            for j in 0..warehouse.[0].Length-1 do
                if warehouse.[i].[j] = '@' then yield (i,j)]
        |> List.exactlyOne 

    warehouse,
    parts.[1].Replace("\n", "") |> Seq.toList,
    robotRow,
    robotCol

let toString (warehouse: char[][]) = 
    // print the result
    [ for i in 0..warehouse.Length-1 do
        let s = String.concat "" (warehouse.[i] |> Array.map string)
        yield s ]
    |> String.concat "\n"

let rec moveBox direction row col (warehouseMap: char[][]) =
// Can we move a box in `direction` into the (row +-1 , col .. col+1) position?
    let nextRow, nextCol1, nextCol2 = 
        match direction with
        | '^' -> row - 1, col, col+1
        | 'v' -> row + 1, col, col+1
    match warehouseMap.[nextRow].[nextCol1], warehouseMap.[nextRow].[nextCol2] with
    | '.', '.' ->
        warehouseMap.[nextRow].[nextCol1] <- warehouseMap.[row].[col]
        warehouseMap.[nextRow].[nextCol2] <- warehouseMap.[row].[col+1]
        warehouseMap.[row].[col] <- '.'
        warehouseMap.[row].[col+1] <- '.'
        true, warehouseMap, nextRow, nextCol1
    | '#', _ | _, '#' ->
        false, warehouseMap, row, col
    | ']', '.' ->
        let changed, warehouseMap', row', col' = moveBox direction nextRow (nextCol1-1) warehouseMap
        if changed then 
            warehouseMap'.[nextRow].[nextCol1] <- warehouseMap'.[row].[col]
            warehouseMap'.[nextRow].[nextCol2] <- warehouseMap'.[row].[col+1]
            warehouseMap'.[row].[col] <- '.'
            warehouseMap'.[row].[col+1] <- '.'
            true, warehouseMap', nextRow, nextCol1
        else
            false, warehouseMap, row, col
    | '[', ']' ->
        let changed, warehouseMap', row', col' = moveBox direction nextRow (nextCol1) warehouseMap
        if changed then 
            warehouseMap'.[nextRow].[nextCol1] <- warehouseMap'.[row].[col]
            warehouseMap'.[nextRow].[nextCol2] <- warehouseMap'.[row].[col+1]
            warehouseMap'.[row].[col] <- '.'
            warehouseMap'.[row].[col+1] <- '.'
            true, warehouseMap', nextRow, nextCol1
        else
            false, warehouseMap, row, col
    | '.', '[' ->
        let changed, warehouseMap', row', col' = moveBox direction nextRow (nextCol2) warehouseMap
        if changed then 
            warehouseMap'.[nextRow].[nextCol1] <- warehouseMap'.[row].[col]
            warehouseMap'.[nextRow].[nextCol2] <- warehouseMap'.[row].[col+1]
            warehouseMap'.[row].[col] <- '.'
            warehouseMap'.[row].[col+1] <- '.'
            true, warehouseMap', nextRow, nextCol1
        else
            false, warehouseMap, row, col
    | ']','[' ->
        let wmap = 
            Array.init warehouseMap.Length (fun i -> Array.copy warehouseMap.[i])
        let changedLeft, wmap', row', col'' = moveBox direction nextRow (nextCol1-1) (wmap)
        let changedRight, wmap'', row'', col'' = moveBox direction nextRow (nextCol2) (wmap')
        if changedLeft && changedRight then 
            wmap''.[nextRow].[nextCol1] <- wmap''.[row].[col]
            wmap''.[nextRow].[nextCol2] <- wmap''.[row].[col+1]
            wmap''.[row].[col] <- '.'
            wmap''.[row].[col+1] <- '.'
            true, wmap'', nextRow, nextCol1
        else
            false, warehouseMap, row, col
    | x -> 
        printfn "===================" 
        printfn "%s" (toString warehouseMap)
        false, warehouseMap, row, col

        
 
    

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
    | '[' ->
        if direction = '<' || direction = '>' then 
            // same as part 1, box moves the same way as just two parentheses separately
            let changed, newMap, _, _ = move direction nextRow nextCol warehouseMap
            if changed then
                newMap.[nextRow].[nextCol] <- newMap.[row].[col]
                warehouseMap.[row].[col] <- '.'
                true, newMap, nextRow, nextCol
            else
                false, warehouseMap, row, col
        else 
            let changed, newMap, _ , _  = moveBox direction nextRow nextCol (warehouseMap)
            if changed then
                newMap.[nextRow].[nextCol] <- newMap.[row].[col]
                warehouseMap.[row].[col] <- '.'
                true, newMap, nextRow, nextCol
            else
                false, warehouseMap, row, col

    | ']' -> 
        if direction = '<' || direction = '>' then
            // same as part 1, box moves the same way as just two parentheses separately
            let changed, newMap, _, _ = move direction nextRow nextCol warehouseMap
            if changed then
                newMap.[nextRow].[nextCol] <- newMap.[row].[col]
                warehouseMap.[row].[col] <- '.' 
                true, newMap, nextRow, nextCol
            else
                false, warehouseMap, row, col
        else 
            let changed, newMap, _, _ = moveBox direction nextRow (nextCol-1) (warehouseMap)
            if changed then
                newMap.[nextRow].[nextCol] <- newMap.[row].[col]
                warehouseMap.[row].[col] <- '.'
                true, newMap, nextRow, nextCol
            else
                false, warehouseMap, row, col

    | '.' | _ ->
        warehouseMap.[nextRow].[nextCol] <- warehouseMap.[row].[col]
        warehouseMap.[row].[col] <- '.'
        true, warehouseMap, nextRow, nextCol


let rec simulateRobot moves robotRow robotCol warehouseMap =
    match moves with
    | [] -> warehouseMap
    | m::ms ->
        let changed, warehouseMap', row,col = move m robotRow robotCol warehouseMap
        if changed then
            warehouseMap'.[robotRow].[robotCol] <- '.'
        // File.AppendAllText("day-15/fsharp_evelinag/log.txt", "\nstep: " + string m + " ---------\n")
        // File.AppendAllText("day-15/fsharp_evelinag/log.txt", toString warehouseMap)
        simulateRobot ms row col warehouseMap'


let gps (warehouse: char[][]) = 
    [ for i in 0..warehouse.Length-1 do 
        for j in 0..warehouse.[0].Length-1 do
            if warehouse.[i].[j] = '[' then 
                let rowIdx = i
                let colIdx = j

                yield rowIdx * 100 + colIdx]
    |> List.sum

let warehouse' = simulateRobot moves robotRow robotCol warehouse
toString warehouse' |> printfn "%s"

gps warehouse'


