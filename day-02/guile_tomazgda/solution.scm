(use-modules (ice-9 textual-ports))
(define port (open-input-file "input"))

;; string -> number list list
(define reports
  (map (lambda (report) 
	 (map (lambda (element) (string->number element)) (string-split report #\space)))
       (string-split (get-string-all port) #\newline)))

;; pair -> boolean
(define (check-tolerance pair)
  (let ((diff (abs (- (car pair) (car (cdr pair))))))
    (and
     (<= diff 3)
     (>= diff 1 ))))

;; return a new list with the last element removed
(define (drop-last l)
  (reverse (cdr (reverse l))))

;; number list -> pair list
(define (create-pair-list lst)
  (map (lambda (i j) (list i j))
       (drop-last lst) (cdr lst)))

;; list -> boolean 
(define (safe? lst)
  (and
   (or (sorted? lst <) (sorted? lst >))
   (if (memq #f (map check-tolerance (create-pair-list lst))) #f #t)))

;; string list -> bool list
(define safe-bool-list
  (map (lambda (x) (safe? x)) reports))

;; sum up safe reports
(display (string-append "Number of Safe Reports: "
			(number->string (apply + (map (lambda (x) (if x 1 0)) safe-bool-list)))
			"\n"))

;;; PART TWO -- With the Problem Dampener 

;; Powerset Function
(define (powerset lst)
  (if (null? lst)
      '(())
      (let ((rst (powerset (cdr lst))))
        (append (map (lambda (x) (cons (car lst) x))
                     rst)
                rst)))) 

;; Evaluate the subsets of a set with length n - 1
(define (damped-subsets lst)
  (filter (lambda (x) (= (length x) (- (length lst) 1)))
       (powerset lst)))

(define (damped-safe? lst)
  (if (memq #t (map safe? (damped-subsets lst))) #t #f))

;; string list -> bool list
(define damped-safe-bool-list
  (map (lambda (x) (damped-safe? x)) reports))

;; sum up damped-safe reports
(display (string-append "After using the Problem Damper: "
			(number->string (apply + (map (lambda (x) (if x 1 0)) damped-safe-bool-list)))
			"\n"))
