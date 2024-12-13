open System.IO

let input = 
//     "Button A: X+94, Y+34
// Button B: X+22, Y+67
// Prize: X=8400, Y=5400

// Button A: X+26, Y+66
// Button B: X+67, Y+21
// Prize: X=12748, Y=12176

// Button A: X+17, Y+86
// Button B: X+84, Y+37
// Prize: X=7870, Y=6450

// Button A: X+69, Y+23
// Button B: X+27, Y+71
// Prize: X=18641, Y=10279"
    File.ReadAllText "day-13/fsharp_evelinag/input.txt"

let part2 = true

let parseButton (line: string) =
    line.Split ": "
    |> fun a -> a.[1].Split ", " 
    |> Array.map (fun x -> x.Replace("X+","").Replace("Y+","") |> int64)
    |> fun a -> a.[0], a.[1]

let parsePrize (line: string) =
    line.Split ": "
    |> fun a -> a.[1].Split ", "
    |> Array.map (fun x -> x.Replace("X=","").Replace("Y=","") |> int64)
    |> fun a -> 
        (if part2 then a.[0] + 10000000000000L else a.[0]), 
        (if part2 then a.[1] + 10000000000000L else a.[1])

let clawMachines=
    input.Split "\n\n"
    |> Array.map (fun machine ->
        let parts = machine.Split "\n"
        (parseButton parts.[0], parseButton parts.[1], parsePrize parts.[2])
        )
    
// Button A: a1, a2
// Button B: b1, b2
// Prize: n_A * a1 + n_B * b1, n_A * a2 + n_B * b2


let calculateCoefficients (a1, a2) (b1, b2) (x, y) = 
    
    let a1' = float a1
    let a2' = float a2
    let b1' = float b1
    let b2' = float b2
    let x' = float x
    let y' = float y


    let n_A' = (y' - b2'*x'/b1')/(a2'-b2'*a1'/b1')
    let n_B' = (x'-n_A'*a1')/b1'
    let n_A = int64(round(n_A'))
    let n_B = int64(round(n_B'))
    // int check?
    if n_A*a1 + n_B*b1 = x && n_A*a2 + n_B*b2 = y then
        Some(int64 n_A, int64 n_B)
    else None


let coefficients =
    clawMachines
    |> Array.mapi (fun i (buttonA, buttonB, prize) ->
        i, calculateCoefficients buttonA buttonB prize
        )
    |> Array.filter (fun (i, x) -> x.IsSome)
    |> Array.choose (fun (_, x) -> x)


let tokens = 
    coefficients
    |> Array.map (fun (n, m)-> n*3L + m*1L)
    |> Array.sum

