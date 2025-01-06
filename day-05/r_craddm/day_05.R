library(stringr)
pages <- readLines("day-05/r_craddm/input.txt")

break_index <- which(pages == "")
rules <- lapply(pages[1:(break_index-1)],
                \(rule) as.numeric(stringr::str_split_1(rule, "[|]")))
updates <- lapply(pages[(break_index+1):length(pages)],
                  \(update) as.numeric(stringr::str_split_1(update, ",")))

good_total <- 0
bad_total <- 0
for (update in updates) {
  applicable_rules <- rules[unlist(lapply(rules, \(rule) {all(rule %in% update)}))]
  rule_followed <- logical(length(applicable_rules))
  for (rule_no in seq_along(applicable_rules)) {
    page_order <- update[which(update %in% applicable_rules[[rule_no]])]
    if (all(page_order == applicable_rules[[rule_no]])) {
      rule_followed[rule_no] <- TRUE
    } else {
      break
    }
  }
  if (all(rule_followed)) {
    good_total <- good_total + as.numeric(update[ceiling(length(update)/2)])
  } else {
    rules_not_met <- TRUE
    while (rules_not_met) {
      for (rule_no in seq_along(applicable_rules)) {
        page_order <- which(update %in% applicable_rules[[rule_no]])
        if (all(applicable_rules[[rule_no]] == update[page_order])) {
          rule_followed[rule_no] <- TRUE
          next
        }
        update[page_order] <- update[rev(page_order)]
      }
      if (all(rule_followed)) {
        rules_not_met <- FALSE
      }
    }
    bad_total <- bad_total + as.numeric(update[ceiling(length(update)/2)])
  }
}
