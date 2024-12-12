#lang racket/base

;; TODO
;; - in-grid-positions (a sequence of all positions within a grid)

(require racket/vector)
(require racket/list)

;; Mutable 2d vectors

(provide pos+
         pos-
         (struct-out grid)
         make-grid
         grid-ref
         grid-set!
         grid-fill!
         grid-ncols
         grid-nrows
         grid-pos-inside?
         grid-adjacents
         grid-row
         grid->lists
         lists->grid
         grid-member
         grid-indexes-of
         grid-map
         grid-indexed-map
         )

;; A pos is a pair, (row . col)
(define (pos+ p1 p2)
  (cons
   (+ (car p1) (car p2))
   (+ (cdr p1) (cdr p2))))

(define (pos- p1 p2)
  (cons
   (- (car p1) (car p2))
   (- (cdr p1) (cdr p2))))

;; ------------------------------------------------------------

(struct grid (vec cols) #:transparent)

;; Converts an index in vec to a grid posn
(define (vec-ref-to-posn n ncols)
  (let-values ([(r c) (quotient/remainder n ncols)])
    (cons r c)))

;; Make an m (rows) x n (cols) grid
(define (make-grid rows cols v)
  (grid (make-vector (* rows cols) v) cols))

;; A position is a pair, (row . col)
;; Note that col changes fastest when accessing vec in order
(define (grid-ref g pos)
  (vector-ref (grid-vec g) (+ (cdr pos) (* (car pos) (grid-cols g)))))

(define (grid-set! g pos v)
  (vector-set! (grid-vec g) (+ (cdr pos) (* (car pos) (grid-cols g))) v))

(define (grid-fill! g v)
  (vector-fill! (grid-vec g) v))

(define (grid-ncols g)
  (grid-cols g))

(define (grid-nrows g)
  (/ (vector-length (grid-vec g)) (grid-cols g)))

;; Is pos inside g?
;; Returns pos if pos is inside g
(define (grid-pos-inside? g pos)
  (let ([x (car pos)]
        [y (cdr pos)])
    (and (>= x 0)
         (< x (grid-nrows g))
         (>= y 0)
         (< y (grid-ncols g))
         pos)))

;; Find adjacent locations
(define (grid-adjacents g pos)
  (filter-map
   (λ (p) (grid-pos-inside? g (pos+ pos p)))
   ;; n e s w  
   '((-1 . 0) (0 . 1) (1 . 0) (0 . -1))))

;; Return row r from the grid
(define (grid-row g row)
  (let ([vec (grid-vec g)]
        [ncs (grid-ncols g)])
    (vector-take
     (vector-drop vec (* row ncs))
     ncs)))

;; Return the first position of v in g, in a search that is
;; "Western reading direction"
(define (grid-member g v)
  (let ([vpos (vector-member v (grid-vec g))])
    (call-with-values (λ () (quotient/remainder vpos (grid-cols g))) cons)))

(define (grid->lists g)
  (for/list ([r (grid-nrows g)])
    (for/list ([c (grid-ncols g)])
      (grid-ref g `(,r . ,c)))))

;; xss is a non-empty list of non-empty lists
(define (lists->grid xss)
  (let ([vec (apply vector-append (map list->vector xss))])
    (grid vec (length (car xss)))))

;; Return a list of positions where v occurs
(define (grid-indexes-of g v)
  (for*/list ([r (grid-nrows g)]
              [c (grid-ncols g)]
              #:when (equal? (grid-ref g `(,r . ,c)) v)
              )
    (cons r c)))
             
;; Like vector-map
(define (grid-map proc g)
  (grid (vector-map proc (grid-vec g)) (grid-cols g)))

;; proc should be a function of two arguments, a posn and a current
;; value
(define (grid-indexed-map proc g)
  (let ([vec   (grid-vec g)]
        [ncols (grid-ncols g)])
    (grid
     (build-vector (vector-length vec)
                   (λ (n) (proc (vec-ref-to-posn n ncols) (vector-ref vec n))))
     ncols)))
