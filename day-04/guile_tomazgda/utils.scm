(define-module (utils)
  #:export (add-pair port->array word-search cross-search))

(use-modules (ice-9 arrays)
	     (ice-9 textual-ports))

;;; General ------------------------------------------------------------------------------

(define (add-pair p1 p2)
  (map (lambda (x y) (+ x y)) p1 p2))

(define (port->array port)
  (string->array (get-string-all port)))

(define (string->row_list str)
  (map string->list (string-split str #\newline)))

(define (string->array str) 
  (list->array 2 (string->row_list str)))

;;; Word Search -------------------------------------------------------------------------------

(define (check-word array key index dir)
  (if (eq? (apply (lambda (i j) (array-ref array i j)) index) (car key))
      (if (null? (cdr key)) 1
	  (let ((next-index (add-pair index dir)))
	    (if (array-in-bounds? array (car next-index) (car (cdr next-index)))
		(check-word array (cdr key) next-index dir) 0
		))) 0))

(define (word-search array key)
  (define directions '((1 0) (1 1) (0 1) (-1 1) (-1 0) (-1 -1) (0 -1) (1 -1)))
  (define return_array (array-copy array))
  (array-index-map! return_array (lambda (i j)
				   (apply + (map (lambda (dir) (check-word array (string->list key) (list i j) dir)) directions))))
  (apply + (map (lambda (l) (apply + l)) (array->list return_array))))

;; Cross Search (Ugly implementation)  ---------------------------------------------------

(define (check-letter array index)
  (define letter (apply (lambda (i j) (array-ref array i j)) index))
  (if (or (equal? #\M letter) (equal? #\S letter)) letter 0))

(define (cross-search array)
  (define directions '((-1 -1) (1 1) (-1 1) (1 -1)))
  (define return_array (array-copy array))
  (array-index-map! return_array (lambda (i j)
				   (if (eq? #\A (array-ref array i j))
				       (begin
					 (let ((pattern (map (lambda (dir)
							       (if (apply (lambda (i j) (array-in-bounds? array i j)) (add-pair dir (list i j)))
								   (check-letter array (add-pair dir (list i j)))
								   0
								   )) directions)))
					   (if (or (equal? pattern '(#\M #\S #\M #\S))
						   (equal? pattern '(#\S #\M #\M #\S))
						   (equal? pattern '(#\M #\S #\S #\M))
						   (equal? pattern '(#\S #\M #\S #\M))
						   ) 1 0)))
				       0)))
  (apply + (map (lambda (l) (apply + l)) (array->list return_array))))

