#lang racket

(require "grid.rkt")

(module+ main
  (define-values (*start* *end* *maze*)
    (call-with-input-file "input.txt" read-puzzle-input))

  ;; Part 1

  ;; Minimum cost to end up and end heading in any direction
  (find-min-cost *maze* *start* *end*)

  
  
  )




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

(define heading-directions #((0 . 1) (1 . 0) (0 . -1) (-1 . 0)))
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

;; Poor man's priority queue: insert a value into its place in a non-decreasing list
(define (pq-insert pq val <:)
   (let loop ([acc '()]
              [xs  pq])
     (cond
       [(null? xs)        (reverse (cons val acc))]
       [(<: val (car xs)) (append (reverse acc) (cons val xs))]
       [else              (loop (cons (car xs) acc) (cdr xs))])))

(define (pq-insert-all pq vals <:)
  (for/fold ([pq pq])
            ([val vals])
    (pq-insert pq val <:))
  )


(define (cost< f1 f2)
  (< (cdr f1) (cdr f2)))

(define (not-wall? g pos)
  (not (char=? (grid-ref g pos) #\#)))

;; The neighbours of here, that are not wall, and their costs from here
(define (neighbours-of g here)
  (let ([pos (:pos (car here))]
        [hdg (:hdg (car here))]
        [cst (cdr here)])
    (let ([ahead (pos+ pos (hdg->dir hdg))]
          [turned (map (λ (δh δc) (cons (locn pos (modulo (+ hdg δh) 4)) (+ cst δc)))
                       '(1 3)
                       '(1000 1000))])
      (if (not-wall? g ahead)
          (cons (cons (locn ahead hdg) (+ cst 1))
                turned)
          turned))))
    
    
;; Fill out the entire grid -- TODO: early stopping!
;; - frontier is a list of (locn . cost) to search next,
;;   sorted non-decreasing by cost
;; - cg is the tentative minimum cost found so far, or #f if univisited
;; - mutates cg
(define (find-min-cost/recur! g cg frontier)
  ;; If the frontier is empty, we are done
  (if (null? frontier)
      cg
      ;; 1. Pick the next cheapest cell off the frontier and find its neighbours
      ;;    together with the cost to get to each neighbour
      (let* ([here     (car frontier)]
             [frontier (cdr frontier)]
             [yon      (neighbours-of g here)])
        ;; For each element in yon:
        ;; - if it is no cheaper than the minimum so far, take it off the list
        ;; - if it is cheaper than the minimum found so far,
        ;;   replace the minimum so far, and push it back on the frontier
        (let ([new-frontier 
               (filter-map
                (λ (l)
                  (let ([min-cost-so-far (cost-ref cg (car l))]
                        [cost-of-this (cdr l)])
                    (if (or (not min-cost-so-far) (< cost-of-this min-cost-so-far))
                        (begin
                          (cost-set! cg (car l) cost-of-this)
                          l)
                        #f)))
                yon)])
          (find-min-cost/recur! g cg (pq-insert-all frontier new-frontier cost<))))))

;; start is a locn, goal a pos. Return cost grid
(define (find-min-cost g start)
  (define cost-grid (initialise-cost-grid g))
  (cost-set! cost-grid start 0)
  (find-min-cost/recur! g cost-grid `((,start . 0))))

(define (where-min cost-grid goal)
  (let* ([ends
          (map (λ (hdg) (cost-ref cost-grid (locn goal hdg)))
               '(0 1 2 3))]
         [minimum
          (apply min ends)]
         [minimiser (index-of ends minimum)])
    (values minimum minimiser)))


;; For part 2
(define (follow-the-yellow-brick-road g cg here)
  (let loop ([xs (list (car here))]
             [frontier (list here)])
    (if (null? frontier)
        xs
        (let ([new-frontier
               (append-map (λ (f) 
                             (let* ([loc (car f)]
                                    [cst (cost-ref cg loc)]
                                    [nbrs (neighbours-of g (cons loc 0))])
                               (filter (λ (x)
                                         (equal? cst (+ (cdr x) (cost-ref cg (car x)))))
                                       nbrs)))
                           frontier)])
          (loop (append new-frontier xs) new-frontier)
          ))))


;;; ------------------------------------------------------------------------------------------

(module+ test
  (define *eg1* #<<END
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

  (define *eg2* #<<END
#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################
END
    )

  (define-values (*start1* *end1* *maze1*)
    (call-with-input-string *eg1* read-puzzle-input))

  (define-values (*start2* *end2* *maze2*)
    (call-with-input-string *eg2* read-puzzle-input))
  
  ;; Part 1
  
  (define ans1 (find-min-cost *maze1* *start1*))
  (define-values (min1 hdg1) (where-min ans1 *end1*))
  min1
  
  (define ans2 (find-min-cost *maze2* *start2*))
  (define-values (min2 hdg2) (where-min ans2 *end2*))
  min2

  ;; Part 2

  ;; Start at the end, heading the other way, and go to the beginning
  (define backwards-cost-grid1 (find-min-cost *maze1* (locn *end1* (modulo (+ hdg1 2) 4))))

  ;; Now start at the beginning again, mapping out the paths where the
  ;; difference in costs to the end is exactly the cost of this edge.
  (follow-the-yellow-brick-road *maze1* backwards-cost-grid1 *start1*)

  
  )
