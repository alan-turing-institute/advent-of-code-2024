let input = In_channel.with_open_bin "input.txt" In_channel.input_all
  |> Str.split (Str.regexp "\n\n")

(*x|y -> if y, x must be _before_, not _after y*)
let rules = List.nth input 0
  |> Str.split (Str.regexp "\n")
  |> List.map (Str.split (Str.regexp "|"))
  |> List.map (fun ele -> (List.nth ele 1, List.nth ele 0))

let pages = List.nth input 1
  |> Str.split (Str.regexp "\n")
  |> List.map (Str.split (Str.regexp ","))

(* Part 1*)
let ruleHash = Hashtbl.create 100000
let () = Hashtbl.add_seq ruleHash (List.to_seq rules) (*mutability: sad!*)

let isValid pageList ruleHash =
  let rec _isValid pageList ruleHash acc =
    match pageList with
    | [] -> true;
    | h :: t -> if List.mem h acc then false 
    else _isValid t ruleHash (List.append (Hashtbl.find_all ruleHash h) acc) in
  _isValid pageList ruleHash []

let getMiddleEle list =
  int_of_string (List.nth list (((List.length list) - 1) / 2))

let computeMiddle pageList ruleHash =
  if isValid pageList ruleHash then getMiddleEle pageList
  else 0

let () =
    List.map (fun ele -> computeMiddle ele ruleHash) pages
    |> List.fold_left ( + ) 0
    |> print_int
let () = print_newline ()

(*Part 2*)
(*Got lazy - slow but works*)
let rec makeValid pageList ruleHash =
  let rec _makeValid pageList ruleHash acc disallowList =
    match pageList with
    | [] -> pageList
    | h :: t -> if List.mem h disallowList then List.append (h :: acc) t
    else _makeValid t ruleHash (List.append acc [h]) (List.append (Hashtbl.find_all ruleHash h) disallowList) in
  if isValid pageList ruleHash then pageList
  else makeValid (_makeValid pageList ruleHash [] []) ruleHash

let computeInvalidMiddle pageList ruleHash =
  if isValid pageList ruleHash then 0
  else getMiddleEle (makeValid pageList ruleHash)

let () =
  List.map (fun ele -> computeInvalidMiddle ele ruleHash) pages
  |> List.fold_left ( + ) 0
  |> print_int
let () = print_newline ()
