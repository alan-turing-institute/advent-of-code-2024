let extract_number s =
  Str.string_after s (Str.search_forward (Str.regexp "[0-9]") s 0) |> float_of_string

let equations = In_channel.with_open_bin "input.txt" In_channel.input_all
  |> Str.split (Str.regexp "\n\n")
  |> List.map (fun ele ->
    String.split_on_char '\n' ele
    |> List.map (fun subele -> Str.split (Str.regexp ", ") subele
                |> List.map extract_number |> Array.of_list))

let det a b c d =
  a *. d -. c *. b

(*Cramer's rule*)
let solve eq offset =
  match eq with
  | a :: b :: out :: []  ->
      let d = det a.(0) a.(1) b.(0) b.(1) in
      let x = out.(0) +. offset in
      let y = out.(1) +. offset in
      (det x y b.(0) b.(1)) /. d, (det a.(0) a.(1) x y) /. d
  | _ -> raise (Invalid_argument "Fn should be passed a list containing 3 elements")

let isInt x =
  let a, _ = modf x in
  a = 0.

let aggregate condition (a,b) =
  if isInt a && isInt b && ((a <= 100. && b <= 100.) || condition) then 3. *. a +. b
  else 0.

let countTokens equations offset condition =
  equations |> List.map (fun ele -> solve ele offset |> aggregate condition) |> List.fold_left (+.) 0.

(*Run*)
let () = countTokens equations 0. false |> int_of_float |> print_int
let () = print_newline ()
let () = countTokens equations 10000000000000. true |> int_of_float |> print_int
let () = print_newline ()
