test_data <-
  c(
    "190: 10 19",
    "3267: 81 40 27",
    "83: 17 5",
    "156: 15 6",
    "7290: 6 8 6 15",
    "161011: 16 10 13",
    "192: 17 8 14",
    "21037: 9 7 18 13",
    "292: 11 6 16 20"
  )

oprep <- function(operators, spots) {
  expand.grid(rep(list(operators), times = spots), stringsAsFactors = FALSE)
}

concat_numeric <- function(number1, number2) {
  as.numeric(paste0(number1, number2))
}

parse_input <- function(input, operators) {
  hits <- 0
  total_calibration <- 0
  for (row in seq_along(input)) {
    split_string <- unlist(strsplit(input[row], ": "))
    target <- as.numeric(split_string[[1]])
    values <- as.numeric(unlist(strsplit(split_string[[2]], " ")))
    op_list <- oprep(operators, length(values) - 1)
    possible_values <- numeric(nrow(op_list))
    accumulation <- numeric(length(values) - 1)
    for (ops in seq(1, nrow(op_list))) {
      accumulation[1] <- op_list[ops, 1][[1]](values[1], values[2])
      if (length(values) > 2) {
        for (value in seq(2, length(values) - 1)) {
          accumulation[value] <- op_list[ops, value][[1]](accumulation[value - 1], values[value + 1])
        }
      }
      possible_values[ops] <- accumulation[length(values) - 1]
    }
    if (target %in% possible_values) {
      hits <- hits + 1
      total_calibration <- total_calibration + target
    } 
  }
  print(paste0("Total hits: ", hits, "; calibration: ", total_calibration))
}

parsed_results <-

real_data <- readLines("day-07/r_craddm/input.txt")

#Part 1
part_1_ops <- c(`+`, `*`)
parse_input(test_data, part_1_ops)
parse_input(real_data, part_1_ops)

#Part 2
part_2_ops <- c(`+`, `*`, concat_numeric)
parse_input(test_data, part_2_ops)
parse_input(real_data, part_2_ops)
