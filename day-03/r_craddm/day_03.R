library(stringi)

memory <-
  paste(readLines("day-03/r_craddm/input.txt"), collapse = "")

# Part 1 - Total of all multiplies
all_muls <- unlist(stri_extract_all(memory,
                                     regex = "mul\\([[:digit:]]+,[[:digit:]]+\\)"))
products <- vapply(all_muls,
             function(x) {
               first_split <- stri_extract_all(x,
                                               regex = "[[:digit:]]+")
               vapply(first_split,
                      function(x)
                        prod(as.numeric(x)),
                      numeric(1))
             },
             numeric(1))
print(paste("Total:", sum(products)))

# Part 2 - Only include permitted multiplies

all_sections <- unlist(
  stri_extract_all(memory,
                   regex = "mul\\([[:digit:]]+,[[:digit:]]+\\)|do\\(\\)|don't\\(\\)")
)

valid <- TRUE
total <- 0
for (section in all_sections) {
  if (identical(section, "don't()")) {
    valid <- FALSE
    next
  } else if (identical(section, "do()")) {
    valid <- TRUE
    next
  }
  if (valid) {
    total <- 
      total + prod(as.numeric(
        unlist(
          stri_extract_all(section,
                           regex = "[[:digit:]]+")
          )
        ))
  }
}
print(paste("Total:", total))
