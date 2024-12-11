library(stringr)
library(purrr)

test_data <- function() {
  matrix(
    c("....#.....",
      ".........#",
      "..........",
      "..#.......",
      ".......#..",
      "..........",
      ".#..^.....",
      "........#.",
      "#.........",
      "......#..."),
    nrow = 10,
    byrow = TRUE
  ) |>
    apply(1, str_split_1, "") |>
    t()
}

update_location <- function(direction, location) {
  if (direction == "^") {
    location[1] <- location[1] - 1
  } else if (direction == "v") {
    location[1] <- location[1] + 1
  } else if (direction == ">") {
    location[2] <- location[2] + 1
  } else if (direction == "<") {
    location[2] <- location[2] - 1
  }
  location
}

init_map <- readLines("day-06/r_craddm/input.txt") 
init_map <- matrix(init_map,
                   nrow = length(init_map),
                   byrow = TRUE)
init_map <- t(apply(init_map, 1, str_split_1, ""))

walk_map <- function(init_map) {
  location <- which(init_map == "^", arr.ind = TRUE)
  guard <- "^"
  on_map <- TRUE
  map_size <- dim(init_map)
  locations <- list(list(location = location, direction = guard))
  loop <- FALSE
  while (on_map) {
    next_location <- update_location(guard,
                                     location)
    if (any(next_location < 1) | any(next_location > map_size)) {
      on_map <- FALSE
      break
    }
    if (init_map[next_location] == "#") {
      guard <- switch(
        guard,
        "^" = ">",
        "<" = "^",
        ">" = "v",
        "v" = "<",
      )
    } else {
      location <- next_location
      locations <- append(locations, list(list(location = location, direction = guard)))
      if (any(duplicated(locations))) {
        loop <- TRUE
        break
      }
    }
  }
  list(locations = locations, loop = loop)
}

do_run <- function(init_map) {
  output_map <- walk_map(init_map)
  occupied_spots <- unique(map_depth(output_map$locations, 1, "location"))
  print(paste("Unique positions:", length(occupied_spots)))
  looped <- 0
  for (obstacle in seq(2, length(occupied_spots))) {
    next_map <- init_map
    next_map[occupied_spots[[obstacle]][1], occupied_spots[[obstacle]][2]] <- "#"
    out <- walk_map(next_map)
    looped <- looped + out$loop
  }
  print(paste("Total loops:", sum(looped)))
}

do_run(init_map)