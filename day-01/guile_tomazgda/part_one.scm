(use-modules (ice-9 textual-ports))
(define port (open-input-file "input"))

;; read all of the input file and produce a list of strings seperated by new lines
(define input-list (string-split (get-string-all port) #\newline))

;; return the last element of a list
(define (last l)
  (cond ((null? (cdr l)) (car l))
	(else (last (cdr l)))))

(define (total-distance input)
  ;; produce a list of pairs (first_id second_id) from the sorted id lists.
  (define sorted-list
    (map (lambda (i j) (list i j))
	 ;; first list
	 (sort (map (lambda (line)
		      (string->number (car (string-split line #\space)))) input) <)
	 ;; second list
	 (sort (map (lambda (line)
		      (string->number (last (string-split line #\space)))) input) <)
	 ))

  ;; takes a pair of ids and returns their different
  (define (reduce-pair pair)
    (abs (- (car pair) (car (cdr pair)))))

  ;; reduce across the list of pairs, and return the sum.
  (apply + (map reduce-pair sorted-list)))

(total-distance input-list)
