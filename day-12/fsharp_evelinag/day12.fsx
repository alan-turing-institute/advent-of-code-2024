open System.IO

let input = 
//     "AAAAAA
// AAABBA
// AAABBA
// ABBAAA
// ABBAAA
// AAAAAA".Split "\n"
    File.ReadAllLines "day-12/fsharp_evelinag/input.txt"

// flood-filled grid 
let filled = 
    Array.init 
        (input.Length)
        (fun _ -> Array.init (input.[0].Length) (fun _ -> -1))

let rec floodFill value label (row, col) = 
    if row < 0 || col < 0 || row >= input.Length || col >= input.[0].Length then
        ()
    else
        if input.[row].[col] <> value || filled.[row].[col] <> -1 then
            ()
        else 
            filled.[row].[col] <- label
            floodFill value label (row - 1, col)
            floodFill value label (row, col - 1)
            floodFill value label (row + 1, col)
            floodFill value label (row, col + 1)

let mutable label = 0
for i in 0..input.Length-1 do
    for j in 0..input.[0].Length-1 do
        if filled.[i].[j] = -1 then
            floodFill input.[i].[j] label (i,j)
            label <- label + 1

let perimeters = System.Collections.Generic.Dictionary<int, int>()
for l in 0..label-1 do perimeters.Add(l, 0)

for i in 0..input.Length-1 do
    for j in 0..input.[0].Length-1 do
        // boundaries
        if i = 0 then // top
            perimeters.[filled.[i].[j]] <- perimeters.[filled.[i].[j]] + 1
        if j = 0 then // left
            perimeters.[filled.[i].[j]] <- perimeters.[filled.[i].[j]] + 1
        if i = input.Length-1 then // bottom
            perimeters.[filled.[i].[j]] <- perimeters.[filled.[i].[j]] + 1
        if j = input.[0].Length-1 then // right
            perimeters.[filled.[i].[j]] <- perimeters.[filled.[i].[j]] + 1

        if j <= input.[0].Length-2 then
            // look right 
            if filled.[i].[j] <> filled.[i].[j+1] then 
                perimeters.[filled.[i].[j]] <- perimeters.[filled.[i].[j]] + 1
                perimeters.[filled.[i].[j+1]] <- perimeters.[filled.[i].[j+1]] + 1
        if i <= input.Length - 2 then // look down
            if filled.[i].[j] <> filled.[i+1].[j] then
                perimeters.[filled.[i].[j]] <- perimeters.[filled.[i].[j]] + 1
                perimeters.[filled.[i+1].[j]] <- perimeters.[filled.[i+1].[j]] + 1

let sizes =
    filled 
    |> Array.concat
    |> Array.countBy id
    |> dict

let totalPrice = 
    [| 0..label-1 |]
    |> Array.sumBy (fun l -> 
        perimeters.[l] * sizes.[l])



// part 2 --------------

type Fence = {
    Row : int
    Col : int
    Above : int option
    Below : int option
}

let getHorizontalFences (filled: int[][]) = [
    for i in 0..filled.Length-1 do
        for j in 0..filled.[0].Length-1 do
            // top
            if i = 0 then 
                yield {Row = 0; Col = j; Above = None; Below = Some filled.[i].[j]}                
            // middle - look down
            if i <= filled.Length - 2 then 
                // look down
                if filled.[i].[j] <> filled.[i+1].[j] then
                    yield { Row = i+1; Col = j; Above = Some filled.[i].[j]; Below = Some filled.[i+1].[j] }
            // bottom
            if i = filled.Length-1 then // bottom
                yield { Row = i+1; Col = j; Above = Some filled.[i].[j]; Below = None }

    ]   

let mergeHorizontal (sections: Fence list) =
    // fence is merged if:
    // the row index is the same
    // column index is adjacent
    // and either above or below values are the same
    sections
    |> List.groupBy (fun f -> f.Row)
    |> List.map (fun (_, rowSections) -> 
         rowSections
         |> List.sortBy(fun f -> f.Col)
         |> List.fold (fun acc f ->
                match acc with
                | [] -> [f]
                | f'::processed ->
                    if f'.Col + 1 = f.Col 
                        && (f.Above = f'.Above || f.Below = f'.Below) then
                        f::processed
                    else
                        f::f'::processed
                ) []
         |> List.length
        )   
    |> List.sum

let getHorizontalCount filled = 
    sizes
    |> Seq.map (fun (KeyValue(l, size)) ->
        let fencesForLabel = 
            getHorizontalFences filled
            |> List.filter (fun f -> f.Above = Some l || f.Below = Some l)
        let count = mergeHorizontal fencesForLabel
        (l, count)
        )
    |> Array.ofSeq

let horizontals = getHorizontalCount filled |> dict
let verticals = 
    let filledFlipped = 
        Array.init filled.[0].Length (fun j ->
            Array.init filled.Length (fun i ->
                filled.[i].[j]))
    getHorizontalCount filledFlipped
    |> dict

[ 0..sizes.Count-1 ]
|> List.sumBy (fun l -> sizes.[l] * (horizontals.[l] + verticals.[l]))
