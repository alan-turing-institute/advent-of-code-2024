open System.IO

let input = 
//     "Register A: 729
// Register B: 0
// Register C: 0

// Program: 0,1,5,4,3,0"
   File.ReadAllText "day-17/fsharp_evelinag/input.txt"
//     "Register A: 2024
// Register B: 0
// Register C: 0

// Program: 0,3,5,4,3,0"

type Computer = {
    A: int64
    B: int64
    C: int64
    InstructionPointer: int
    Program : int list
}

let comp =
    let parts = input.Split "\n\n"

    let registers =
        parts.[0].Split "\n"
        |> Array.map (fun line -> 
            line.Split ": " |> fun a -> a.[1] |> int64)

    let program = 
        parts.[1].Split ": " 
        |> fun a -> a.[1].Split ","
        |> Array.map int

    {
        A = registers.[0]
        B = registers.[1]
        C = registers.[2]
        InstructionPointer = 0
        Program = program |> List.ofArray
    }

let comboOperand x (comp: Computer) = 
    match x with
    | 0 | 1 | 2 | 3 -> int64 x
    | 4 -> comp.A
    | 5 -> comp.B
    | 6 -> comp.C
    | 7 | _ -> failwith  ("Unexpected combo operand: " + string x)

let rec execute (comp: Computer) (acc: int list) =
    if comp.InstructionPointer >= comp.Program.Length then
        acc |> List.rev
    else

    // File.AppendAllText("day-17/fsharp_evelinag/log.csv",
    //     string comp.A + ",\"" + acc + "\"\n")

    let opcode = comp.Program.[comp.InstructionPointer]
    let operand = comp.Program.[comp.InstructionPointer+1]

    match opcode with
    | 0 ->
        //The adv instruction (opcode 0) performs division. The numerator is the value in the A register. The denominator is found by raising 2 to the power of the instruction's combo operand. (So, an operand of 2 would divide A by 4 (2^2); an operand of 5 would divide A by 2^B.) The result of the division operation is truncated to an integer and then written to the A register.
        let numerator = comp.A
        let denominator = 2.**(float (comboOperand operand comp))
        let result = (float numerator)/denominator |> floor |> int64

        execute { comp with A = result; InstructionPointer = comp.InstructionPointer + 2} acc

    | 1 ->
        //The bxl instruction (opcode 1) calculates the bitwise XOR of register B and the instruction's literal operand, then stores the result in register B.
        let result = comp.B ^^^ operand

        execute { comp with B = result; InstructionPointer = comp.InstructionPointer + 2 } acc

    | 2 ->
        // The bst instruction (opcode 2) calculates the value of its combo operand modulo 8 (thereby keeping only its lowest 3 bits), then writes that value to the B register.
        
        execute { comp with B = (comboOperand operand comp) % 8L; InstructionPointer = comp.InstructionPointer + 2 } acc


    | 3 ->
        // The jnz instruction (opcode 3) does nothing if the A register is 0. However, if the A register is not zero, it jumps by setting the instruction pointer to the value of its literal operand; if this instruction jumps, the instruction pointer is not increased by 2 after this instruction.

        if comp.A = 0 then
            execute { comp with InstructionPointer = comp.InstructionPointer + 2 } acc
        else    
            execute { comp with InstructionPointer = operand } acc

    | 4 ->
        // The bxc instruction (opcode 4) calculates the bitwise XOR of register B and register C, then stores the result in register B. (For legacy reasons, this instruction reads an operand but ignores it.)

        execute { comp with B = comp.B ^^^ comp.C; InstructionPointer = comp.InstructionPointer + 2 } acc

    | 5 ->
        // The out instruction (opcode 5) calculates the value of its combo operand modulo 8, then outputs that value. (If a program outputs multiple values, they are separated by commas.)
        
        execute { comp with InstructionPointer = comp.InstructionPointer + 2 } (( int ((comboOperand operand comp) % 8L))::acc) 

    | 6 ->
        // The bdv instruction (opcode 6) works exactly like the adv instruction except that the result is stored in the B register. (The numerator is still read from the A register.)
        let numerator = comp.A
        let denominator = 2.**(float (comboOperand operand comp))
        let result = (float numerator)/(float denominator) |> floor |> int64

        execute { comp with B = result; InstructionPointer = comp.InstructionPointer + 2} acc        

    | 7 -> 
        // The cdv instruction (opcode 7) works exactly like the adv instruction except that the result is stored in the C register. (The numerator is still read from the A register.)        
        let numerator = comp.A
        let denominator = 2.**(float (comboOperand operand comp))
        let result = (float numerator)/(float denominator) |> floor |> int64

        execute { comp with C = result; InstructionPointer = comp.InstructionPointer + 2} acc        


let part1 = 
    execute comp []
    |> List.map string
    |> String.concat ","


// part 2


let rec findQuine a idx =
    if execute { comp with A = a } [] = comp.Program then
        [ Some(a) ]
    else
        if idx >= comp.Program.Length then
            [ None ]
        else 
            [ for i in 0L..7L do
                let result = execute {comp with A = a*8L + i} []
                if result = comp.Program[comp.Program.Length - idx - 1 ..] then 
                    yield findQuine (8L * a + i) (idx + 1) ]
            |> List.concat
            |> List.filter (fun x -> x.IsSome)


findQuine 0L 0                
