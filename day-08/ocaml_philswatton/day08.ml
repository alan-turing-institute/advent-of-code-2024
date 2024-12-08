let antennaMap = In_channel.with_open_bin "input.txt" In_channel.input_all
  |> String.split_on_char '\n'
  |> List.map (fun ele -> Str.split (Str.regexp "") ele |> Array.of_list)
  |> Array.of_list

let h = Array.length antennaMap
let w = Array.length antennaMap.(0)

(*Store antenna coordinates*)
let rec _findAntennaCoords antennaMap acc i j =
  if j = w then acc
  else if not (antennaMap.(i).(j) = ".") then
    _findAntennaCoords antennaMap ((antennaMap.(i).(j), [|i; j|]) :: acc) i (j+1)
  else _findAntennaCoords antennaMap acc i (j+1)

let findAntennas antennaMap =
  let rec _findAntennas antennaMap acc i =
    if i = h then acc
    else _findAntennas antennaMap (List.append acc (_findAntennaCoords antennaMap [] i 0)) (i+1) in
  _findAntennas antennaMap [] 0

let antennaLocations = findAntennas antennaMap
let antennaHash = Hashtbl.create 100000
let () = Hashtbl.add_seq antennaHash (List.to_seq antennaLocations)

(*Store unique antennas*)
module StringSet = Set.Make(String)
let rec getFrequencies antennaLocations =
  match antennaLocations with
  | [] -> []
  | (a,b) :: t -> a :: getFrequencies t
let frequencies = getFrequencies antennaLocations |> StringSet.of_list |> StringSet.to_list

(*Fns for getting unordered combinations of a list's elements*)
let rec distribute ele l =
  match l with
  | [] -> []
  | h :: t -> (ele, h) :: distribute ele t

let rec getCombinations l =
  match l with
  | [] -> []
  | h :: t -> (distribute h t) @ getCombinations t

(*Part 1*)
let rec findAntiNodes combinations =
  match combinations with
  | [] -> []
  | (a, b) :: t ->
      let dx = a.(0) - b.(0) in
      let dy = a.(1) - b.(1) in
      [[|a.(0) + dx; a.(1) + dy|]; [|b.(0) - dx; b.(1) - dy|]] @ findAntiNodes t

let rec getAntiNodes frequencies fn =
  match frequencies with
  | [] -> []
  | h :: t ->
    (Hashtbl.find_all antennaHash h |> getCombinations |> fn) @ getAntiNodes t fn

let inGrid arr =
  if (arr.(0) < 0) || (arr.(0) >= h) || (arr.(1) < 0) || (arr.(1) >= w) then 0
  else 1

module OrderedPair = struct
  type t = int array
  let compare x y = compare (x.(0), x.(1)) (y.(0), y.(1))
end
module PairSet = Set.Make(OrderedPair)

let countNodes nodes =
  nodes |> PairSet.of_list |> PairSet.to_list |> List.map (inGrid) |> List.fold_left (+) 0

(*Part2*)
let rec generateAntiNodes x y dx dy op =
  let newAntiNode = [|op x dx; op y dy|] in
  if (inGrid newAntiNode) = 0 then []
  else newAntiNode :: generateAntiNodes newAntiNode.(0) newAntiNode.(1) dx dy op 

let rec findAntiNodesWhileTakingIntoAccountResonantHarmonics combinations =
  match combinations with
  | [] -> []
  | (a,b) :: t ->
    let dx = a.(0) - b.(0) in
    let dy = a.(1) - b.(1) in
    generateAntiNodes a.(0) a.(1) dx dy (+) @ 
    generateAntiNodes b.(0) b.(1) dx dy (-) @
    findAntiNodesWhileTakingIntoAccountResonantHarmonics t

(*Run*)
let antiNodes1 = getAntiNodes frequencies findAntiNodes
let antiNodes2 =
  (getAntiNodes frequencies findAntiNodesWhileTakingIntoAccountResonantHarmonics) @
  Hashtbl.fold (fun k v acc -> v :: acc) antennaHash []
let () = countNodes antiNodes1 |>  print_int
let () = print_newline ()
let () = countNodes antiNodes2 |>  print_int
let () = print_newline ()

