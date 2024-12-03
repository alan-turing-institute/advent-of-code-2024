let filename = "input.txt"

let readLines file =
  let contents = In_channel.with_open_bin file In_channel.input_all in
  String.split_on_char '\n' contents
  |> List.map (String.split_on_char ' ')
  |> List.map (List.map int_of_string)

(* Part 1*)
let rec isIncreasing report =
  match report with
  | x :: y :: t -> if (x > y) && (x - y <= 3) then isIncreasing (y :: t) else false
  | _ -> true

let isDecreasing report = isIncreasing (List.rev report)

let isSafe report = if isIncreasing report || isDecreasing report then 1 else 0

(* Part 2 *)
let rec _isSafeWithDampner report acc =
  match report with
  | [] -> 0
  | h :: t -> if (isSafe (List.rev_append acc t)) == 1 then 1 else
    _isSafeWithDampner t (h :: acc)

let isSafeWithDampner report =
  if (isSafe report) == 1 then 1
  else _isSafeWithDampner report []

(* Run *)
let () =
  let input = readLines filename in
  let () = print_int (List.fold_left (+) 0 (List.map isSafe input)) in
  let () = print_newline () in
  let () = print_int (List.fold_left (+) 0 (List.map isSafeWithDampner input)) in
  print_newline ()
