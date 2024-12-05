(use-modules (ice-9 textual-ports))

;; Helper Functions ----------------------------------------------------------------------

(define (middle-of-list lst)
  (if (null? (cdr lst))
      (car lst)
      (middle-of-list (reverse (cdr lst)))))

(define (create-pair-list lst)
  (define (drop-last l)
    (reverse (cdr (reverse l))))
  (map (lambda (i j) (list i j))
       (drop-last lst) (cdr lst)))

(define (list-diff lst1 lst2)
  (filter (lambda (x) (not (member x lst2))) lst1))

;; Main Functions ------------------------------------------------------------------------

(define (rule_string->rules rule_data)
  (map (lambda (str)
	 (define elements (string-split str #\|))
	 (map string->number (list (car elements) (car (cdr elements))))
	 ) (string-split rule_data #\newline)))

(define (update_string->updates updates_data)
  (map (lambda (line)
	(map (lambda (x) (string->number x)) (string-split line #\,)))
      (string-split updates_data #\newline)))

(define (compliant? pair rules)
  (not (eq? #f (member pair rules))))

(define (is-update-compliant? update rules)
  (not (member #f
	       (map (lambda (pair) (compliant? pair rules)) update ))))

(define (updates_port->updates port)
  (update_string->updates (get-string-all port)))

(define (rules_port->rules port)
  (rule_string->rules (get-string-all port)))

;; Quicksort implementation for sorting updates
(define (sort-update lst rules)
  (cond
   ((or (null? lst) (null? (cdr lst))) lst)
   (else
    (let ((pivot (car lst)) 
          (rest (cdr lst)))
      (append
       (sort-update (filter (lambda (x) (compliant? (list x pivot) rules)) rest) rules)
       (list pivot) 
       (sort-update (filter (lambda (x) (compliant? (list pivot x) rules)) rest) rules))))))

;; ---------------------------------------------------------------------------------------

(define rules (rules_port->rules (open-input-file "rules"))) ; can't find how to string-split on a double new line
(define updates (updates_port->updates (open-input-file "updates")))

(define compliant_updates
  (filter (lambda (update)
	    (is-update-compliant? (create-pair-list update) rules))
	  updates))

(define non_compliant_updates (list-diff updates compliant_updates))

;; Results  ------------------------------------------------------------------------------

(display (string-append "Answer to Part One: "
			(number->string (apply + (map middle-of-list compliant_updates)))
			"\nAnswer to Part Two: "
			(number->string (apply + (map middle-of-list (map (lambda (update) (sort-update update rules)) non_compliant_updates))))
			))
