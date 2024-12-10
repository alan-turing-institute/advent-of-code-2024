#lang racket

(require "grid.rkt")

(module+ main

  (define *eg3* #<<END
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
END
    )

;; (define *map*
;;   (call-with-input-string *eg3* read-puzzle-input))

(define *map*
  (call-with-input-file "input.txt" read-puzzle-input))
  
(define *peaks*
  (grid-indexes-of *map* 9))

;; A signpost is a position, and a list of peaks reachable from this position;;
;; A gazetteer is a set of signposts
;;;; The initial gazetteer is just the peaks
(define *gazetteer*
  (map (λ (p) (cons p (list p))) *peaks*))

;; Part 1

(define *trailheads*
  (for/fold ([gazetteer *gazetteer*])
            ([_ (in-range 9)])
    (update-gazetteer-downhill *map* gazetteer)))

(define (score sps)
  (for/sum ([sp (in-list sps)])
    (length (signpost-peaks sp))))

(score *trailheads*)
  
)

;; port? -> grid?
(define (read-puzzle-input p)
  (lists->grid
   (for/list ([l (in-lines p)])
     (map (λ (c) (- (char->integer c) 48)) (string->list l)))))

;; eg, 1 -> #\1
(define (map-marker n)
  (integer->char (+ n 48)))

;; Visualise positions on a grid of char
(define (show-positions-on-map grid posns)
  (define g (make-grid (grid-nrows grid) (grid-ncols grid) #\.))
  (for ([pos (in-list posns)])
    (grid-set! g pos (map-marker (grid-ref grid pos))))
  (displayln
   (string-join (map list->string (grid->lists g)) "\n")))


;; Signposts
(define (signpost-posn sp) (car sp))
(define (signpost-peaks sp) (cdr sp))

;; All positions downhill by one from this one
(define (downhill-by-one grid pos)
  (filter (λ (p) (equal? (- (grid-ref grid pos) (grid-ref grid p)) 1))
          (filter (curry grid-pos-inside? grid)
                  (map (curry pos+ pos)
                       '((1 . 0) (0 . -1) (-1 . 0) (0 . 1)))))

  )

(define (unify-peaks sps)
  (cons (signpost-posn (car sps))
        (remove-duplicates (append-map signpost-peaks sps))))

;; Go downhill by one, amalgamating the list of peaks reachable from
;; each new position
(define (update-gazetteer-downhill grid gaz)
  (define (push-signpost-downhill sp)
    (map (λ (p) (cons p (signpost-peaks sp)))
         (downhill-by-one grid (signpost-posn sp))))
  (map unify-peaks
       (group-by signpost-posn
                 (append-map push-signpost-downhill gaz))))
