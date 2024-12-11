open System.IO
open System

//let input = "125 17"
let input = File.ReadAllText "day-11/fsharp_evelinag/input.txt"

let pebbles = input.Split (" ") |> Array.map int64

let rec blink remaining (pebbles: int64 []) =
    if remaining = 0 then
        pebbles
    else 
        blink 
            (remaining - 1)
            [| for p in pebbles do
                let numDigits = int ((floor (Math.Log10(float p))) + 1.)
                match p with 
                | 0L -> yield 1L
                | x when numDigits % 2 = 0 ->
                    let s = string x
                    yield int64 s.[..numDigits/2-1]
                    yield int64 s.[numDigits/2..]
                | x -> yield x * 2024L
                |]

let result = blink 25 pebbles       

result
|> Array.length    


// Observations:
// - the order doesn't matter
// - numbers will reoccur MANY times
// Solution:
// keep a dictionary with the following:
// (number, number of times it occurs in the sequence)


let pebbleDict = 
    pebbles
    |> Array.countBy id
    |> Array.map (fun (x, y) -> x, int64 y)
    |> dict

let countPebbles (pebbleDict: Collections.Generic.IDictionary<int64,int64>) =
    pebbleDict.Values
    |> Seq.sum

let rec blink2 remaining (pebbleDict: Collections.Generic.IDictionary<int64,int64>) =
    if remaining = 0 then
        pebbleDict
    else
        let pebbleDict' = Collections.Generic.Dictionary<int64, int64>()
        for p in pebbleDict.Keys do
            let numDigits = int ((floor (Math.Log10(float p))) + 1.)
            let count = pebbleDict.[p]
            match p with 
            | 0L -> 
                if pebbleDict'.ContainsKey(1L) then
                    pebbleDict'.[1L] <- pebbleDict'.[1L] + count
                else
                    pebbleDict'.Add(1L, count)
            | x when numDigits % 2 = 0 ->
                let s = string x
                let key1 = int64 s.[..numDigits/2-1]
                let key2 = int64 s.[numDigits/2..]

                if pebbleDict'.ContainsKey key1 then
                    pebbleDict'.[key1] <- pebbleDict'.[key1] + count
                else    
                    pebbleDict'.Add(key1, count)
                
                if pebbleDict'.ContainsKey key2 then
                    pebbleDict'.[key2] <- pebbleDict'.[key2] + count
                else    
                    pebbleDict'.Add(key2, count)

            | x -> 
                let key = x * 2024L
                if pebbleDict'.ContainsKey key then
                    pebbleDict'.[key] <- pebbleDict'.[key] + count
                else    
                    pebbleDict'.Add(key, count)
        blink2 (remaining - 1) pebbleDict'

let n = 75
let pebbleDict' = blink2 n pebbleDict
countPebbles pebbleDict'