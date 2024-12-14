#lang racket

(require "grid.rkt")

(module+ main
  (define *robots*
    (call-with-input-file "input.txt" read-puzzle-input))

  ;; Part 1
  
  (safety-factor
   (map (curry move-robot 100 101 103) *robots*) 101 103)

  ;; Part 2 -- look in this list for the minimum!
  ;; ("density" was a misnomer: it is smaller for denser arrangements.)
  
  (for/fold ([mini #f]
             [mind 10000000])
            ([i (in-range 10000)])
    (let* ([new (map (curry move-robot i 101 103) *robots*)]
           [d (density new)])
      (if (< d mind)
          (begin
            (displayln (format "~a: ~a" i d))
            (values i d))
          (values mini mind))))
  

  )


;; ------------------------------------------------------------------------------------------

(define (read-robot s)
  (let* ([parsed
          (regexp-match #px"p=([[:digit:]]+),([[:digit:]]+) v=(-?[[:digit:]]+),(-?[[:digit:]]+)" s)]
         [coords (map string->number (cdr parsed))])
    (cons (cons (first coords) (second coords))
          (cons (third coords) (fourth coords)))))

(define (read-puzzle-input p)
  (map read-robot (port->lines p)))

(define (move-robot steps width height robot)
  (match-let ([(cons (cons x y) (cons vx vy)) robot])
    (cons
     (cons
      (modulo (+ x (* steps vx)) width)
      (modulo (+ y (* steps vy)) height))
     (cons vx vy))))

(define ((quadrant-of width height) coord)
    (let ([midx (quotient (- width 1) 2)]
          [midy (quotient (- height 1) 2)])
      (match-let ([(cons x y) coord])
        (cond
          [(< y midy)
           (cond
             [(< x midx) 0]
             [(> x midx) 1]
             [else #f])]
          [(> y midy)
           (cond
             [(< x midx) 2]
             [(> x midx) 3]
             [else #f])]
          [else #f]))))

(define (safety-factor robots width height)
  (define quadrant (quadrant-of width height))
  (define counts (make-vector 4 0))
  (for ([robot robots])
    (let ([q (quadrant (car robot))])
      (when q
        (vector-set! counts q (+ (vector-ref counts q) 1)))))
  (apply * (vector->list counts)))

(define (density robots)
  (for/sum ([r1r2 (in-combinations robots 2)])
    (match-let ([(list (cons (cons x1 y1) _) (cons (cons x2 y2) _)) r1r2])
      (+ (abs (- x2 x1))
         (abs (- y2 y1))))))

;; Visualisation utilities

(define (count->symbol n)
  (cond
    [(zero? n) #\.]
    [(equal? 1 n) #\*]
    [else #\O]))

(define (show-robots/step robots steps width height)
  (show-robots (map (curry move-robot steps width height) robots) width height))

(define (show-robots robots width height)
  (define g (make-grid height width 0))
  (for ([robot robots])
    (match-let ([(cons (cons x y) _) robot])
      (grid-set! g (cons y x) (+ 1 (grid-ref g (cons y x))))))
  (for ([ln (grid->lists (grid-map count->symbol g))])
    (displayln (list->string ln))))

(define (show-grid g)
  (for ([ln (grid->lists g)])
    (displayln ln)))


;; ------------------------------------------------------------------------------------------

(module+ test

  (define *eg* #<<END
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
END
    )

  (define *robots*
    (call-with-input-string *eg* read-puzzle-input))

  
  (safety-factor
   (map (curry move-robot 100 11 7) *robots*) 11 7)
  
  )


