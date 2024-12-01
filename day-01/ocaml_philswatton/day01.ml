let filename = "input.txt"

let read_lines file =
  let contents = In_channel.with_open_bin file In_channel.input_all in
  String.split_on_char '\n' contents

let split_list_element input =
  input
  |> List.map (Str.split (Str.regexp "   "))
  |> List.map (List.map int_of_string)

let rec extract_list list index =
  match list with
  | [] -> []
  | h :: t -> List.nth h index :: extract_list t index


(* Part 1 Solution *)
let abs_val value = 
  if value < 0 then -value else value

let rec sort_subtract_sum list1 list2 =
  match List.sort compare list1, List.sort compare list2 with
  | [], [] -> 0
  | [], h :: t -> raise (Invalid_argument "Lists should be same length")
  | h :: t, [] -> raise (Invalid_argument "Lists should be same length")
  | h1 :: t1, h2 :: t2 -> abs_val (h1 - h2) + sort_subtract_sum t1 t2


(* Part 2 Solution *)
let count value list =
  List.fold_left (fun acc ele -> if ele = value then acc + 1 else acc + 0) 0 list

let rec _get_sum_map uniq list =
  match uniq with
  | [] -> []
  | h :: t -> (h, count h list) :: _get_sum_map t list

let get_sum_map list1 list2 =
  let uniq = List.sort_uniq compare list1 in
  _get_sum_map uniq list2

let rec lookup key dict =
  match dict with
  | [] -> 0
  | (key', value) :: t -> if key = key' then value else lookup key t

let rec _lookup_multiply_sum list dict =
  match list with
  | [] -> 0
  | h :: t -> h * lookup h dict + _lookup_multiply_sum t dict

let lookup_multiply_sum list1 list2 =
  let dict = get_sum_map list1 list2 in
  _lookup_multiply_sum list1 dict


(* Run *)
let run file =
  let input = split_list_element (read_lines file) in
  let list1 = extract_list input 0 in
  let list2 = extract_list input 1 in
  let () = print_int (sort_subtract_sum list1 list2) in
  let () = print_newline () in
  let () = print_int (lookup_multiply_sum list1 list2) in
  print_newline ()

let () = run filename
