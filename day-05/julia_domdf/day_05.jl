using DelimitedFiles
input = readdlm("day_5_data.txt")[:,1]

rules, updates = [], []
for line in input
    if contains(line, "|")
        push!(rules, line)
    else
        push!(updates, line)
    end
end

all_pages = split.(updates, ",") |> u -> [parse.(Int, str) for str in u]

function build_order_map(rules::Vector{Any})
    order_map = Dict{Int, Set{Int}}()

    # process each rule "X|Y" => before_page = X, after_page = Y
    for rule in rules
        before_page, after_page = split(rule, "|") |> nums -> parse.(Int, nums)
        # first rule for this page number? create a new entry for it
        if !haskey(order_map, before_page)
            order_map[before_page] = Set{Int}()
        end
        # otherwise we can add the rule to the existing entry for the page
        push!(order_map[before_page], after_page)
    end
    return order_map
end

function is_correct_order(pages::Vector{Int}, order_map::Dict{Int, Set{Int}})
    for i in 1:length(pages)
        current_page = pages[i]
        # future pages
        for j in (i+1):length(pages)
            next_page = pages[j]
            # later pages should all come after current_page
            if haskey(order_map, next_page) && current_page in order_map[next_page]
                return false
            end
        end
    end
    return true
end

function find_middle_page(pages::Vector{Int})
    middle_index = (length(pages) / 2) |> ceil |> Int
    return pages[middle_index]
end

middle_pages_pt1 = Int[]
for pages in all_pages
    if is_correct_order(pages, build_order_map(rules))
        push!(middle_pages_pt1, find_middle_page(pages))
    end
end

# part 1
middle_pages_pt1 |> sum

function reorder_pages(pages::Vector{Int}, order_map::Dict{Int, Set{Int}})
    # for a given order of pages, find the number of pages that must come after the current page 'x'
    sorted_pages = sort(pages,
        by = x -> sum(y in order_map[x] for y in pages),
        # descending order so pages with fewer dependencies...
        # ...(fewer numbers that must follow it) are towards the end
        rev = true)
    return sorted_pages
end

middle_pages_pt2 = Int[]
for pages in all_pages
    if !is_correct_order(pages, build_order_map(rules))
        push!(middle_pages_pt2, reorder_pages(pages, build_order_map(rules)) |> find_middle_page)
    end
end

# part 2
middle_pages_pt2 |> sum