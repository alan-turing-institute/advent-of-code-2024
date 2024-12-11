;;; Plutonian Pebbles --------------------------------------------------------------------

(use-modules (srfi srfi-1))

(define (length-of-number n)
  (if (< n 10) 1
      (+ 1 (length-of-number (quotient n 10)))))

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

(define count-stones
  (let [(table (make-hash-table))]
    (lambda (n stone)
      (let [(found (hash-ref table (list n stone)))]
	(or found
	    (let [(result (if (zero? n) 1
			      (apply + (map (λ (s)
					      (count-stones (1- n) s))
					    (compute-stone stone)))))]
	      (hash-set! table (list n stone) result)
	      result))))))

(define (count-all-stones n lo_stones)
  (apply + (map (λ (s) (count-stones n s)) lo_stones)))

;;; --------------------------------------------------------------------------------------

(define initial_arrangement
  ;; puzzle input
  )

(display (string-append "Part One: "
			(number->string (count-all-stones 25 initial_arrangement))
			"\nPart Two: "
			(number->string (count-all-stones 75 initial_arrangement))))


