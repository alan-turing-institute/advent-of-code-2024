open System.IO

let input = 
//     "kh-tc
// qp-kh
// de-cg
// ka-co
// yn-aq
// qp-ub
// cg-tb
// vc-aq
// tb-ka
// wh-tc
// yn-cg
// kh-ub
// ta-co
// de-co
// tc-td
// tb-wq
// wh-td
// ta-ka
// td-qp
// aq-cg
// wq-ub
// ub-vc
// de-ta
// wq-aq
// wq-vc
// wh-yn
// ka-de
// kh-ta
// co-tc
// wh-qp
// tb-vc
// td-yn".Split "\n"
    File.ReadAllLines "day-23/fsharp_evelinag/input.txt"

// find groups of 3 computers connected together

let edges = 
    input
    |> Array.map (fun line -> 
        let es = line.Split "-" 
        es.[0], es.[1])
    |> Set

let computers = 
    input
    |> Array.collect (fun line -> line.Split "-")
    |> Array.distinct

let isEdge x1 x2 = edges.Contains (x1,x2) || edges.Contains (x2,x1)

let group3 = 
    [|
        for i in 0..computers.Length-1 do
            for j in i+1..computers.Length-1 do
                for k in j+1..computers.Length-1 do
                    if isEdge computers.[i] computers.[j] 
                        && isEdge computers.[i] computers.[k]
                        && isEdge computers.[j] computers.[k] then 
                            yield [| computers.[i]; computers.[j]; computers.[k] |]
    |]



let part1 = 
    group3
    |> Array.filter (fun xs -> 
        xs |> Array.filter (fun x -> x.StartsWith "t")
        |> Array.length |> fun l -> l > 0)
    |> Array.length


// find the largest clique in the graph
let neighbours v = 
    computers
    |> Array.filter (fun c -> isEdge v c)
    |> Set

let rec bronKerbosch (r: string list) (p: string list) (x: string list) : seq<string list> =
    seq {
        // Base case: if P and X are both empty, we have a maximal clique
        if List.isEmpty p && List.isEmpty x then
            yield r
        else
            // Otherwise, try each vertex v in P
            match p with
            | [] -> ()
            | v :: rest ->
                let nv = neighbours v  

                // Restrict P and X to the neighbors of v
                let p' = List.filter (fun u -> nv.Contains u) p
                let x' = List.filter (fun u -> nv.Contains u) x

                // Recurse with R + v
                yield! bronKerbosch (v :: r) p' x'

                // Remove v from P and add it to X, then continue
                yield! bronKerbosch r rest (v :: x)
    }

let largestClique =
    bronKerbosch [] (computers |> Array.toList) []
    |> Seq.maxBy List.length

let part2 = 
    largestClique
    |> List.sort
    |> String.concat ","
