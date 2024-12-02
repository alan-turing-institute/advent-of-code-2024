###
test_input = "test.txt"
input = "input.txt"
test_filename = joinpath(@__DIR__, test_input)
filename = joinpath(@__DIR__, input)
####
using DelimitedFiles
using Test

function read_day(filename)::Matrix{Int}
    # columns separated by whitespace, lines by \n
    return DelimitedFiles.readdlm(filename, Int)
end

function part_one(data::Matrix{Int})::Int
    sorted = sort(data, dims=1)
    # sum of the distances (absolute difference)
    result = sum(abs.(sorted[:, 1] - sorted[:, 2]))
    return result
end

function part_two(data::Matrix{Int})::Int
    return sum(map(i -> i * count(j -> j == i, data[:, 2]), data[:, 1]))
end

test_input = read_day(test_filename)
# test part one
@test part_one(test_input) == 11
# test part two
@test part_two(test_input) == 31

input = read_day(filename)
println("part one: ", part_one(input))
println("part two: ", part_two(input))