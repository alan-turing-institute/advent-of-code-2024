reports = [parse.(Int, split(line)) for line in readlines("day_2_data.txt")] # read in the reports 

function safe_report_check(levels::Vector{Int64}, dampener::Bool = false)
    
    Δ_levels = diff(levels) # find differences between neighbouring levels
    
    valid_Δs = [1 <= abs(Δ) <= 3 for Δ in Δ_levels] # all absolute deltas must be between 1 and 3
    same_dir = all(x -> x > 0, Δ_levels) || all(x -> x < 0, Δ_levels) # deltas must be either all +ve or all -ve

    if !same_dir || count(!, valid_Δs) > 0
        # if we don't meet criteria, try removing one level (if the dampener is enabled)
        if dampener > 0
            for i in 1:length(levels)
                # create a new report without the i-th level
                new_levels = vcat(levels[begin:i-1], levels[i+1:end])
                new_Δ_levels = diff(new_levels)
                # are remaining deltas either all +ve or all -ve...
                if (all(x -> x > 0, new_Δ_levels) || all(x -> x < 0, new_Δ_levels)) &&
                # ...and are the absolute deltas all between 1 and 3?
                   all(x -> 1 <= abs(x) <= 3, new_Δ_levels)
                    return true
                end
            end
        end
        return false
    end
    
    return true
end

# part 1
safe_report_check.(reports) |> sum

# part 2
safe_report_check.(reports, true) |> sum