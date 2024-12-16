#lang racket

(require "grid.rkt")

(define (read-puzzle-input p)
  (let ([g (lists->grid
            (map string->list
                 (port->lines p)))])
    (let ([start (car (grid-indexes-of g #\S))]
          [end   (car (grid-indexes-of g #\E))])
      (grid-set! g start #\.)
      (grid-set! g end #\.)
      (values (locn start 0) end g))))

(define (show-puzzle g here end)
  (let ([g (grid-copy g)])
    (grid-set! g (:pos here) (hdg-sym (:hdg here)))
    (grid-set! g end #\E )
    (display (string-join (map list->string (grid->lists g)) "\n"))))

;; A locn is a position and a heading
;; heading is an integer, 0 = e, 1 = s, 2 = w, 3 = n

(struct locn (pos hdg) #:transparent)
(define :pos locn-pos)
(define :hdg locn-hdg)
(define (:x pos) (car pos))
(define (:y pos) (cdr pos))
(define (:px loc) (:x (:pos loc)))
(define (:py loc) (:y (:pos loc)))

(define heading-directions #('(0 . 1) '(1 . 0) '(0 . -1) '(-1 . 0)))
(define (hdg->dir h)
  (vector-ref heading-directions h))

(define heading-symbols #(#\> #\v #\< #\^))
(define (hdg-sym h)
  (vector-ref heading-symbols h))

;; The cost grid is four copies of the grid, one for each cardinal direction
;; Initially #f, will contain the current minimum cost to each point
(define (initialise-cost-grid g)
  (vector (grid-map (const #f) g)
          (grid-map (const #f) g)
          (grid-map (const #f) g)
          (grid-map (const #f) g)))

(define (cost-set! cg locn cost)
  (grid-set! (vector-ref cg (:hdg locn)) (:pos locn) cost))

(define (cost-ref cg locn)
  (grid-ref (vector-ref cg (:hdg locn)) (:pos locn)))

;; pq is a list sorted non-decreasing
(define (pq-insert pq val)
  
  )



;; start is a locn, goal a pos
(define (find-min-cost g start goal)
  (define (cost-grid (initialise-cost-grid g)))
  (cost-set! cost-grid start 0)
  
  )

;;; ------------------------------------------------------------------------------------------

(module+ test
  (define *eg* #<<END
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
END
    )

  (define-values (*start* *end* *maze*)
    (call-with-input-string *eg* read-puzzle-input))

  (show-puzzle *maze* *start* *end*)


  
  )
