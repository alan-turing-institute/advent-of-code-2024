open! Lib

let files_of_list ls =
  let file_len_space_len_ls =
    match Pair.pairs_of_list_r ls with
    | files, None -> files
    | files, Some file -> (file, 0) :: List.rev files |> List.rev
  in
  file_len_space_len_ls
  |> List.mapi @@ fun file_id (file_len, space_len) ->
     (file_id, file_len, space_len)

let list_of_ids n id = List.init n (fun _ -> id)

let take_file_chunks n ls =
  let rec aux acc n ls =
    match ls with
    | (id, file_len, space_len) :: rest ->
        if n < file_len then
          let new_ids = list_of_ids n id in
          let all_ids = acc @ new_ids in
          (all_ids, (id, file_len - n, space_len) :: rest)
        else if n == file_len then
          let new_ids = list_of_ids n id in
          let all_ids = acc @ new_ids in
          (all_ids, rest)
        else
          let new_ids = list_of_ids file_len id in
          aux (acc @ new_ids) (n - file_len) rest
    | [] -> failwith "no file chunks left"
  in
  aux [] n ls

let disk_len files =
  List.fold_left (fun acc (_id, f_len, _s_len) -> acc + f_len) 0 files

let expanded files =
  let disk_len = disk_len files in
  let tail_files = List.rev files in
  let f_ids, _ =
    List.fold_left
      (fun (acc, tail_files) (id, f_len, s_len) ->
        if List.length acc >= disk_len then (acc, tail_files)
        else
          let own_file = list_of_ids f_len id in
          let inserted_files, tail_files' = take_file_chunks s_len tail_files in
          (acc @ own_file @ inserted_files, tail_files'))
      ([], tail_files) files
  in
  List.filteri (fun i _ -> i < disk_len) f_ids

let checksum f_ids =
  List.mapi (fun i f_id -> (i, f_id)) f_ids
  |> List.fold_left (fun acc (i, f_id) -> acc + (i * f_id)) 0

let compact () =
  let x =
    Core.In_channel.read_all "./puzzles/day9.txt"
    |> String.to_seq |> List.of_seq
    |> List.map @@ String.make 1
  in
  x |> List.map @@ int_of_string_opt |> List.filter_map Fun.id

let () =
  let compact = compact () in
  files_of_list compact |> expanded |> checksum |> Printf.printf "part 1: %i\n"

let gap_after (_id, _f_len, s_len) = s_len
let remove_gap (id, f_len, _s_len) = (id, f_len, 0)
let remove_file (id, f_len, s_len) = (id, 0, f_len + s_len)
let update_gap (id, f_len, _s_len) new_gap = (id, f_len, new_gap)
let size (_id, f_len, _s_len) = f_len

let try_move files (to_move : int * int * int) =
  let rec aux unchanged files_with_gaps =
    match files_with_gaps with
    | [] -> (List.rev unchanged, to_move)
    | file_with_gap :: rest_files ->
        if size to_move <= gap_after file_with_gap then
          let before_move = List.rev unchanged in
          let file_with_gap' = remove_gap file_with_gap in
          let to_move' =
            update_gap to_move (gap_after file_with_gap - size to_move)
          in
          let empty_slot = remove_file to_move in
          (before_move @ [ file_with_gap'; to_move' ] @ rest_files, empty_slot)
        else aux (file_with_gap :: unchanged) rest_files
  in
  aux [] files

(* Try to move each file once, in decending order of file ID. *)
let reorder files =
  let rec aux unmovable files =
    let desc = List.rev files in
    match desc with
    | [] -> unmovable
    | to_move :: rest_desc ->
        let rest_files = List.rev rest_desc in
        let files, mover = try_move rest_files to_move in
        aux (mover :: unmovable) files
  in
  aux [] files

let expand_zeros files =
  List.fold_left
    (fun acc (id, f_len, s_len) ->
      acc @ list_of_ids f_len id @ list_of_ids s_len 0)
    [] files

let () =
  let compact = compact () in
  files_of_list compact |> reorder |> expand_zeros |> checksum
  |> Printf.printf "part 2: %i\n"
