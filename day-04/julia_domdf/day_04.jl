wordsearch = read("day_4_data.txt", String) |> ws -> split(ws, "\n") |> ws -> map(String, ws)

function count_word(grid::Vector{String}, target_word::String = "XMAS")
    word_count = 0
    n_rows = [grid[i][1] for i in 1:length(grid)] |> length
    n_cols = grid[1] |> length
    
    for i in 1:n_rows, j in 1:n_cols
        for dx in -1:1, dy in -1:1
            # go through every direction except dx = 0, dy = 0, which is stationary
            (dx == 0 && dy == 0) && continue
            valid = true
            
            current_i, current_j = i, j
            for k in 1:length(target_word)
                # catch when we move beyond the grid
                if current_i < 1 || current_i > n_rows || current_j < 1 || current_j > n_cols
                    valid = false; break
                end
                # are we on track to spell the target word (does the current character match)?
                if grid[current_i][current_j] != target_word[k]
                    valid = false; break
                end
                #...if so, keep stepping in the given direction
                current_i += dx; current_j += dy
            end
            
            if valid
                # we've found an "xmas" so add it to the count
                word_count += 1
            end
        end
    end
    
    return word_count
end

# part 1
count_word(wordsearch)

function count_X_words(grid::Vector{String})
    word_count = 0
    n_rows = [grid[i][1] for i in 1:length(grid)] |> length
    n_cols = grid[1] |> length

    # we only need to look for the "A"'s since they'll always be the centre of the X
    for i in 1:n_rows, j in 1:n_cols
        if grid[i][j] != 'A'
            continue
        end
        
        # catch when diagonals move beyond the grid
        if 1 < i < n_rows && 1 < j < n_cols
            # get characters from the diagonal positions
            lr_chars = [string(grid[i-1][j-1]), string(grid[i+1][j+1])]  # diagonal from left to right
            rl_chars = [string(grid[i-1][j+1]), string(grid[i+1][j-1])]  # diagonal from right to left

            # valid x patterns must be M->A->S or S->A->M
            if (lr_chars in [["M", "S"], ["S", "M"]]) && (rl_chars in [["M", "S"], ["S", "M"]])
                 word_count += 1
            end
        end
    end
    return word_count
end

# part 2
count_X_words(wordsearch)