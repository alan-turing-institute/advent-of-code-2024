reports <- readLines("day-02/r_craddm/input.txt")

# Part 1 - How many are safe?
part_one <- lapply(reports, function(x) {
  report <- as.numeric(unlist(strsplit(x, split = " ")))
  differences <- diff(report)
  (all(differences > 0) |
      all(differences < 0)) && all(abs(differences) <= 3)
})

print(paste("Total safe reports:", sum(unlist(part_one))))

# Part 2 - Fault tolerance

part_two <- lapply(reports, function(x) {
  report <- as.numeric(unlist(strsplit(x, split = " ")))
  safety_check <- function(x) {
    (all(x > 0) | all(x < 0)) && all(abs(x) <= 3)
  }
  if (safety_check(diff(report))) {
    return(TRUE)
  } else {
    for (element in seq_along(report)) {
      if (safety_check(diff(report[-element]))) {
        return(TRUE)
      }
    }
  }
})

print(paste("Total safe reports:", sum(unlist(part_two))))