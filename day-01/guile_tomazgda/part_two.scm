(use-modules (ice-9 textual-ports))
(define port (open-input-file "input"))

;; read all of the input file and produce a list of strings seperated by new lines
(define input-list (string-split (get-string-all port) #\newline))

;; return the last element of a list
(define (last l)
  (cond ((null? (cdr l)) (car l))
	(else (last (cdr l)))))

(define (total-similarity input)
  ;; produce a list containing all the left_ids
  (define left-list
    (map (lambda (line)
	   (string->number (car (string-split line #\space)))) input))

  ;; produce a list containing all the right_ids
  (define right-list
    (map (lambda (line)
	   (string->number (last (string-split line #\space)))) input))

  ;; make a list from the left list corresponding to the number of times each element appeared in the right list
  (define sorted-list
    (map (lambda (element)
	   (* element (length (filter (lambda (x) (eq? x element)) right-list))))
	 left-list))

  ;; sum up the elements of the sorted list
  (apply + sorted-list))

(total-similarity input-list)
