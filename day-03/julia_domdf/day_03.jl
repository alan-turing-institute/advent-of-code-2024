input = read("day_3_data.txt", String)

function process_muls(input::String, check_mul_status::Bool = false)
    # 😢 regex. Pattern for mul operations - including up to 3 digit numbers
    mul_pattern = r"mul\s*\((\d{1,3}),(\d{1,3})\)"

    # pattern for do/don't operations
    control_pattern = r"(do|don't)\s*\(\s*\)"
    
    # set up enabling multiplcations, starting result at zero, with an empty list of matches
    mul_enabled = true; result = 0; all_matches = []
    
    for m in eachmatch(mul_pattern, input)
        push!(all_matches, 
                (position = m.offset, # the position in the input of the `mul(x, y)`
                type = "mul",         # the type of operation (multiplication)
                match = m)            # the operation itself
            )
    end
    
    # if we are checking for status (`do()`'s and `don't()`'s)...
    if check_mul_status
        for m in eachmatch(control_pattern, input)
            push!(all_matches, 
                    (position = m.offset, # the position in the input of the `do()` or `don't()`
                    type = "control",     # the type of operation (control)
                    match = m))           # the operation itself
        end
    end
    
    # since i've just appended the control ops, i need re-order them based on their position
    sort!(all_matches, by = x -> x.position)
    
    # ...now they can be processed in order
    for op in all_matches
        if op.type == "control" # update mul_enabled based on control operation
            mul_enabled = (op.match[1] == "do") # a `don't()` will return false and disable multiplcations, until a `do()`
        elseif op.type == "mul" && mul_enabled
            result += parse(Int, op.match[1]) * parse(Int, op.match[2]) # increment result based on the mul (if enabled)
        end
    end
    
    return result
end

# part 1
process_muls(input)

# part 2
process_muls(input, true)