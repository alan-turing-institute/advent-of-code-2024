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

let abs_val value = 
  if value < 0 then
    -value
  else
    value

let rec sort_subtract_sum list1 list2 =
  match List.sort compare list1, List.sort compare list2 with
  | [], [] -> 0
  | [], h :: t -> raise (Invalid_argument "Lists should be same length")
  | h :: t, [] -> raise (Invalid_argument "Lists should be same length")
  | h1 :: t1, h2 :: t2 -> abs_val (h1 - h2) + sort_subtract_sum t1 t2

let run file =
  let input = split_list_element (read_lines file) in
  let list1 = extract_list input 0 in
  let list2 = extract_list input 1 in
  print_int (sort_subtract_sum list1 list2)

let () = run filename