open System.IO
open System.Collections.Generic

let input =
//     "x00: 1
// x01: 0
// x02: 1
// x03: 1
// x04: 0
// y00: 1
// y01: 1
// y02: 1
// y03: 1
// y04: 1

// ntg XOR fgs -> mjb
// y02 OR x01 -> tnw
// kwq OR kpj -> z05
// x00 OR x03 -> fst
// tgd XOR rvg -> z01
// vdt OR tnw -> bfw
// bfw AND frj -> z10
// ffh OR nrd -> bqk
// y00 AND y03 -> djm
// y03 OR y00 -> psh
// bqk OR frj -> z08
// tnw OR fst -> frj
// gnj AND tgd -> z11
// bfw XOR mjb -> z00
// x03 OR x00 -> vdt
// gnj AND wpb -> z02
// x04 AND y00 -> kjc
// djm OR pbm -> qhw
// nrd AND vdt -> hwm
// kjc AND fst -> rvg
// y04 OR y02 -> fgs
// y01 AND x02 -> pbm
// ntg OR kjc -> kwq
// psh XOR fgs -> tgd
// qhw XOR tgd -> z09
// pbm OR djm -> kpj
// x03 XOR y03 -> ffh
// x00 XOR y04 -> ntg
// bfw OR bqk -> z06
// nrd XOR fgs -> wpb
// frj XOR qhw -> z04
// bqk OR frj -> z07
// y03 OR x01 -> nrd
// hwm AND bqk -> z03
// tgd XOR rvg -> z12
// tnw OR pbm -> gnj"
    File.ReadAllText "day-24/fsharp_evelinag/input.txt"

type Operation = { 
    Op : string
    X : string
    Y : string
    Result : string
}

let values, operations = 
    let parts = input.Split "\n\n"
    let values = Dictionary<string,int>()
    parts.[0].Split "\n"
    |> Array.iter (fun line -> 
        let xs = line.Split ": "
        values.Add(xs.[0], int xs.[1]))

    let operations = 
        parts.[1].Split "\n"
        |> Array.map (fun line -> 
            let xs = line.Split " -> "
            let operands = xs.[0].Split " "
            { Op = operands.[1]; X = operands.[0]; Y = operands.[2]; Result = xs.[1] })
    values, operations

let eval operation (values: Dictionary<string,int>) =
    let result = 
        match operation.Op with
        | "AND" -> 
            if values.[operation.X] = 1 && values.[operation.Y] = 1 then 1 else 0
        | "OR" -> if values.[operation.X] = 1 || values.[operation.Y] = 1 then 1 else 0
        | "XOR" -> if values.[operation.X] <> values.[operation.Y] then 1 else 0
    if values.ContainsKey(operation.Result) then
        values.[operation.Result] <- result
    else
        values.Add(operation.Result, result)

let rec evaluate (ops: Operation array) (values: Dictionary<string,int>)= 
    if ops.Length = 0 then 
        ()
    else
        let idx = 
            ops
            |> Array.findIndex (fun o ->
                values.ContainsKey(o.X) && values.ContainsKey(o.Y)
                )
        eval ops.[idx] values
        evaluate (Array.removeAt idx ops) values

evaluate operations values

let part1 = 
    values.Keys
    |> Seq.filter (fun k -> k.StartsWith "z")
    |> Seq.sortDescending
    |> Array.ofSeq
    |> Array.map (fun k -> string values.[k])
    |> String.concat ""
    |> fun s -> System.Convert.ToInt64(s, 2)

// part 2


// a + b is
// a XOR b XOR c 
// (a AND b) OR (c and (a XOR b)) for the next carry bit

let name x n = x + sprintf "%02d" n

let opsInput input = 
    operations
    |> Array.filter (fun o -> o.X = input || o.Y = input)

let opsInputs input1 input2 =
    operations 
    |> Array.filter (fun o -> (o.X = input1 || o.Y = input1) && (o.X = input2 || o.Y = input2))

let rec verifyOperations i (carryOption: string option) = 
    if i >= 45 then ()
    else
    let x = name "x" i
    let y = name "y" i
    let z = name "z" i

    try
        // operations involving x and y should be:
        // x AND y
        // x XOR y

        let xy = opsInputs x y

        let xyXorResult = xy |> Array.filter (fun o -> o.Op = "XOR") |> Array.tryExactlyOne
        let xyAndResult = xy |> Array.filter (fun o -> o.Op = "AND") |> Array.tryExactlyOne

        if xyXorResult.IsNone then printfn "%d: error 1" i
        if xyAndResult.IsNone then printfn "%d: error 2" i

        // z should be a result of `xyXorResult` XOR c (carry bit from previous operations)
        
        let zPresumably = 
            if carryOption.IsSome then
                opsInputs xyXorResult.Value.Result carryOption.Value
                |> Array.filter (fun o -> o.Result.StartsWith "z") 
                |> Array.tryExactlyOne
            else
                opsInput xyXorResult.Value.Result |> Array.filter (fun o -> o.Result.StartsWith "z") |> Array.tryExactlyOne

        if zPresumably.IsNone && i > 0 then 
            printfn "%d: error 3" i

        match carryOption with
        | Some carry ->
            if zPresumably.Value.X <> carry && zPresumably.Value.Y <> carry then
                printfn "%d: Error carry bit incorrect" i
        | None -> 
                ()

        if zPresumably.Value.Result <> z then 
            printfn "%d: Error zPresumably <> z" i

        // next carry bit computation
        let cAndXyXorResult =
            match carryOption with
            | Some carry ->
                opsInputs carry xyXorResult.Value.Result
                |> Array.filter (fun o -> o.Op = "AND")
                |> Array.tryExactlyOne
            | None ->
                // carry bit unknown or not existing (if i = 0)
                opsInput xyXorResult.Value.Result
                |> Array.filter (fun o -> o.Op = "AND")
                |> Array.tryExactlyOne
        if cAndXyXorResult.IsNone then printfn "%d: error 4" i

        let carry' = 
            opsInputs xyAndResult.Value.Result cAndXyXorResult.Value.Result
            |> Array.filter (fun o -> o.Op = "OR")
            |> Array.tryExactlyOne
        if carry'.IsNone then printfn "%d: error 5" i

        verifyOperations (i + 1) (Some(carry'.Value.Result))

    with _ -> 
        printfn "%d, %A: error" i carryOption
        verifyOperations (i+1) None

verifyOperations 0 None

// 7: error 3
// 7, Some "btq": error
// 17: error 3
// 17, Some "nmq": error
// 24: error 3
// 24, Some "nmp": error
// 32: error 5
// 32, Some "fth": error

// Manual analysis...
// let i = 32
// let carryOption = Some "fth"

let errors = 
    ["nqk"; "z07"; "fgt"; "pcp"; "z24"; "fpq"; "srn"; "z32" ]
    |> List.sort
    |> String.concat ","