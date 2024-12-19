open Lib

module Stripes = struct
  type t = char Seq.t

  let compare a b = String.compare (String.of_seq a) (String.of_seq b)
  let equal a b = compare a b = 0
  let hash a = String.of_seq a |> Hashtbl.hash
end

module TSet = Set.Make (Stripes)
module Cache = Hashtbl.Make (Stripes)

let valid_splits ~max_len ~towels stripes =
  (* break a towel off the start of the sequence of stripes, do this for all possible towel lengths *)
  List.init
    (min max_len (Seq.length stripes))
    (fun i ->
      let towel_len = i + 1 in
      (Seq.take towel_len stripes, Seq.drop towel_len stripes))
  (* filter for the towel existing in the available towels *)
  |> List.filter (fun (towel, _rest) ->
         TSet.find_opt towel towels |> Option.is_some)

let rec possible ~cache ~max_len ~towels stripes =
  if Seq.length stripes = 0 then true
  else
    match Cache.find_opt cache stripes with
    | Some is_possible -> is_possible
    | None ->
        let is_possible =
          valid_splits ~max_len ~towels stripes
          (* out of these options find the first where the remaining strip sequence is possible *)
          |> List.exists (fun (_towel, rest) ->
                 possible ~cache ~max_len ~towels rest)
        in
        Cache.add cache stripes is_possible;
        is_possible

let parse_towels () =
  let towels =
    Core.In_channel.read_all "./puzzles/day19.txt.towels"
    |> Core.String.strip |> String.split_on_char ','
    |> List.map Core.String.strip |> List.map String.to_seq |> TSet.of_list
  in
  let stripes_ls =
    Parsing.Text.seq_of_lns "./puzzles/day19.txt.stripes"
    |> List.of_seq |> List.map String.to_seq
  in
  (towels, stripes_ls)

let longest_towel towels =
  TSet.fold
    (fun towel acc ->
      let towel_len = Seq.length towel in
      if towel_len > acc then towel_len else acc)
    towels 1

(* Part 1. *)
let () =
  let towels, stripes_ls = parse_towels () in
  let max_len = longest_towel towels in
  let cache = Cache.create 1000 in
  stripes_ls
  |> List.filter (fun stripes -> possible ~cache ~max_len ~towels stripes)
  |> List.length
  |> Printf.printf "part 1: %i\n"

let rec all ~cache ~max_len ~towels stripes =
  if Seq.length stripes = 0 then 1
  else
    match Cache.find_opt cache stripes with
    | Some is_possible -> is_possible
    | None ->
        let filtered = valid_splits ~max_len ~towels stripes in
        let all =
          filtered
          |> List.map (fun (_towel, rest) -> all ~cache ~max_len ~towels rest)
          |> List.fold_left ( + ) 0
        in
        Cache.add cache stripes all;
        all

(* Part 2. *)
let () =
  let towels, stripes_ls = parse_towels () in
  let max_len = longest_towel towels in
  let pos_cache = Cache.create 1000 in
  let all_cache = Cache.create 1000 in
  let num_orders =
    stripes_ls
    |> List.filter (fun stripes ->
           possible ~cache:pos_cache ~max_len ~towels stripes)
    |> List.map (fun stripes -> all ~cache:all_cache ~max_len ~towels stripes)
  in
  num_orders |> List.fold_left ( + ) 0 |> Printf.printf "part 2: %i\n"
