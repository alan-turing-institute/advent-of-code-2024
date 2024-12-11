(use-modules (ice-9 arrays) (ice-9 textual-ports) (srfi srfi-1))

;;; Graphs (HtDP) ------------------------------------------------------------------------

(define (neighbours name graph)
  (caddr (assq name graph)))

;; -> (list-f routes)
(define (find-routes/list lo_origins dest graph)
  (if (null? lo_origins)
      '()
      (apply append (map (lambda (o) (find-routes o dest graph)) lo_origins))))

;; -> (list-of routes)
(define (find-routes origin dest graph)
  (if (equal? origin dest)
      (list (list dest))
      (let [(possible_routes
	     (find-routes/list (neighbours origin graph) dest graph))]
	(map (lambda (r) (cons origin r)) possible_routes))))

;;; Scoring a Graph ----------------------------------------------------------------------

(define (score-graph graph scoring_proc)
  (apply + (map (λ (trailhead)
		  (scoring_proc trailhead 9 graph))
		(find-targets 0 graph))))

(define (score-trailhead-distinct trailhead value graph)
  (apply + (map (λ (target)
		  (length (find-routes trailhead target graph)))
		(find-targets value graph))))

(define (score-trailhead trailhead value graph)
  (length (filter-map (λ (target)
			(not (null? (find-routes trailhead target graph))))
		      (find-targets value graph))))

;; extracts from a graph all nodes equal to a target value
(define (find-targets value graph)
  (filter-map (λ (node)
		(cond [(equal? value (cadr node)) (car node)]
		      [else #f])
		) graph ))

;;; Helper Functions ---------------------------------------------------------------------

(define-values (LEFT RIGHT UP DOWN) (values '(0 -1) '(0 1) '(-1 0) '(1 0)))

(define (path->string p)
  (get-string-all (open-input-file p)))

(define (add-pair p1 p2)
  (map (lambda (x y) (+ x y)) p1 p2))

(define (string->row_list str)
  (map string->list (string-split str #\newline)))

(define (string->array str) 
  (list->array 2 (string->row_list str)))

(define (position->symbol y x)
  (string->symbol (string-append (number->string y) ":" (number->string x))))

(define (char->number ch)
  ((compose string->number string) ch))

;;; Creating a Graph ---------------------------------------------------------------------

(define (array->graph array)
  (let loop [(x (iota (cadr (array-dimensions array))))
	     (y (iota (car (array-dimensions array))))
	     (graph '())]

    (cond [(null? y) (reverse graph)]
	  [(null? x)
	   (loop (iota (cadr (array-dimensions array))) (cdr y) graph)]
	  [else
	   (loop
	    (cdr x) y
	    (cons (list (position->symbol (car y) (car x))
			(char->number (array-ref array (car y) (car x)))
			(filter values
				(map (λ (dir)
				       (let [(neighbour_x (+ (car x) (car dir)))
					     (neighbour_y (+ (car y) (cadr dir)))]
					 
					 (let [(current_value (char->number (array-ref array (car y) (car x))))
					       (neighbour_value (char->number (array-ref array neighbour_y neighbour_x)))]

					   (cond [(equal? (+ current_value 1) neighbour_value) (position->symbol neighbour_y neighbour_x)]
						 [else #f]))))
				     
				     (filter (λ (any_dir) (array-in-bounds? array (+ (car y) (cadr any_dir)) (+ (car x) (car any_dir))))
					     (list LEFT RIGHT UP DOWN))))
			) graph))])))

;;; Results ------------------------------------------------------------------------------

(define g ((compose array->graph string->array path->string) "input"))

(display (string-append "Part One: "
			(number->string (score-graph g score-trailhead))
			"\nPart Two: "
			(number->string (score-graph g score-trailhead-distinct))))
