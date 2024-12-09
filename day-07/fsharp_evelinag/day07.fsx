open System.IO

// let input = 
//     "190: 10 19
// 3267: 81 40 27
// 83: 17 5
// 156: 15 6
// 7290: 6 8 6 15
// 161011: 16 10 13
// 192: 17 8 14
// 21037: 9 7 18 13
// 292: 11 6 16 20".Split "\n"

let input = File.ReadAllLines("day-07/fsharp_evelinag/input.txt")

let parseLine (line: string) =
    let parts = line.Split(": ")
    let numbers = 
        parts.[1].Split(" ") 
        |> Array.map bigint.Parse 
        |> List.ofArray
    bigint.Parse parts.[0], numbers

 
let inputValues = 
    input
    |> Array.map parseLine    

let combineDigits (x: System.Numerics.BigInteger) (y: System.Numerics.BigInteger) =
    string x + string y 
    |> bigint.Parse

let rec placeOperator (result: System.Numerics.BigInteger) values resultAcc operands =
    match values with
    | [] -> 
        if resultAcc = result then 
            true
        else
            false
    | x::xs ->
        if result < resultAcc then 
            false
        else
            operands
            |> List.fold (fun state op ->
                state
                || placeOperator result xs (op resultAcc x) operands) false

let part1 =
    inputValues
    |> Array.filter (fun (result, values) -> 
        placeOperator result values.Tail values.Head [(+); (*)])            
    |> Array.sumBy fst


let part2 =
    inputValues
    |> Array.filter (fun (result, values) -> 
        placeOperator result values.Tail values.Head [(+); (*); combineDigits])            
    |> Array.sumBy fst

