open System.IO


let input = File.ReadAllLines "day-14/fsharp_evelinag/input.txt"
let width, height = 101,103


let positions, velocities =
    input
    |> Array.map (fun line -> 
        line.Replace("p=", "").Replace("v=", "").Split " "
        |> Array.map (fun xs -> xs.Split "," |> Array.map int))
    |> Array.map (fun robot ->
        (robot.[0].[0], robot.[0].[1]), (robot.[1].[0], robot.[1].[1]))
    |> Array.unzip

let update (p1,p2) (v1,v2) nSeconds=
    let p1' = 
        if v1 >= 0 then (p1 + nSeconds*v1)%width
        else ((p1 + nSeconds*v1)%width + width)%width
    let p2' = 
        if v2 >= 0 then (p2 + nSeconds*v2)%height
        else ((p2 + nSeconds*v2)%height + height)%height
    p1', p2'

let update1 (p1,p2) (v1,v2) =
    let p1' = 
        if v1 >= 0 then (p1 + v1)%width
        else (p1 + width + v1)%width
    let p2' = 
        if v2 >= 0 then (p2 + v2)%height
        else (p2 + height + v2)%height
    p1', p2'
    
let newPositions =
    (positions, velocities)
    ||> Array.map2 (fun p v -> update p v 100)

let score =
    let q1 =
        newPositions
        |> Array.filter (fun (x,y) ->
            x < width/2 && y < height/2)
        |> Array.length
    let q2 =
        newPositions
        |> Array.filter (fun (x,y) ->
            x > width/2  && y < height/2)
        |> Array.length
    let q3 =
        newPositions
        |> Array.filter (fun (x,y) ->
            x < width/2 && y > height/2  )
        |> Array.length    
    let q4 =
        newPositions
        |> Array.filter (fun (x,y) ->
            x > width/2 && y > height/2 )
        |> Array.length    
    q1 * q2 * q3 * q4


// part 2

let isSomewhatSymmetric positions =          
    // find how many have a vertical line 
    let allPositions = positions |> Set
    let symmetricCount = 
        positions
        |> Array.filter (fun (x,y) ->
                x < width/2)
        |> Array.fold (fun count (x, y) ->
            if allPositions.Contains (width - x - 1, y)
                then (count + 1)
            else count) 0
    if symmetricCount > 40 then
        true 
    else false

let rec findTree nSeconds positions =
    if nSeconds = 100000 then
        0
    else
        let positions' = 
            (positions, velocities) 
            ||> Array.map2 update1
        if isSomewhatSymmetric positions' then 
            nSeconds
        else 
            findTree (nSeconds+1) positions'

let iter = findTree 1 positions


let print (positions: (int*int) []) = 
    let ps = positions |> Set
    for j in 0..height-1 do
        for i in 0..width-1 do
        
            if ps.Contains(i,j) then 
                printf "X"
            else 
                printf " "
        printf "\n"

(positions, velocities)
||> Array.map2 (fun p v -> update p v iter)
|> print