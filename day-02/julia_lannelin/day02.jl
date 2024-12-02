###
test_input = "test.txt"
input = "input.txt"
test_filename = joinpath(@__DIR__, test_input)
filename = joinpath(@__DIR__, input)
####

using Test

function read_day(filename)::Vector{Vector{Int64}}
    # columns separated by whitespace, lines by \n
    # varying length so can't use DelimitedFiles.readdlm
    return map(x -> map(z -> parse(Int64, z), split(x)), readlines(filename))
end

function safe_increment(a::Int64, b::Int64)::Bool
    inc = b - a
    return inc <= 3 && inc >= 1
end

function pair(x::Vector{Int64}, i::Int)::Tuple{Int64,Int64}
    return (x[i], x[i+1])
end


function is_safe(row::Vector{Int64})::Bool
    if row[1] > row[end]
        row = reverse(row)
    end
    pairs = pair.(Ref(row), 1:length(row)-1)
    # lazy eval to effectively exit early
    return reduce((result, elt) -> result && safe_increment(elt[1], elt[2]), pairs, init=true)
end


function is_safe_dampner(row::Vector{Int64}, has_popped::Bool=false)::Bool
    if is_safe(row)
        return true
    end

    # brute force through :(
    for i in 1:length(row)
        if is_safe(deleteat!(copy(row), i))
            return true
        end
    end

    return false

end

function count_valid(data::Vector{Vector{Int64}}, safe_fn::Function)::Int64
    return sum(map(safe_fn, data))
end

function part_one(data::Vector{Vector{Int64}})::Int64
    return count_valid(data, is_safe)
end

function part_two(data::Vector{Vector{Int64}})::Int64
    return count_valid(data, is_safe_dampner)
end

test_input = read_day(test_filename)
# test part one
@test part_one(test_input) == 2
# test part two
@test part_two(test_input) == 4

input = read_day(filename)
println("part one: ", part_one(input))
println("part two: ", part_two(input))