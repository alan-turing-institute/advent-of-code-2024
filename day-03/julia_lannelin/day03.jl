###
test_input = "test.txt"
test2_input = "example_input.txt"
input = "input.txt"
test_filename = joinpath(@__DIR__, test_input)
test2_filename = joinpath(@__DIR__, test2_input)
filename = joinpath(@__DIR__, input)
####
using DelimitedFiles
using Test

function read_day(filename)::String
    #single string
    return read(filename, String)
end

function get_mul_sum(data::AbstractString)::Int
    re = r"mul\((\d+),(\d+)\)"

    return eachmatch(re, data) |> # find all matches
           x -> map(m -> parse(Int, m[1]) * parse(Int, m[2]), x) |> # parse each to ints
                sum
end

function part_one(data::String)::Int
    return get_mul_sum(data)
end

function part_two(data::String)::Int

    function do_mul_sum(x::AbstractString)::Int
        # extract after do and calc
        do_ind = findfirst("do()", x)
        if isnothing(do_ind)
            return 0
        end
        return get_mul_sum(x[last(do_ind):end])
    end

    # first group ok, others only after do()
    (initial, splits) = Iterators.peel(eachsplit(data, "don't()"))
    return get_mul_sum(initial) + sum(map(do_mul_sum, splits))

end

test_input = read_day(test_filename)
test2_input = read_day(test2_filename)
# test part one
@test part_one(test_input) == 161
# test part two
@test part_two(test2_input) == 48

input = read_day(filename)
println("part one: ", part_one(input))
println("part two: ", part_two(input))