#lang racket

(require "grid.rkt")

(module+ main


  (define-values (*track* *start* *end*)
    (call-with-input-file "input.txt" read-puzzle-input))

  ;; Grid with 0 at end and total distance + 1 and start, otherwise #f
  (define *costs*
    (shortest-path *track* *start* *end*))

  (displayln (format "Distance from start to end: ~a"
                     (grid-ref *costs* *start*)))

  ;; Part 1
  
  (define *cheats*
    (filter values
            (for*/list ([row (in-range 1 (grid-nrows *costs*))]
                        [col (in-range 1 (grid-ncols *costs*))])
              (cheat-bonus *costs* `(,row . ,col))))
    )
  
  (count (curryr >= 100) *cheats*)

 ;; Part 2

  ;; Make a list of the path
  (define *path*
    (sort 
     (for*/list ([row (in-range 1 (grid-nrows *costs*))]
                 [col (in-range 1 (grid-ncols *costs*))]
                 #:when (grid-ref *costs* `(,row . ,col)))
       (cons `(,row . ,col) (grid-ref *costs* `(,row . ,col))))
     <
     #:key cdr
     ))

  (displayln (format "Path length: ~a" (length *path*)))
  
  (define *cheats/2* (find-all-cheats *path* 20))
  
  (count (λ (c) (>= (car c) 100)) *cheats/2*)
  
  )

;;; ------------------------------------------------------------------------------------------

