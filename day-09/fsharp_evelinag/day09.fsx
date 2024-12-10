open System.IO

let input = 
    //"2333133121414131402" 
    File.ReadAllText("day-09/fsharp_evelinag/input.txt")
    |> Seq.toList |> List.map (string >> int)

// File system is represented as:
// start position, length, content (either None or Some(fileID))

let rec constructDisc input isFile fileId position (acc:(int*int*int option) list) = 
    match input with
    | [] -> acc |> List.rev |> Array.ofList, fileId - 1
    | segment_length::input' ->
        if isFile then
            // a file
            let acc' = (position, segment_length, Some fileId)::acc
            let nextPosition = position + segment_length
            constructDisc input' false (fileId + 1) nextPosition acc'
        else
            // empty space
            let acc' = (position, segment_length, None)::acc
            let nextPosition = position + segment_length            
            constructDisc input' true fileId nextPosition acc'

let disc, maxFileId = constructDisc input true 0 0 []

let explicitDisc disc = 
    disc
    |> Array.collect (fun (start, length, content) ->
        Array.init length (fun _ -> content))


let fullDisc = explicitDisc disc |> Array.copy
let rec fill () =
    let firstEmpty = 
        fullDisc |> Array.findIndex (fun x -> x.IsNone)            
    let lastFull = 
        fullDisc |> Array.findIndexBack (fun x -> x.IsSome)

    if firstEmpty > lastFull then
        ()
    else
        fullDisc.[firstEmpty] <- fullDisc.[lastFull]
        fullDisc.[lastFull] <- None
        fill()

fill()

let checksum disc = 
    disc 
    |> Array.mapi (fun idx content ->
        (int64 idx) * (match content with Some(x) -> int64 x | None -> int64 0))
    |> Array.sum

// part1
checksum fullDisc


let fileToMove = maxFileId
let filesystem = disc |> Array.copy

let rec moveFiles (filesystem: (int*int*int option) []) (fileToMove: int) =
    if fileToMove = 0 then
        filesystem
    else

    let fileIdx = 
        filesystem 
        |> Array.findIndex (fun (_,_,f) -> f = Some(fileToMove))
    let fileStart, fileLength, _ = filesystem.[fileIdx]

    // identify the first gap that's >= length and move the file there
    let gap =
        filesystem
        |> Array.tryFindIndex (fun (s,l,x) -> 
            s < fileStart && l >= fileLength && x.IsNone )
    
    match gap with  
    | None -> moveFiles filesystem (fileToMove - 1)
    | Some(idx) ->
        let gapStart, gapLength, _ = filesystem.[idx]
        let filesystem' = 
            Array.removeAt idx filesystem
            |> Array.removeAt (fileIdx-1)

        let filesystem'' = 
            Array.append filesystem' 
                [| yield (gapStart, fileLength, Some(fileToMove));                        
                            yield (fileStart, fileLength, None);
                            if fileLength < gapLength then 
                                yield (gapStart + fileLength, gapLength - fileLength, None)
                            |]
            |> Array.sort
        
        moveFiles filesystem'' (fileToMove - 1)

let newFilesystem = moveFiles filesystem maxFileId

explicitDisc newFilesystem |> checksum

