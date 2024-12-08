;; should I be an antinode?

(use-modules (srfi srfi-1)
	     (srfi srfi-9)
	     (ice-9 textual-ports))

(define-record-type <antenna>
  (make-antenna frequency location)
  antenna?
  (frequency antenna-frequency)
  (location antenna-location))

;;; Helper Functions ---------------------------------------------------------------------

(define (boolean->number boolean)
  (if boolean 1 0))

(define (member? x xs)
  (not (eq? #f (member x xs))))

(define (find-distance p1 p2)
  (map (λ (x1 x2) (- x2 x1)) p1 p2))

(define (cartesian-product . lists)
  (fold-right (λ (xs ys) (append-map (λ (x) (map (λ (y) (cons x y)) ys)) xs)) '(()) lists))

(define (twice-area-of-triangle p1 p2 p3)
  (let ((x1 (car p1)) (y1 (cadr p1)) (x2 (car p2)) (y2 (cadr p2)) (x3 (car p3)) (y3 (cadr p3)))
    (+ (* x1 (- y2 y3))
       (* x2 (- y3 y1))
       (* x3 (- y1 y2)))))

;;; Main Bit -----------------------------------------------------------------------------

(define (antinode? f pos antennas)	; where f is a prodecure that checks if a spot should be an antinode given the location of two antennas
  (member? #t (map (λ (x) (member? #t x))
		   (map (λ (antenna1)
			  (map (λ (antenna2)
				 (f pos (antenna-location antenna1) (antenna-location antenna2))
				 ) (filter (λ (x)
					     (and
					      (equal? (antenna-frequency x) (antenna-frequency antenna1))
					      (not (equal? (antenna-location x) (antenna-location antenna1)))))
				 antennas))
			  ) antennas))))

(define (find-antennas-in-row map_row row_index)
  (fold (λ (x idx xs)
	  (cond
	   ((equal? x #\.) xs)
	   (else (cons (make-antenna x (list idx row_index)) xs))))
	'()
	map_row
	(iota (length map_row))))

(define (find-antennas puzzle_map)
  (let loop ((rows puzzle_map)
	     (row_index 0)
	     (result '()))
    (if (null? rows)
	(reverse result)
	(loop (cdr rows)
	      (+ row_index 1)
	      (append result
		      (find-antennas-in-row (car rows) row_index))))))

(define (count-antinodes f puzzle_map)
  (apply + (map (λ (x)
		  (boolean->number (antinode? f x (find-antennas puzzle_map))))
		(cartesian-product (iota (length puzzle_map)) (iota (length puzzle_map))))))


;; Create the map
(define puzzle_map (map string->list (string-split (get-string-all (open-input-file "input")) #\newline)))

;;; Part One -----------------------------------------------------------------------------

(define (twice-as-far-apart? p1 p2 p3)
  (equal? (map (λ (x) (* x 2)) (find-distance p1 p2))
	  (find-distance p1 p3)))

(display (string-append "Part One: "
			(number->string (count-antinodes twice-as-far-apart? puzzle_map))))

;;; Part Two -----------------------------------------------------------------------------

(define (collinear? p1 p2 p3)
  (equal? 0 (twice-area-of-triangle p1 p2 p3)))

(display (string-append "\nPart Two: "
			(number->string (count-antinodes collinear? puzzle_map))))


