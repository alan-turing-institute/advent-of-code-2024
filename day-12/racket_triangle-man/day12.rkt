#lang racket

(require "grid.rkt")

(module+ main

  (define *eg* #<<END
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
END
)

(define *garden*
  (lists->grid
   (map string->list
        (call-with-input-file "input.txt" port->lines))))

;; Part 1

(define *canvas* (grid-map (const #f) *garden*))

(for*/sum ([r (range (grid-nrows *garden*))]
           [c (range (grid-ncols *garden*))])
  (let ([pos (cons r c)])
    (if (not (grid-ref *canvas* pos))
        (let-values ([(lbl area perimeter) (flood-into! *canvas* *garden* pos)])
          (* area perimeter))
        0)))

  
  )

;; ------------------------------------------------------------------------------------------

(define (show-grid g)
  (for ([ln (grid->lists g)])
    (displayln ln)))

;; Update canvas with the results of flood-filling g, starting at start-pos.
;; canvas should be a grid of the same shape as g, containing either:
;; - #f, if we have not filled this node
;; - A unique identifier of the region, if we have filled the region
;;
;; Returns (values label area perimeter) for the region
;;
;; Modifies canvas

(define (flood-into! canvas g start-pos)

  ;; same-label? : is this position labelled the same as start-pos?
  (define same-label?
    (let ([the-label (grid-ref g start-pos)])
      (λ (pos) 
        (equal? (grid-ref g pos) the-label))))

  ;; Mark pos as visited
  (define (visit! pos)
    (grid-set! canvas pos start-pos))
  
  ;; visited? : have we visited this position?
  (define (visited? pos)
    (equal? (grid-ref canvas pos) start-pos))

  ;; Mark the starting position as visited
  (visit! start-pos)
  
  (define-values (area perimeter)
    (let fill-loop ([frontier  (list start-pos)]
                    [area      0]
                    [perimeter 0])
      (if (null? frontier)
          (values area perimeter)
          (let* ([next-pos  (car frontier)]
                 [nbrs      (grid-adjacents g next-pos)] ; all neighbours not out of bounds
                 [reg       (filter same-label? nbrs)]   ; exclude different labels
                 [new-posns (filter (compose not visited?) reg)]) ; exclude already visited
            (begin
              (for ([p new-posns]) (visit! p)) ; Mark the new list as visited
              ;; (displayln (format "Adding ~a" next-pos))
              (fill-loop (append new-posns (cdr frontier))
                         (+ area 1)                ; One for this position
                         (+ perimeter (- 4 (length reg)))))))))

  (values (grid-ref g start-pos) area perimeter))
