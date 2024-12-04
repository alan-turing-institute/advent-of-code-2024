# a bit like python written in julia today
###
test_input = "test.txt"
input = "input.txt"
test_filename = joinpath(@__DIR__, test_input)
filename = joinpath(@__DIR__, input)
####
using Test

function read_day(filename)::Vector{Vector{Char}}
    # lines of chars
    return collect.(readlines(filename))
end


function will_end_oob(start::Int, ax_direction::Int, sq_size::Int, steps::Int)::Bool
    end_ind = start + ax_direction * steps
    return end_ind < 1 || end_ind > sq_size
end

function check_direction(row::Int, col::Int, dir::Tuple{Int,Int}, subword::AbstractString, sq::Vector{Vector{Char}})::Bool
    i, j = row, col # copy
    sq_size = length(sq)
    l = length(subword)
    if will_end_oob(i, dir[1], sq_size, l) || will_end_oob(j, dir[2], sq_size, l)
        return false
    end
    for c in subword
        i += dir[1]
        j += dir[2]
        if sq[i][j] != c
            return false
        end
    end
    return true
end



function part_one(sq::Vector{Vector{Char}})::Int
    word = "XMAS"
    # ensure square
    @assert (sq_size = length(sq)) == length(sq[1])

    directions = [
        (0, 1), # down
        (1, 0), # right
        (0, -1), # up
        (-1, 0), # left
        (1, 1), # down right
        (-1, 1), # down left
        (1, -1), # up right
        (-1, -1) # up left
    ]
    count = 0

    for row in 1:sq_size
        for col in 1:sq_size
            if sq[row][col] == word[1]
                subword = word[2:end]
                for dir in directions
                    if check_direction(row, col, dir, subword, sq)
                        count += 1
                    end
                end
            end
        end
    end
    return count

end


function check_each_side(row::Int, col::Int, dir::Tuple{Int,Int}, prev_char::Char, next_char::Char, sq::Vector{Vector{Char}})::Bool
    return sq[row-dir[1]][col-dir[2]] == prev_char && sq[row+dir[1]][col+dir[2]] == next_char
end

function part_two(sq::Vector{Vector{Char}})::Int
    # word: "MAS"
    centre_char = 'A'
    prev_char = 'M'
    next_char = 'S'
    # ensure square
    @assert (sq_size = length(sq)) == length(sq[1])

    directions = [
        (1, 1), # down right
        (1, -1), # down left
        (-1, 1), # up right
        (-1, -1) # up left
    ]

    count = 0

    for row in 2:sq_size-1 # start and end offset to allow X
        for col in 2:sq_size-1
            if sq[row][col] == centre_char
                dir_count = 0
                for direction in directions
                    if check_each_side(row, col, direction, prev_char, next_char, sq)
                        dir_count += 1
                    end
                    if dir_count == 2
                        count += 1
                        break # no need to check final dir
                    end
                end

            end
        end
    end
    return count

end

test_input = read_day(test_filename)
# test part one
@test part_one(test_input) == 18
# test part two
@test part_two(test_input) == 9

input = read_day(filename)
println("part one: ", part_one(input))
println("part two: ", part_two(input))