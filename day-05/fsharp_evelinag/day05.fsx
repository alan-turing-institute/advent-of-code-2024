open System.IO

let testInput = 
    "47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"


let data = 
    //testInput
    File.ReadAllText("day-05/fsharp_evelinag/input.txt")
    |> fun input -> input.Split "\n\n"

let pageOrders = 
    data.[0].Split "\n"
    |> Array.map (fun line -> 
        line.Split("|") 
        |> fun xs -> int xs.[0], int xs.[1])
    |> Set

let pagesToPrint =
    data.[1].Split("\n")
    |> Array.map (fun line -> 
        line.Split ","
        |> Array.map int)

let pageComparer x y =
    if pageOrders.Contains(x, y) then -1
    else if pageOrders.Contains(y, x) then 1
    else 0


let part1 = 
    pagesToPrint
    |> Array.filter (fun pages ->
        let sorted = pages |> Array.sortWith pageComparer 
        sorted = pages)
    |> Array.sumBy (fun xs-> xs.[xs.Length/2])


let part2 = 
    pagesToPrint
    |> Array.choose (fun pages ->
        let sorted = pages |> Array.sortWith pageComparer 
        if sorted <> pages then
            Some(sorted)
        else 
            None)
    |> Array.sumBy (fun xs-> xs.[xs.Length/2])

