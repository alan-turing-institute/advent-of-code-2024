library(data.table)
locations <- data.table::fread("input.txt")

# Part 1 - Total distance

print(paste("Total distance:",
            sum(abs(
              sort(locations$V1) - sort(locations$V2)
            ))))

# Part 2 - Similarity score

print(paste("Similarity score:",
            sum(
              intersect(locations$V1, locations$V2)  * table(locations$V2)[as.character(intersect(locations$V1, locations$V2))]
            )))
