wordsearch <- readLines("day-04/r_craddm/input.txt")

#Part 1
wordsearch_matrix <- apply(as.matrix(wordsearch), 1, function(x) unlist(strsplit(x, split = "")))
xmas_count <- 0
max_col <- ncol(wordsearch_matrix)
max_row <- nrow(wordsearch_matrix)
for (row in seq_len(nrow(wordsearch_matrix))) {
  for (column in seq_len(ncol(wordsearch_matrix))) {
    current_letter <- wordsearch_matrix[row, column]
    if (current_letter == "X") {
      # search left-to-right
      if ((column + 3) <= max_col) {
        if (paste(wordsearch_matrix[row, column:(column+3)], collapse = "") == "XMAS") {
          xmas_count <- xmas_count +1
        }
        # search left-to-right diagonally up
        if ((row + 3) <= max_row) {
          if (paste(diag(wordsearch_matrix[row:(row+3), column:(column+3)]), collapse = "") == "XMAS") {
            xmas_count <- xmas_count + 1
          } 
        }
        # search left-to-right diagonally down
        if ((row - 3) > 0) {
          if (paste(diag(wordsearch_matrix[(row-3):row, column:(column+3)][4:1, ]), collapse = "") == "XMAS") {
            xmas_count <- xmas_count + 1
          } 
        }
      }
      # search right-to-left
      if ((column - 3) > 0) {
        if (paste(wordsearch_matrix[row, (column-3):(column)], collapse = "") == "SAMX") {
          xmas_count <- xmas_count +1
        } 
        # search right-to-left diagonally down
        if ((row + 3) <= max_row) {
          if (paste(diag(wordsearch_matrix[row:(row+3), (column-3):column][, 4:1]), collapse = "") == "XMAS") {
            xmas_count <- xmas_count + 1
          } 
        }
        # search right-to-left diagonally up
        if ((row - 3) > 0) {
          if (paste(diag(wordsearch_matrix[(row-3):row, (column-3):column]), collapse = "") == "SAMX") {
            xmas_count <- xmas_count + 1
          } 
        }
      }
      # search down
      if ((row + 3) <= max_row) {
        if (paste(wordsearch_matrix[row:(row+3), column], collapse = "") == "XMAS") {
          xmas_count <- xmas_count +1
        } 
      }
      # search up
      if ((row - 3) > 0) {
        if (paste(wordsearch_matrix[row:(row-3), column], collapse = "") == "XMAS") {
          xmas_count <- xmas_count +1
        } 
      }
    }
  }
}

print(paste("Total XMAS:", xmas_count))

# Part 2

mas_count <- 0
for (row in seq(2, nrow(wordsearch_matrix) - 1)) {
  for (column in seq(2, ncol(wordsearch_matrix) - 1)) {
    current_letter <- wordsearch_matrix[row, column]
    if (current_letter == "A") {
      x_mas <- wordsearch_matrix[(row-1):(row+1), (column-1):(column+1)]
      top_to_bottom <- paste(diag(x_mas), collapse = "")
      bottom_to_top <- paste(diag(x_mas[3:1, ]), collapse = "")
      mas_count <- mas_count + all(any(top_to_bottom %in% c("MAS", "SAM")), any(bottom_to_top %in% c("MAS", "SAM")))
    }
  }
}
print(paste("Total X-MAS:", mas_count))
