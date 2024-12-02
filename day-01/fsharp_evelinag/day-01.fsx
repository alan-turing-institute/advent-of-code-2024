open System.IO

let list1, list2 = 
    File.ReadAllLines("day-01/fsharp_evelinag/day-01.txt")
    |> Array.map (fun line -> 
        let items = line.Split("   ")
        int items.[0], int items.[1])
    |> Array.unzip

let distance = 
    (list1 |> Array.sort, list2 |> Array.sort)
    ||> Array.map2 (fun x1 x2 -> abs(x1 - x2))
    |> Array.sum

let countLookup = 
    list2 
    |> Array.countBy id
    |> dict

let similarityScore = 
    list1
    |> Array.sumBy (fun x ->
        if countLookup.ContainsKey x then  
            x * countLookup[x]
        else 
            0)    
