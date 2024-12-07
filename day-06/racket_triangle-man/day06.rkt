#lang racket

(require "grid.rkt")

(struct guard (pos dir) #:transparent)

(module+ main

  (define *the-map*
    (call-with-input-file "input.txt" read-puzzle-input))  

  ;; Find the guard
  (define *the-guard*
    (guard (grid-member *the-map* #\^) '(-1 . 0)))

  ;; Replace the guard with floor
  (grid-set! *the-map* (guard-pos *the-guard*) #\.)

  ;; Part 1
  
  ;; Run the guard progamme
  (define *path-of-guard*
    (remove-duplicates
     (unfold
      (compose1 (curry escaped? *the-map*) guard-pos) ; Test for done
      guard-pos                                       ; What to return each time
      (curry guard-take-step *the-map*)               ; Function to take next step
      *the-guard*                                     ; Starting position and direction
      )))

  (length *path-of-guard*)

  ;; Part 2
  ;; Valid locations to put an obstacle are anywhere the guard would have walked, excluding the start. 

  (length
   (filter
    (curry infinite-loop? *the-map* *the-guard*) (remove (guard-pos *the-guard*) *path-of-guard*)))

  
)

;; ------------------------------------------------------------------------------------------

;; Read input as a grid.
;; Position (r . c) is r rows down, c columns across
(define (read-puzzle-input p)
  (lists->grid
   (map string->list
        (string-split (port->string p)))))

;; North     East     South    West
;; (-1 . 0)  (0 . 1)  (1 . 0)  (0 . -1)

(define (turn-right g)
  (match-let ([(cons s e) (guard-dir g)])
    (struct-copy guard g [dir (cons e (- s))])))

(define (turn-right/2 d)
  (match-let ([(cons s e) d])
    (cons e (- s))))

;; Is position pos outside the grid?
(define (escaped? grid pos)
  (not (grid-pos-inside? grid pos)))
  
;; One step of the guard : returns next position. (Part 1 only)
(define (guard-take-step floorplan gd)
  (let ([pos (guard-pos gd)]
        [dir (guard-dir gd)])
    (let ([next-pos (pos+ pos dir)])
      (if (or (escaped? floorplan next-pos)
              (char=? (grid-ref floorplan next-pos) #\.))
          (struct-copy guard gd [pos next-pos])
          (guard-take-step floorplan (turn-right gd)))))) ; let's hope there is a good diretion!

;; Does this path infinite loop? 
(define (infinite-loop? floorplan gd extra-obstacle)
  (let loop ([this-pos (guard-pos gd)]
             [this-dir (guard-dir gd)]
             [previous-states '()])
    ;; (displayln (format "At ~a heading ~a. Previous: ~a" this-pos this-dir previous-states))
    (if (member (cons this-pos this-dir) previous-states)
        #t                                                    ; we've been here before!
        (let ([maybe-next-pos (pos+ this-pos this-dir)])
          (if (escaped? floorplan maybe-next-pos)
              #f                                              ; escaped -- no infinite loop
              (if (or (char=? (grid-ref floorplan maybe-next-pos) #\#)
                      (equal? extra-obstacle maybe-next-pos))
                  (loop this-pos (turn-right/2 this-dir) (cons (cons this-pos this-dir) previous-states))
                  (loop maybe-next-pos this-dir previous-states)))))))


;; Useful for iteration

(define (unfold pred? f next seed)
  (let loop ([seed seed]
             [xs   '()])
    (if (pred? seed)
        xs
        (loop (next seed) (cons (f seed) xs)))))

;; ------------------------------------------------------------------------------------------

(module+ test

  (define *input* #<<END
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
END
    )

  (define *the-map*
    (call-with-input-string *input* read-puzzle-input))  

  ;; Find the guard
  (define *the-guard*
    (guard (grid-member *the-map* #\^) '(-1 . 0)))

  ;; Replace the guard with floor
  (grid-set! *the-map* (guard-pos *the-guard*) #\.)

  ;; Part 1
  
  ;; Run the guard progamme
  (define *path-of-guard*
    (remove-duplicates
     (unfold
      (compose1 (curry escaped? *the-map*) guard-pos)
      guard-pos
      (curry guard-take-step *the-map*)
      *the-guard*
      )))

  (length *path-of-guard*)

  ;; Part 2
  ;; Valid locations to put an obstacle are anywhere the guard would have walked, excluding the start. 

  (length
   (filter
    (curry infinite-loop? *the-map* *the-guard*) (remove (guard-pos *the-guard*) *path-of-guard*)))
  
  )
