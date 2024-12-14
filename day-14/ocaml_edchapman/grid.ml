(** Assumes a zero-indexed grid where the top row is the zero-th row. *)

type 'a t = 'a list list
(** Abstraction function:
    A list of rows, the first row containing locations [(0,0)] through [(w-1,0)].

  I.e.
  [ [[ (0,0); (1,0); (2,0) ];
     [ (0,1); (1,1); (2,1) ];
     [ (0,2); (1,2); (2,2) ]] ]
  *)

type loc = int * int
type size = int * int

type dir =
  | Up
  | Right
  | Down
  | Left

let of_lss lss = lss

let size lss =
  let row = List.hd lss in
  let height = List.length lss in
  let width = List.length row in
  (width, height)

let off_grid size (x, y) =
  let maxx, maxy = Pair.map (fun el -> el - 1) size in
  x > maxx || y > maxy || x < 0 || y < 0

let on_grid size loc = Bool.not (off_grid size loc)

let wrap (w, h) (x, y) =
  let transform coord dim =
    let offset = if coord < 0 then ((abs coord / dim) + 1) * dim else 0 in
    (coord + offset) mod dim
  in
  (transform x w, transform y h)

let ( +@ ) (ax, ay) (bx, by) = (ax + bx, ay + by)
let ( -@ ) (ax, ay) (bx, by) = (ax - bx, ay - by)
let delta (ax, ay) (bx, by) = (bx - ax, by - ay)
let eq (ax, ay) (bx, by) = ax = bx && ay = by

let all_locations focus lss =
  (* map over rows *)
  List.mapi
    (fun j row ->
      (* map over row *)
      List.mapi (fun i el -> if el = focus then Some (i, j) else None) row
      |> List.filter_map Fun.id)
    lss
  |> List.concat

let fold f (acc : 'acc) (lss : 'a list list) =
  List.fold_left (fun acc row -> List.fold_left f acc row) acc lss

let mapi f lss =
  lss
  |> List.mapi (fun row_idx row ->
         row |> List.mapi (fun col_idx el -> f (col_idx, row_idx) el))

let foldi f (acc : 'acc) (lss : 'a list list) =
  lss
  |> mapi (fun loc el -> (loc, el))
  |> fold (fun acc (loc, el) -> f acc loc el) acc

let print_loc (x, y) = Printf.printf "(%i,%i)\n" x y
let at lss (x, y) = List.nth lss y |> fun row -> List.nth row x

let move (x, y) dir =
  match dir with
  | Up -> (x, y + 1)
  | Down -> (x, y - 1)
  | Right -> (x + 1, y)
  | Left -> (x - 1, y)

let move_delta ~delta:(dx, dy) (x, y) = (x + dx, y + dy)
