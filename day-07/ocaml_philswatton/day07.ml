let rec parseEquation equation =
  match equation with
  | h :: [] -> List.map int_of_string (String.split_on_char ' ' h)
  | h :: t -> int_of_string h :: parseEquation t

let equations = In_channel.with_open_bin "input.txt" In_channel.input_all
  |> String.split_on_char '\n'
  |> List.map (fun ele -> Str.split (Str.regexp ": ") ele |> parseEquation)

(*Part 1*)
let check equation ops =
  let rec _check equation acc output =
    match equation with
    | [] -> acc = output
    | h :: t -> if acc = 0 then _check t h output
    else List.fold_left (||) false (List.map (fun ele -> _check t (ele acc h) output) ops)  in
  _check (List.tl equation) 0 (List.nth equation 0)

let () =
  List.map (fun ele -> if check ele [( + ); ( * )] then (List.nth ele 0) else 0) equations
  |> List.fold_left ( + ) 0
  |> print_int
let () = print_newline ()

(*Part 2*)
let intConcat a b = int_of_string (String.concat "" [(string_of_int a); (string_of_int b)])

let () =
  List.map (fun ele -> if check ele [( + ); ( * ); intConcat] then (List.nth ele 0) else 0) equations
  |> List.fold_left ( + ) 0
  |> print_int
let () = print_newline ()



