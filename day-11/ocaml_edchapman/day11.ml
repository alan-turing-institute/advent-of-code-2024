open! Lib

let even_digits stone =
  let n_digits = string_of_int stone |> String.length in
  if n_digits == 0 then failwith "stone must have a number"
  else n_digits mod 2 == 0

(* The result after incrementing a stone. *)
type stone_incr =
  | Single of int
  | Double of (int * int)

let split stone_num =
  let chars = string_of_int stone_num |> String.to_seq in
  let n_digits = Seq.length chars in
  let stones =
    [ Seq.take (n_digits / 2) chars; Seq.drop (n_digits / 2) chars ]
    |> List.map @@ String.of_seq
    |> List.map (fun i -> int_of_string i)
    |> Pair.head_pair_of_list
  in
  Double stones

(* A condition is a tuple of: a function to test if the condition is relevant, and an update function to be applied if it is. *)
type condition = (int -> bool) * (int -> stone_incr)

let conditions : condition list =
  [
    ((fun stone -> stone == 0), fun _stone -> Single 1);
    (even_digits, split);
    ((fun _stone -> true), fun stone -> Single (stone * 2024));
  ]

(* Increments a stone_num once, returning a [stone_incr], which is either a single stone number or a pair. *)
let rec update u_cache conditions stone_num : stone_incr =
  (* Partially apply the cache to the function. *)
  let update = update u_cache in
  match Hashtbl.find_opt u_cache stone_num with
  | Some stone_incr -> stone_incr
  | None ->
      let stone_incr =
        match conditions with
        | (applies_to, update_fn) :: other_conds ->
            if applies_to stone_num then update_fn stone_num
            else update other_conds stone_num
        | [] -> failwith "unreachable, final condition must apply"
      in
      Hashtbl.add u_cache stone_num stone_incr;
      stone_incr

let rec expansion u_cache e_cache stone_num depth =
  (* Partially apply the caches to the functions. *)
  let update = update u_cache in
  let expansion = expansion u_cache e_cache in
  if depth == 0 then 1
  else
    match Hashtbl.find_opt e_cache (stone_num, depth) with
    | Some expanded -> expanded
    | None ->
        (* Take conditions from module namespace, they are const. *)
        let expanded =
          match update conditions stone_num with
          | Single a -> expansion a (depth - 1)
          | Double (a, b) -> expansion a (depth - 1) + expansion b (depth - 1)
        in
        Hashtbl.add e_cache (stone_num, depth) expanded;
        expanded

let puzz = [ 5910927; 0; 1; 47; 261223; 94788; 545; 7771 ]

let run steps puzz =
  let u_cache = Hashtbl.create 1000 in
  let e_cache = Hashtbl.create 1000 in
  let expansion = expansion u_cache e_cache in
  puzz |> List.fold_left (fun acc stone -> expansion stone steps + acc) 0

let () = run 25 puzz |> Printf.printf "\npart 1: %i"
let () = run 75 puzz |> Printf.printf "\npart 2: %i"