(define (read-puzzle-input p)
  (define in
    (lists->grid (map string->list (port->lines p))))
  (define start
    (car (grid-indexes-of in #\S)))
  (define end
    (car (grid-indexes-of in #\E)))
  (grid-set! in start #\.)
  (grid-set! in end #\.)
  (values in start end))

;;; Stolen from Day 18

(define (shortest-path g start end)
  (let ([costg (grid-map (const #f) g)])
    (grid-set! costg end 0)
    (shortest-path-length/recur! g costg (list end) 1)))

(define (shortest-path-length/recur! g costg frontier steps)
  (if (null? frontier)
      costg
      (let ([new-frontier
             (remove-duplicates
              (append-map
               (λ (p)
                 (filter (conjoin (unvisited? costg) (empty-space? g))
                         (grid-adjacents g p)))
               frontier))])
        (for-each (λ (p) (grid-set! costg p steps)) new-frontier)
        (shortest-path-length/recur! g costg new-frontier (+ steps 1)))))

(define ((unvisited? g) p)
  (not (grid-ref g p)))

(define ((empty-space? g) p)
  (char=? (grid-ref g p) #\.))

(define (show-grid g)
  (for ([ln (in-list (grid->lists g))])
    (displayln (list->string ln))))

;;; Code for today's

;; grid is a cost grid
;; Returns #f if no cheat available here
(define (cheat-bonus grid pos)
  (and (not (grid-ref grid pos)) ; return #f if c is already on the shortest path
       (let ([dists (filter-map (curry grid-ref grid) (grid-adjacents grid pos))])
         ;; (displayln (format "cs: ~a" dists))
         (and (not (null? dists))
              (let ([cheat-dist (- (apply max dists) (apply min dists) 2)])
                (if (> cheat-dist 0)
                    cheat-dist
                    #f))))

       )

  )

;; (define (grid-pos-inside/no-sides? g pos)
;;   (let ([x (car pos)]
;;         [y (cdr pos)])
;;     (and (> x 0)
;;          (< x (- (grid-nrows g) 1))
;;          (> y 0)
;;          (< y (- (grid-ncols g) 1))
;;          pos)))

;; (define (grid-adjacents/no-sides g pos)
;;   (filter-map
;;    (λ (p) (grid-pos-inside/no-sides? g (pos+ pos p)))
;;    ;; n e s w  
;;    '((-1 . 0) (0 . 1) (1 . 0) (0 . -1))))

;; cheat-exits
;; If tick equals zero, or the frontier is empty, return 
;; Starting from here, if tick > 0, expand to neighbouring unvisited cells.
;; - if any new cell is a space, enter it on the return list, and don't consider it further
;; - otherwise, recurse with tick - 1

;; (define (cheat-exits/recur grid frontier tick visiteds returns)
;;   (if (or (zero? tick)
;;           (null? frontier))
;;       returns
;;       (let ([maybe-new-frontier
;;              (remove-duplicates
;;               (append-map
;;                (λ (p)
;;                  (filter (λ (p) (not (member p visiteds)))
;;                          (grid-adjacents grid p)))
;;                frontier))])
;;         (let-values ([(new-frontier to-return)
;;                       (partition (λ (p) (char=? (grid-ref grid p) #\#)) maybe-new-frontier)])
;;           (cheat-exits/recur grid
;;                              new-frontier
;;                              (- tick 1)
;;                              (append maybe-new-frontier visiteds)
;;                              (append (map (curryr cons (- tick 1)) to-return) returns))))))

;; (define (cheat-exits grid here tick)
;;   (cheat-exits/recur grid (list here) tick (list here) '()))

;; For each position in path,
;; Find all exists from cheating at most tick from here
;; Exclude those with no time savings
;; 
;; (define (find-all-cheats grid costg path ticks)
;;   (apply append
;;          (for/list ([p (in-list path)])
;;           (find-cheats-from grid costg p ticks))))

;; (define (find-cheats-from grid costg p ticks)
;;   (let* ([here (car p)]
;;          [start-dist (cdr p)]
;;          [cheats (cheat-exits grid here ticks)]
;;          [savings
;;           (map (λ (c) (cons (- (- start-dist (grid-ref costg (car c)))
;;                                (- ticks (cdr c)))
;;                             (cons here (car c))))
;;                         cheats)])
;;     ;; (displayln (format "cheats: ~a" cheats))
;;     ;; (displayln (format "savings ~a" savings))
;;     (filter (λ (s) (> (car s) 0)) savings)))

;; For each position in path,
;; Find all exists from cheating at most tick from here
;; Exclude those with no time savings

(define (find-all-cheats path ticks)
  (apply append
         (for/list ([pth (in-list path)])
          (find-cheats-from path pth ticks))))

(define (l1-dist pos1 pos2)
  (+ (abs (- (car pos1) (car pos2)))
     (abs (- (cdr pos1) (cdr pos2)))))

;; p1, p2 : (cons pos dist-to-end)
(define (successful-cheat p1 p2 ticks)
  (let* ([pos1 (car p1)]
         [pos2 (car p2)]
         [l1 (l1-dist pos1 pos2)])
    (and (<= l1 ticks)
         (let ([saving (- (cdr p1) (cdr p2) l1)])
           (and (> saving 0)
                (cons saving (cons pos1 pos2)))))))

(define (find-cheats-from path pth ticks)
  (let* ([here (car pth)]
         [start-dist (cdr pth)])
    (filter-map
     (λ (pth2) (successful-cheat pth pth2 ticks))
     path)))






;;; ------------------------------------------------------------------------------------------

(module+ test

  (define *eg* #<<END
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
END
    )

  (define-values (*track* *start* *end*)
    (call-with-input-string *eg* read-puzzle-input))

  ;; Grid with 0 at end and total distance + 1 and start, otherwise #f
  (define *costs*
    (shortest-path *track* *start* *end*))

  (define *cheats*
    (filter values
            (for*/list ([row (in-range 1 (grid-nrows *costs*))]
                        [col (in-range 1 (grid-ncols *costs*))])
              (cheat-bonus *costs* `(,row . ,col))))
    )
  
  ;; Part 2

  ;; Make a list of the path
  (define *path*
    (sort 
     (for*/list ([row (in-range 1 (grid-nrows *costs*))]
                 [col (in-range 1 (grid-ncols *costs*))]
                 #:when (grid-ref *costs* `(,row . ,col)))
       (cons `(,row . ,col) (grid-ref *costs* `(,row . ,col))))
     <
     #:key cdr
     ))

  (define *cheats/2* (find-all-cheats *path* 20))
  
  (map (λ (g) (cons (caar g) (length g))) (group-by car *cheats/2*))
  
  
  )
