(use-modules (srfi srfi-1))

;;; Memoisation --------------------------------------------------------------------------
;;; (For Part 2: Todo later)

(define (memoize f)
  (let [(table (make-hash-table))]
    (lambda (n)
      (let [(prev (hashq-ref table n))]
	(or prev
	    (let [(result (f n))]
	      (hashq-set! table n result)
	      result))))))

;;; Part One ----------------------------------------------------------------------------- 

;; early attempts to not have to use costly string->number & number->string
(define (length-of-number n)
  (cond ((< n 10) 1)
	(else (+ 1 (length-of-number (quotient n 10))))))

(define (split-number-in-half n)
  (let* [(half (/ (length-of-number n) 2))
	 (power (expt 10 half))
	 (left (quotient n power))
	 (right (- n (* left power)))]
    (list left right)))

(define (compute-stone stone)
  (cond
   [(zero? stone) (list 1)]
   [(even? (length-of-number stone)) (split-number-in-half stone)]
   [else (list (* stone 2024))]))

(define (count-stones n stone)
  (if (zero? n) 1
      (apply + (map (λ (s)
		      (count-stones (1- n) s))
		    (compute-stone stone)))))

(define (count-all-stones n lo_stones)
  (apply + (map (λ (s) (count-stones n s)) lo_stones)))

;;; --------------------------------------------------------------------------------------

(define initial_arrangement
  ;; list of stones
  )

(display (count-all-stones 25 initial_arrangement))
