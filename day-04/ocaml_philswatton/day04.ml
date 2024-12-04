let filename = "input.txt"

let readLines file =
  let contents = In_channel.with_open_bin file In_channel.input_all in
  String.split_on_char '\n' contents
  |> List.map (Str.split (Str.regexp ""))

let reverse input = List.rev (List.map List.rev input)

let makeGrid input =
  input
  |> List.map Array.of_list
  |> Array.of_list 


(* Part 1*)
let xmas = [|"X"; "M"; "A"; "S"|]

let identity value = value
let increment value = value + 1
let decrement value = value - 1

let rec wordCheck grid row col inc_row inc_col acc word =
  if row >= (Array.length grid) then 0
  else if col >= (Array.length grid.(row)) then 0
  else if row < 0 then 0
  else if col < 0 then 0
  else if grid.(row).(col) = word.(acc)
    then if acc = ((Array.length word) - 1) then 1
    else wordCheck grid (inc_row row) (inc_col col) inc_row inc_col (increment acc) word
  else 0

let wordSearch input =
  let rec search grid row col acc =
    if (row = (Array.length grid)) then acc
    else if (col = (Array.length grid.(0))) then search grid (increment row) 0 acc
    else if grid.(row).(col) = xmas.(0) then
      search grid row (increment col) (acc + 
      (wordCheck grid row col increment identity 0 xmas) + 
      (wordCheck grid row col identity increment 0 xmas) + 
      (wordCheck grid row col increment increment 0 xmas) + 
      (wordCheck grid row col increment decrement 0 xmas))
    else search grid row (increment col) acc in
  (search (makeGrid input) 0 0 0) + (search (makeGrid (reverse input)) 0 0 0)


(* Part 2 *)
let mas = [|"M"; "A"; "S"|]
let sam = [|"S"; "A"; "M"|]

let xCheck grid row col =
  if (wordCheck grid row col increment increment 0 mas) = 1 then
    if (wordCheck grid (row + 2) col decrement increment 0 mas) = 1 then 1
    else if (wordCheck grid (row + 2) col decrement increment 0 sam) = 1 then 1
    else 0
  else 0

let xWordSearch input =
  let rec xSearch grid row col acc =
    if (row = (Array.length grid)) then acc
    else if (col = (Array.length grid.(0))) then xSearch grid (increment row) 0 acc
    else if grid.(row).(col) = mas.(0) then
      xSearch grid row (increment col) (acc + (xCheck grid row col))
    else xSearch grid row (increment col) acc in
    (xSearch (makeGrid input) 0 0 0) + (xSearch (makeGrid (reverse input)) 0 0 0)


(* Run *)
let () =
  let input = readLines filename in
  let () = print_int (wordSearch input) in
  let () = print_newline () in
  let () = print_int (xWordSearch input) in
  print_newline ()
