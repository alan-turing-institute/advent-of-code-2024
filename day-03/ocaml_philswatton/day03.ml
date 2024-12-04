open Re

let memory = In_channel.with_open_bin "input.txt" In_channel.input_all

(* Part 1 *)
let digitReg = rep1 digit
let digitRegex = compile digitReg
let opReg = seq [(str "mul("); digitReg; (str ","); digitReg; (str ")")]
let opRegex = compile opReg
let operations = matches opRegex memory

let mul operation =
  matches digitRegex operation
  |> List.map int_of_string
  |> List.fold_left ( * ) 1

let () =
  List.map mul operations
  |> List.fold_left ( + ) 0
  |> print_int
let () = print_newline ()

(* Part 2*)
let doReg = str "do()"
let dontReg = str "don't()"
let fullOpRegex = compile (alt [opReg; doReg; dontReg])
let allOperations = matches fullOpRegex memory

let rec conditionalComputeMuls operations acc condition =
  match operations with
  | [] -> acc
  | h :: t -> if h = "do()" then conditionalComputeMuls t acc true
  else if h = "don't()" then conditionalComputeMuls t acc false
  else if condition then conditionalComputeMuls t (acc + (mul h)) condition
  else conditionalComputeMuls t acc condition

let () =
  conditionalComputeMuls allOperations 0 true
  |> print_int
let () = print_newline ()