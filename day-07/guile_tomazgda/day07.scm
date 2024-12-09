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

(define (|| x y)
  (string->number (string-append (number->string x) (number->string y))))

;; Part One ------------------------------------------------------------------------------

(define (make-operator-lists equation)
  (apply cartesian-product (make-list (- (length equation) 1) (list + *))))

(define (evaluate-equation equation operator_list)
  (fold (lambda (e op previous)
	  (op previous e))
	(car equation)
	(cdr equation) 
	operator_list))

(define (can-equation-satisfy-target target equation op-proc)
  (not (eq? #f (member target
		       ;; create list of possible evaluations
		       (map (lambda (operator_list)
			      (evaluate-equation equation operator_list))
			    (op-proc equation))))))

(define (get-target line)
  (string->number (car (string-split line #\:))))

(define (get-equation line)
  (map string->number (cdr (string-split (cadr (string-split line #\:)) #\space))))

(define (solve-part targets_and_equations op-proc)
  (apply + (map (lambda (x)
		(cond
		 ((can-equation-satisfy-target (get-target x) (get-equation x) op-proc) (get-target x))
		 (else 0))
		) targets_and_equations)))

;; Part Two ------------------------------------------------------------------------------

(define (make-operator-lists-p2 equation)
  (apply cartesian-product (make-list (- (length equation) 1) (list + * ||))))

;; Results -------------------------------------------------------------------------------

(display (string-append
	  "Part One Result: "
	  (number->string  (solve-part (string-split (get-string-all (open-input-file "input")) #\newline) make-operator-lists))
	  "\nPart Two Result: "
	  (number->string  (solve-part (string-split (get-string-all (open-input-file "input")) #\newline) make-operator-lists-p2))))


