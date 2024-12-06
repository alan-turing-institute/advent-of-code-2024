;;; Lot's of imperative code :: TODO Complete functional refactor (zipper?)

(use-modules (ice-9 arrays)
	     (ice-9 textual-ports))

(define-values (LEFT RIGHT UP DOWN) (values '(0 -1) '(0 1) '(-1 0) '(1 0)))

;;; Helper Functions ---------------------------------------------------------------------

(define (string->array str)
  (list->array 2 (map string->list (string-split str #\newline))))

(define (add-pair p1 p2)
  (map (lambda (x y) (+ x y)) p1 p2))

(define (out-of-bounds? grid pos)
  (not (array-in-bounds? grid (car pos) (cadr pos))))

(define (obstacle? grid pos)
  (equal? #\# (array-ref grid (car pos) (cadr pos))))

(define (traversed? grid pos)
  (equal? #\X (array-ref grid (car pos) (cadr pos))))

(define (rotate-90 dir)
  (cond
   ((equal? dir LEFT) UP)
   ((equal? dir UP) RIGHT)
   ((equal? dir RIGHT) DOWN)
   ((equal? dir DOWN) LEFT)))

;;; Part One -----------------------------------------------------------------------------

(define (find-path grid pos dir steps)
  (define return (array-copy grid))
  (array-set! return #\X (car pos) (cadr pos))
  (let ((next_pos (add-pair pos dir)))
    (cond
     ((out-of-bounds? grid next_pos) (list steps grid))
     ((obstacle? grid next_pos) (find-path grid pos (rotate-90 dir) steps))
     (else (find-path return next_pos dir (if (traversed? grid pos) steps (+ 1 steps)))))))

(define (find-guard grid)
  (define guard_pos '(0 0))
  (let ((width (cadr (array-dimensions grid))) (height (car (array-dimensions grid))))
    (for-each (lambda (x) (for-each (lambda (y)
				      (if (equal? #\^ (array-ref grid x y)) (set! guard_pos (list x y))))
				    (iota height))) (iota width)))
  guard_pos)

(define grid (string->array (get-string-all (open-input-file "input"))))
(define guard_pos (find-guard grid))
(define steps_and_path (find-path grid guard_pos UP 1))

(display (string-append "Part One: "
			(number->string (car steps_and_path))))

;;; Part Two -----------------------------------------------------------------------------

;; For each traversed tile in the grid, place an obstacle and see if an infinite loop is run into

(define (infinite? grid pos dir old_states)
  (define current_state (append dir pos))
  (cond
   ((not (eq? #f (member current_state old_states))) #t)
   (else
    (let ((next_pos (add-pair pos dir)))
      (cond
       ((out-of-bounds? grid next_pos) #f)
       ((obstacle? grid next_pos) (infinite? grid pos (rotate-90 dir) (append (list current_state) old_states)))
       (else (infinite? grid next_pos dir old_states)))))))

(define path (cadr steps_and_path))

(define (make-pos-list grid)
  (define pos_list '())
  (let ((width (cadr (array-dimensions grid))) (height (car (array-dimensions grid))))
    (for-each (lambda (x) (for-each (lambda (y)
				      (if (equal? #\X (array-ref grid x y) ) (set! pos_list (cons (list x y) pos_list)))
				      ) (iota height))) (iota width)))
  pos_list)

(define (create-grid-with-pos grid pos)
  (define return (array-copy grid))
  (array-set! return #\# (car pos) (cadr pos))
  return)

;;; Takes ~30s :(
(display (string-append "\nPart Two: "
			(number->string (apply + (map (lambda (x) (if x 1 0))
						      (map (lambda (pos)
							     (infinite? (create-grid-with-pos grid pos) guard_pos UP '())
							     ) (make-pos-list path)))))))



