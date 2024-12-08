open! Lib

let branch all_ops leaf operand = List.map (fun op -> op leaf operand) all_ops

type equation = {
  test : int;
  seq : int list;
}

let int_seq_of_str s =
  s |> Parsing.SString.ws_split |> List.map @@ int_of_string

let equation_of_line ln =
  match String.split_on_char ':' ln with
  | [] -> failwith "unreachable"
  | hd :: tl ->
      (* Assume only one colon. *)
      let seq = List.hd tl in
      { test = int_of_string hd; seq = int_seq_of_str seq }

let poss_solutions test solutions =
  List.filter_map (fun sol -> if sol <= test then Some sol else None) solutions

let exists_valid test solutions =
  if List.exists (fun sol -> sol == test) solutions then true else false

type validity =
  | True of int
  | False

let equation_ok all_ops eq =
  (* Maintain an acc of values < eq.test. These values may become solutions. *)
  let rec valid poss_acc seq =
    match seq with
    | [] -> if exists_valid eq.test poss_acc then True eq.test else False
    | operand :: tl ->
        let results =
          List.map (fun poss -> branch all_ops poss operand) poss_acc
          |> List.concat
        in
        let solutions = poss_solutions eq.test results in
        valid solutions tl
  in
  match eq.seq with
  | [] -> failwith "empty seq"
  | hd :: tl -> valid [ hd ] tl

let parse_equations () =
  let lns = Parsing.Text.seq_of_lns "./puzzles/day7.txt" in
  lns |> Seq.map @@ equation_of_line |> List.of_seq

let sum_validities vs =
  List.fold_left
    (fun acc validity ->
      match validity with
      | True t -> acc + t
      | False -> acc)
    0 vs

(* Part 1. *)
let () =
  let eqs = parse_equations () in
  let ops = [ ( + ); ( * ) ] in
  let equation_ok = equation_ok ops in
  eqs |> List.map @@ equation_ok |> sum_validities |> Printf.printf "part 1: %i"

(* New operator. *)
let ( ^^ ) a b = string_of_int a ^ string_of_int b |> int_of_string

(* Part 2. *)
let () =
  let eqs = parse_equations () in
  let ops = [ ( + ); ( * ); ( ^^ ) ] in
  let equation_ok = equation_ok ops in
  eqs |> List.map @@ equation_ok |> sum_validities |> Printf.printf "part 2: %i"
