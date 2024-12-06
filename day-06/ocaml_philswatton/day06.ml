let routeMap = In_channel.with_open_bin "input.txt" In_channel.input_all
  |> String.split_on_char '\n'
  |> List.map (fun ele -> Str.split (Str.regexp "") ele |> Array.of_list)
  |> Array.of_list 

let findStartCol routeMap row =
  let rec _findStartCol routeMap row n =
    if routeMap.(row).(n) = "^" then [|row; n|]
    else _findStartCol routeMap row (n+1) in
    _findStartCol routeMap row 0

let findStart routeMap =
  let rec _findStart grid n =
    if Array.mem "^" routeMap.(n) then findStartCol routeMap n
    else _findStart grid (n+1) in
  _findStart routeMap 0

let start = findStart routeMap
let () = routeMap.(start.(0)).(start.(1)) <- "."

(*Part 1*)
let rotate dir =
  match dir with
  | "f" -> "r"
  | "r" -> "b"
  | "b" -> "l"
  | "l" -> "f"

let increment dir =
  match dir with
  | "f" -> [|-1;0|]
  | "r" -> [|0;1|]
  | "b" -> [|1;0|]
  | "l" -> [|0;-1|]

let arrSetAppend arr ele =
  if Array.mem ele arr then arr
  else Array.append arr [|ele|]

let walk routeMap start =
  let rec _walk routeMap row col direction acc =
    if row = 0 || row = ((Array.length routeMap) - 1) then acc
    else if col = 0 || col = ((Array.length routeMap.(0)) - 1) then acc
    else let inc = increment direction in
    let next = routeMap.(row + inc.(0)).(col + inc.(1)) in
    match next with
    | "#" -> _walk routeMap row col (rotate direction) acc
    | "." -> _walk routeMap (row + inc.(0)) (col + inc.(1)) direction 
      (arrSetAppend acc [|row + inc.(0); col + inc.(1)|]) in
    _walk routeMap start.(0) start.(1) "f" [||]

let visited = walk routeMap start
let () = 
  arrSetAppend visited start (*guard does not re-visit start in my input - part 2 may not generalise to other inputs*)
  |> Array.length
  |> print_int
let () = print_newline ()

(*Part 2*)
let rec whatDoYouMeanNoMixedTypeList intList =
  match intList with
  | [] -> []
  | h :: t -> (string_of_int h) :: (whatDoYouMeanNoMixedTypeList t)

let isInLoop routeMap start =
  let rec _isInLoop routeMap row col direction acc =
    if row = 0 || row = ((Array.length routeMap) - 1) then 0
    else if col = 0 || col = ((Array.length routeMap.(0)) - 1) then 0
    else let inc = increment direction in
    let next = routeMap.(row + inc.(0)).(col + inc.(1)) in
    match next with
    | "#" -> if List.mem (direction :: (whatDoYouMeanNoMixedTypeList [row + inc.(0); col + inc.(1)])) acc then 1
      else _isInLoop routeMap row col (rotate direction) ((direction :: (whatDoYouMeanNoMixedTypeList [row + inc.(0); col + inc.(1)])) :: acc)
    | "." -> _isInLoop routeMap (row + inc.(0)) (col + inc.(1)) direction acc in
  _isInLoop routeMap start.(0) start.(1) "f" []

let deepCopy arr =
  let newArr = Array.copy arr in
  let rec _deepCopy arr newArr n =
    if n = (Array.length arr) then newArr
    else let () = newArr.(n) <- (Array.copy arr.(n)) in _deepCopy arr newArr (n+1)  in
  _deepCopy arr newArr 0

let tryNewObstacle newMap start index =
  let newMap = deepCopy routeMap in
  let () = newMap.(index.(0)).(index.(1)) <- "#" in
  isInLoop newMap start
  
let bruteForce routeMap start visited = 
  let rec _bruteForce routeMap start visited acc =
    match visited with
    | [] -> acc
    | h :: t -> _bruteForce routeMap start t (acc + (tryNewObstacle routeMap start h)) in
  _bruteForce routeMap start visited 0

let () =
  bruteForce routeMap start (Array.to_list visited)
  |> print_int
let () = print_newline ()