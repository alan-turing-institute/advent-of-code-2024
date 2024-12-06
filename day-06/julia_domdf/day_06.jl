# directions (in order of right turns): 1 = facing up, 2 = facing right, 3 = facing down, 4 = facing left
const dirs = [(-1,0), (0,1), (1,0), (0,-1)]

function parse_input(filename)
    input = read(filename, String) |> str -> split(str, "\n")
    height = length(input); width = length(input[1])
    
    # initialisae then populate the grid and starting position
    grid = Matrix{Char}(undef, height, width); start_pos = nothing
    
    for (i, line) in enumerate(input)
        for (j, char) in enumerate(line)
            grid[i,j] = char
            if char == '^'
                start_pos = (i,j)
            end
        end
    end
    
    return grid, start_pos
end

function simulate_guard(grid:: Matrix{Char}, start_pos::Tuple{Int, Int}; check_loop::Bool = false)
    height, width = size(grid)
    # revisiting after part 2: now need to track position and direction
    visited_states = Set{Tuple{Tuple{Int,Int}, Int}}()
    
    # facing up at the starting position to begin
    pos = start_pos; dir = 1
    
    path_grid = copy(grid)
    while 1 ≤ pos[1] ≤ height && 1 ≤ pos[2] ≤ width
        # track visited positions and states
        state = (pos, dir); path_grid[pos...] = 'X'         
        
        if check_loop && state in visited_states
            return true
        end
        push!(visited_states, state)
        
        next_pos = (pos[1] + dirs[dir][1], pos[2] + dirs[dir][2])
        
        # if next position is in bounds and hits a wall, turn right
        if 1 ≤ next_pos[1] ≤ height && 1 ≤ next_pos[2] ≤ width && grid[next_pos...] == '#'
            dir = (dir + 1) > 4 ? 1 : dir + 1
        else
            pos = next_pos
        end
    end

    return check_loop ? false : ([s[1] for s in visited_states] |> unique |> length, path_grid)
end

grid, start_pos = parse_input("day_6_data.txt")

# part 1
simulate_guard(grid, start_pos)[1]

function find_loop_positions(grid, start_pos)
    height, width = size(grid)
    loop_positions = Set{Tuple{Int,Int}}()

    path_grid = simulate_guard(grid, start_pos)[2]
    
    for i in 1:height
        for j in 1:width
            if path_grid[i,j] != 'X' || # no benefit to placing obstacles the guard does not encounter... 
                path_grid[i,j] == '#'   # ...or where one already exists
                continue
            end
        
            # create a new grid with a new obstacle, and check for a loop
            test_grid = copy(grid); test_grid[i,j] = '#'
            
            if simulate_guard(test_grid, start_pos, check_loop = true)
                push!(loop_positions, (i,j))
            end
        end
    end
    
    return loop_positions
end

grid, start_pos = parse_input("day_6_data.txt")
find_loop_positions(grid, start_pos) |> length

using BenchmarkTools
@btime (find_loop_positions(grid, start_pos) |> length)