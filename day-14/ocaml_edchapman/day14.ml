open! Lib

type robot = {
  loc : int * int;
  vec : int * int;
}

let robot_of_group g =
  let get pos = Re.Group.get g pos |> int_of_string in
  { loc = (get 1, get 2); vec = (get 3, get 4) }

(* Expected: p=82,54 v=14,-84 *)
let parse_robots text =
  let open Re in
  let regex =
    [
      str "p=";
      group (rep digit);
      str ",";
      group (rep digit);
      str " v=";
      group (seq [ opt (str "-"); rep digit ]);
      str ",";
      group (seq [ opt (str "-"); rep digit ]);
    ]
    |> seq |> compile |> all
  in
  regex text |> List.map @@ robot_of_group

let move_robot ~n ~grid_size { loc; vec } =
  let open Grid in
  let delta = Pair.map (( * ) n) vec in
  let loc' = move_delta ~delta loc |> wrap grid_size in
  { loc = loc'; vec }

type lr =
  | Left
  | Right

type tb =
  | Top
  | Bottom

let quadrant_of ~grid_size:(w, h) robot =
  let x, y = robot.loc in
  let horiz =
    if x < w / 2 then Some Left else if x > w / 2 then Some Right else None
  in
  Option.bind horiz (fun lr ->
      if y < h / 2 then Some (lr, Top)
      else if y > h / 2 then Some (lr, Bottom)
      else None)

let score_of_quads (lt, lb, rt, rb) =
  (*Printf.printf "quads: %i,%i,%i,%i\n" lt lb rt rb;*)
  lt * lb * rt * rb

let robots () = Core.In_channel.read_all "./puzzles/day14.txt" |> parse_robots

let () =
  let grid_size = (101, 103) in
  robots ()
  |> List.map @@ move_robot ~n:100 ~grid_size
  |> List.filter_map (quadrant_of ~grid_size)
  |> List.fold_left
       (fun (lt, lb, rt, rb) q ->
         match q with
         | Left, Top -> (lt + 1, lb, rt, rb)
         | Left, Bottom -> (lt, lb + 1, rt, rb)
         | Right, Top -> (lt, lb, rt + 1, rb)
         | Right, Bottom -> (lt, lb, rt, rb + 1))
       (0, 0, 0, 0)
  |> score_of_quads
  |> Printf.printf "part 1: %i\n"

let rows_robots (robots : robot list) =
  let locs = List.map (fun { loc; _ } -> loc) robots in
  let rows = List.init 103 Fun.id in
  List.map (fun i -> List.filter (fun (x, y) -> y = i) locs) rows

let print_robots rows_robots =
  let str_of_robots_row row_of_robots =
    let cols = List.init 101 Fun.id in
    List.fold_left
      (fun acc j ->
        if List.exists (fun (x, y) -> x = j) row_of_robots then acc ^ "@"
        else acc ^ "-")
      "" cols
  in
  rows_robots |> List.map str_of_robots_row |> List.iter print_endline

let () =
  let open Unix in
  let grid_size = (101, 103) in
  let robots = robots () in
  (* Found a repeating structure at step 16,119,... *)
  let headstart = 16 in
  let robots = List.map (move_robot ~n:headstart ~grid_size) robots in
  let step = 103 in
  let rec aux n robots =
    let robots' = List.map (move_robot ~n:step ~grid_size) robots in
    let rows_bots = rows_robots robots' in
    Printf.printf "\n\nstep: %i\n" n;
    Unix.sleepf 0.3;
    print_robots rows_bots;
    aux (n + step) robots'
  in
  aux (step + headstart) robots |> Printf.printf "part 2: %i"
