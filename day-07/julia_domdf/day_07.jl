test_values = Int[]; numbers = Vector{Int}[]
for line in readlines("day_7_data.txt")
    parts = split(line, ":")
    push!(test_values, parse(Int, parts[1]))
    push!(numbers, parts[2] |> split |> nums -> parse.(Int, nums))
end

function evaluate(nums::Vector{Int}, ops::Vector{Char})
    result = nums[1]
    # sequentially evaluate operations left-to-right
    for i in 1:length(ops)
        if ops[i] == '+'
            result += nums[i+1]
        elseif ops[i] == '*'
            result *= nums[i+1]
        else  # '|' concatenation operator
            # convert both numbers to strings => concat => back to an int
            result = parse(Int, string(result) * string(nums[i+1]))
        end
    end
    return result
end

function solve_equation(test_value::Int, numbers::Vector{Int}; part2::Bool = false)
    # use only + and * for part 1, add | for part 2
    ops = part2 ? ['+', '*', '|'] : ['+', '*']
    all_ops = [[op for op in p] for p in Iterators.product(fill(ops, length(numbers) - 1)...)]

    for ops in all_ops
        if evaluate(numbers, ops) == test_value
            return true
        end
    end
    return false
end

# part 1
sum(tv for (tv, nums) in zip(test_values, numbers) if solve_equation(tv, nums))

# part 2
sum(tv for (tv, nums) in zip(test_values, numbers) if solve_equation(tv, nums, part2 = true))
