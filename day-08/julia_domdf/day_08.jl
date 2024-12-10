map = read("day_8_data.txt", String) |> str -> split(str, "\n")
map_height = map |> length; map_width = grid |> first |> length

function parse_input(input::String)
    lines = split(strip(input), '\n')
    antennas = Tuple{Int, Int, Char}[]  # (x, y, frequency)
    
    for (y, line) in enumerate(lines)
        for (x, char) in enumerate(line)
            if char != '.'
                push!(antennas, (x, y, char))
            end
        end
    end
    
    return antennas
end

function find_antinodes(antennas, map_width::Int, map_height::Int; part2::Bool = false)
    antinodes = Set{Tuple{Int, Int}}()
    
    # group antennas (antennae?) by frequency
    freq_groups = Dict{Char, Vector{Tuple{Int, Int, Char}}}()
    for antenna in antennas
        push!(get!(freq_groups, antenna[3], []), antenna)
    end
    
    # for each frequency group, find antinode spacings
    for (freq, antennas_same_freq) in freq_groups
        for i in 1:length(antennas_same_freq)
            for j in (i+1):length(antennas_same_freq)
                (x1, y1, _) = antennas_same_freq[i]; (x2, y2, _) = antennas_same_freq[j]
                
                # distance vector between antennas
                dx = x2 - x1; dy = y2 - y1
                
                # how many steps can we take in this direction before exceeding the map dims?
                function find_max_n(x_start, y_start, dx, dy)
                    n = 0
                    while true
                        next_x = x_start + (n + 1) * dx; next_y = y_start + (n + 1) * dy
                        if !(1 <= next_x <= map_width && 1 <= next_y <= map_height)
                            break
                        end
                        n += 1
                    end
                    return n
                end

                # how many steps can we take before reaching the edges
                n_max_fwd = find_max_n(x2, y2, dx, dy); n_max_back = find_max_n(x1, y1, -dx, -dy)
                
                if part2
                    # start from zero at add the location of the antenna
                    for n in 0:n_max_fwd
                        push!(antinodes, (x2 + n * dx, y2 + n * dy))
                    end
                    for n in 0:n_max_back
                        push!(antinodes, (x1 - n * dx, y1 - n * dy))
                    end
                else
                    if n_max_fwd >= 1
                        push!(antinodes, (x2 + dx, y2 + dy))
                    end
                    if n_max_back >= 1
                        push!(antinodes, (x1 - dx, y1 - dy))
                    end
                end
            end
        end
    end
    
    return antinodes
end

antennas = read("day_8_data.txt", String) |> parse_input

# part 1
find_antinodes(antennas, map_width, map_height) |> length

# part 2
find_antinodes(antennas, map_width, map_height, part2 = true) |> length