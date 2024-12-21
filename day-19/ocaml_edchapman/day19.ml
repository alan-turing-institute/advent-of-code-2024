open Lib

let first_towel_options ~towels stripes =
  towels |> List.filter (fun towel -> String.starts_with ~prefix:towel stripes)

let rec num_ways ~cache ~towels stripes =
  if stripes = "" then 1
  else
    match Hashtbl.find_opt cache stripes with
    | Some num_ways -> num_ways
    | None ->
        let num_ways =
          first_towel_options ~towels stripes
          |> List.map (fun first_towel ->
                 Core.String.drop_prefix stripes (String.length first_towel)
                 |> num_ways ~cache ~towels)
          |> List.fold_left ( + ) 0
        in
        Hashtbl.add cache stripes num_ways;
        num_ways

let parse_towels () =
  let towels, stripes =
    Core.In_channel.read_all "./puzzles/day19.txt"
    |> Str.(split @@ regexp_string "\n\n")
    |> Pair.head_pair_of_list
  in
  let towels = towels |> Str.(split @@ regexp_string ", ") in
  let stripes_ls = stripes |> Str.(split @@ regexp_string "\n") in
  (towels, stripes_ls)

let () =
  let towels, stripes_ls = parse_towels () in
  let cache = Hashtbl.create 1000 in
  let num_ways = stripes_ls |> List.map (num_ways ~cache ~towels) in
  (* Part 1. *)
  num_ways
  |> List.filter (fun n -> n > 0)
  |> List.length
  |> Printf.printf "part 1: %i\n";
  (* Part 2. *)
  num_ways |> List.fold_left ( + ) 0 |> Printf.printf "part 2: %i\n"
