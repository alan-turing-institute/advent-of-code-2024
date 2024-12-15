open Lib

(* Part 1 object type. *)
type obj = {
  loc : Grid.loc;
  char : char;
}

let parse () =
  let grid =
    Parsing.Text.seq_of_lns "./puzzles/day15.txt.grid"
    |> List.of_seq
    |> List.map (fun ln -> String.to_seq ln |> List.of_seq)
    |> Grid.of_lss
  in
  let moves =
    Core.In_channel.read_all "./puzzles/day15.txt.moves"
    |> String.split_on_char '\n' |> List.fold_left ( ^ ) "" |> String.to_seq
    |> List.of_seq
    |> List.map (fun c ->
           let open Grid in
           match c with
           | '^' -> Up
           | 'v' -> Down
           | '>' -> Right
           | '<' -> Left
           | e ->
               print_char e;
               failwith "unreachable")
  in
  (grid, moves)

let shift ~grid dir objs =
  let shifted =
    objs |> List.map (fun obj -> { obj with loc = Grid.move obj.loc dir })
  in
  let robot_before_shift = (List.hd (List.rev objs)).loc in
  let to_write = { loc = robot_before_shift; char = '.' } :: shifted in
  to_write
  |> List.fold_left (fun grid obj -> Grid.overwrite grid obj.loc obj.char) grid

let rec try_shift ~grid dir (objs : obj list) =
  let leading_obj_loc = (List.hd objs).loc in
  let infront = Grid.move leading_obj_loc dir in
  match Grid.at grid infront with
  | '#' -> grid
  | 'O' -> try_shift ~grid dir ({ loc = infront; char = 'O' } :: objs)
  | '.' -> shift ~grid dir objs
  | _ -> failwith "unreachable"

let print_grid grid =
  grid |> Grid.to_lss
  |> List.iter (fun row -> row |> List.to_seq |> String.of_seq |> print_endline);
  flush stdout

let gps (x, y) = (100 * y) + x
let boxes grid = Grid.all_locations 'O' grid
let score grid = boxes grid |> List.map gps |> List.fold_left ( + ) 0

(* For part 2. *)
let boxes' grid = Grid.all_locations '[' grid
let score' grid = boxes' grid |> List.map gps |> List.fold_left ( + ) 0

(* Part 1. *)
let () =
  let grid, moves = parse () in
  moves
  |> List.fold_left
       (fun grid move ->
         let robot_loc = Grid.all_locations '@' grid |> List.hd in
         try_shift ~grid move [ { loc = robot_loc; char = '@' } ])
       grid
  |> score
  |> Printf.printf "part 1: %i\n"

let expand_row row =
  List.map
    (fun el ->
      if el = '@' then [ '@'; '.' ]
      else if el = 'O' then [ '['; ']' ]
      else [ el; el ])
    row
  |> List.concat

let expand grid = Grid.to_lss grid |> List.map expand_row |> Grid.of_lss

(* Object type for part 2. *)
type obj' =
  | Robot of Grid.loc
  | Box of (Grid.loc * Grid.loc)

let locs_of_obj' = function
  | Robot loc -> [ loc ]
  | Box (l, r) -> [ l; r ]

let all_locs objs = objs |> List.map locs_of_obj' |> List.concat

let combine a b =
  if Option.is_none a || Option.is_none b then None
  else Some (List.append (Option.get a) (Option.get b))

(* Return [Some objs] where [objs] is a list of objects to be shifted, or [None] if any of the affected objects get blocked and no shift will occur. *)
let rec affected_objs ~grid dir (cur : obj') : obj' list option =
  let affected_of_loc loc =
    let infront_loc = Grid.move loc dir in
    let infront_char = infront_loc |> Grid.at grid in
    match infront_char with
    | '#' -> None
    | '[' ->
        let box = Box (infront_loc, Grid.move infront_loc Right) in
        affected_objs ~grid dir box
        |> Option.map (fun affected -> cur :: affected)
    | ']' ->
        let box = Box (Grid.move infront_loc Left, infront_loc) in
        affected_objs ~grid dir box
        |> Option.map (fun affected -> cur :: affected)
    | '.' -> Some [ cur ]
    | _ -> failwith "unreachable"
  in
  match cur with
  | Robot loc -> affected_of_loc loc
  | Box (lloc, rloc) -> (
      match dir with
      | Up | Down -> combine (affected_of_loc lloc) (affected_of_loc rloc)
      | Left -> affected_of_loc lloc
      | Right -> affected_of_loc rloc)

(* Shift function for part 2. *)
let shift' ~grid dir (objs : obj' list) =
  let shifted =
    objs
    |> List.map (fun obj ->
           match obj with
           | Robot loc -> Robot (Grid.move loc dir)
           | Box locs -> Box (Pair.map (fun loc -> Grid.move loc dir) locs))
  in
  let grid_with_shifted =
    shifted
    |> List.fold_left
         (fun grid obj ->
           match obj with
           | Robot loc -> Grid.overwrite grid loc '@'
           | Box (lloc, rloc) ->
               let grid = Grid.overwrite grid lloc '[' in
               Grid.overwrite grid rloc ']')
         grid
  in
  (* Write '.' to the locations that have become empty and have not become occupied by shifted objects. *)
  let to_write_empty =
    all_locs objs
    |> List.filter (fun empty_loc ->
           (* if empty_loc has been written to as a shifted position, return false *)
           all_locs shifted
           |> List.exists (fun shifted -> Grid.eq shifted empty_loc)
           |> Bool.not)
  in
  to_write_empty
  |> List.fold_left
       (fun grid loc -> Grid.overwrite grid loc '.')
       grid_with_shifted

(* Part 2. *)
let () =
  let grid, moves = parse () in
  let grid = expand grid in
  let final_grid =
    moves
    |> List.fold_left
         (fun grid move ->
           let robot_loc = Grid.all_locations '@' grid |> List.hd in
           (* Returns [Some objs] or [None] if at least one of the objects gets blocked by a wall. *)
           affected_objs ~grid move (Robot robot_loc)
           (* Shift the objects, returning a new grid. *)
           |> Option.map (shift' ~grid move)
           (* Return the new grid, or the old grid as default if the shifting object were blocked by a wall. *)
           |> Option.value ~default:grid)
         grid
  in
  final_grid |> print_grid;
  final_grid |> score' |> Printf.printf "part 2: %i\n"
