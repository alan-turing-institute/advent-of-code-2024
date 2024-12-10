function parse_disk_map(disk_map::String)
    files = []; free_spaces = []; i = 1
    while i <= length(disk_map)
        file_length = parse(Int, disk_map[i])
        push!(files, file_length)
        i += 1
        if i <= length(disk_map)
            free_space_length = parse(Int, disk_map[i])
            push!(free_spaces, free_space_length)
            i += 1
        end
    end
    return files, free_spaces
end

function compact_disk(files::Vector{Int}, free_spaces::Vector{Int}; part2::Bool = false)
    total_blocks = sum(files) + sum(free_spaces)
    disk = Vector{Int}(undef, total_blocks)
    file_positions = Dict{Int, Int}()
    current_pos = 1
    
    # initial layout
    for (i, file_length) in enumerate(files)
        file_positions[i-1] = current_pos
        disk[current_pos:current_pos + file_length - 1] .= i-1 
        current_pos += file_length
        if i <= length(free_spaces)
            disk[current_pos:current_pos + free_spaces[i] - 1] .= -1
            current_pos += free_spaces[i]
        end
    end
        
    if part2
        total_files = length(files)
        
        # track gaps
        found_gaps = Set{Int}(); max_gap_needed = maximum(files)
        
        # part 2
        for (idx, file_id) in enumerate(reverse(0:length(files)-1))
            @info "Processing file" progress="$(idx)/$(total_files)" file_id
            
            file_length = files[file_id + 1]; start_pos = file_positions[file_id]
            
            # find leftmost suitable free space
            current_free_start = 1
            while current_free_start < start_pos
                end_pos = min(current_free_start + file_length - 1, length(disk))
                if all(==(- 1), @view disk[current_free_start:end_pos])
                    disk[current_free_start:current_free_start + file_length - 1] .= file_id
                    disk[start_pos:start_pos + file_length - 1] .= -1
                    break
                end
                
                # count consecutive -1s to track gap sizes
                if disk[current_free_start] == -1
                    gap_size = 1
                    pos = current_free_start + 1
                    while pos <= length(disk) && disk[pos] == -1
                        gap_size += 1
                        pos += 1
                    end
                    push!(found_gaps, gap_size)
                    
                    # we can stop once all possible gap sizes up to max needed are found
                    if length(found_gaps) == max_gap_needed
                        break
                    end
                end
                
                current_free_start += 1
            end
        end
    else
        # part 1
        for i in reverse(1:total_blocks)
            if disk[i] != -1
                # find the leftmost free space before this position
                free_space_idx = findfirst(x -> x == -1, @view disk[1:i])
                if !isnothing(free_space_idx)
                    # move block
                    disk[free_space_idx] = disk[i]
                    disk[i] = -1
                end
            end
        end
    end
    
    return disk
end

function calculate_checksum(disk::Vector{Int})
    checksum = 0
    for (i, block) in enumerate(disk)
        if block != -1
            checksum += (i - 1) * block
        end
    end
    return checksum
end

function solve(disk_map::String; part2::Bool = false)
    
    return compact_disk(files, free_spaces, part2=part2) |> calculate_checksum
end

files, free_spaces = read("day_9_data.txt", String) |> parse_disk_map

# part 1
compact_disk(files, free_spaces) |> calculate_checksum

# part 2
compact_disk(files, free_spaces, part2 = true) |> calculate_checksum