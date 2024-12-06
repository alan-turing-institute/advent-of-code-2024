(add-to-load-path "/home/tomaz/code/advent-of-code-2024/day-04/guile_tomazgda")
(use-modules (utils))

(define port (open-input-file "input"))
(define input_array (port->array port))

;; Part 1
(define n_words (word-search input_array "XMAS"))
(display (string-append
	  "Number of XMASs Found: "
	  (number->string n_words)
	  "\n"))

;;; Part 2
(define n_crosses (cross-search input_array))
(display (string-append
	  "Number of Crosses Found: "
	  (number->string n_crosses)
	  "\n"))






