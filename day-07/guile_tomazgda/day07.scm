;; Take a list of n length, enumerate all possible combinations of 1 and 0 in that list

(use-modules (srfi srfi-1)
	     (ice-9 textual-ports))

;; Helper Function  ------------------------------------------------------------------------

(define (cartesian-product . lists)
  (fold-right (lambda (xs ys)
                (append-map (lambda (x)
                              (map (lambda (y)
                                     (cons x y))
                                   ys))
                            xs))
              '(())
              lists))

(define (make-all-operator-lists equation)
  (apply cartesian-product (make-list (- (length equation) 1) '(0 1))))

;; Part One ------------------------------------------------------------------------------

(define (evaluate-equation equation operator_list)
  (fold-right (lambda (elem1 elem2 previous)
		(cond
		 ((equal? elem2 0) (+ previous elem1))
		 ((equal? elem2 1) (* previous elem1))))
	      (car equation)
	      (reverse (cdr equation)) 
	      (reverse operator_list)))

(define (can-equation-satisfy-target target equation)
  (not (eq? #f (member target
		       ;; create list of possible evaluations
		       (map (lambda (operator_list)
			      (evaluate-equation equation operator_list))
			    (make-all-operator-lists equation))))))

(define (get-target line)
  (string->number (car (string-split line #\:))))

(define (get-equation line)
  (map string->number (cdr (string-split (cadr (string-split line #\:)) #\space))))

(define (solve-part-one targets_and_equations)
  (apply + (map (lambda (x)
		(cond
		 ((can-equation-satisfy-target (get-target x) (get-equation x)) (get-target x))
		 (else 0))
		) targets_and_equations)))

;; Results -------------------------------------------------------------------------------

(display (string-append
	  "Part One Result: "
	  (number->string  (solve-part-one (string-split (get-string-all (open-input-file "input")) #\newline)))))


