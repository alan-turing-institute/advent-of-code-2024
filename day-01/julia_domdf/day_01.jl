using DelimitedFiles

locations = readdlm("input.txt", Int) # read in the locations 
sorted_locs = sort(locations, dims = 1) # sort each column

Δlocs = abs.(sorted_locs[:, 1] - sorted_locs[:, 2]) # take the difference for each row

# part 1
sum(Δlocs)

sim_scores = Dict{Int, Int}()
for left_loc in locations[:, 1]
    # count how many times each left loc appears in all right locs
    sim_scores[left_loc] = count(x -> x == left_loc, locations[:, 2])
end

# part 2
sum(key * sim_scores[key] for key in keys(sim_scores))