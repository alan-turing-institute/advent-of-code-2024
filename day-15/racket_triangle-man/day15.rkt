#lang racket

(require "grid.rkt")

(module+ main
  
  (define-values (*robot* *warehouse* *moves*)
    (call-with-input-file "input.txt" read-puzzle-input))

  ;; Part 1
  
  (define *robot-final*
    (follow-moves! *warehouse* *robot* *moves*))

  (part1-answer *warehouse*)
  )

;;; ------------------------------------------------------------------------------------------

(define (read-warehouse s)
  (let* ([grid (lists->grid (map string->list (string-split s "\n")))]
         [pos (car (grid-indexes-of grid #\@))])
    (grid-set! grid pos #\.)
    (values grid pos)))

(define (read-moves s)
  (filter (λ (c) (not (char=? #\newline c)))
          (string->list s)))

(define (read-puzzle-input p)
  (let ([input (string-split (port->string p) "\n\n")])
    (let-values ([(warehouse robot) (read-warehouse (car input))])
      (values robot warehouse (read-moves (cadr input))))))

;; Part 2 versions

(define (double-up c)
  (match c
    [#\. '(#\. #\.)]
    [#\@ '(#\@ #\.)]
    [#\# '(#\# #\#)]
    [#\O '(#\[ #\])]))

(define (read-warehouse/2 s)
  (let* ([grid
          (lists->grid
           (map (λ (cs) (append-map double-up (string->list cs)))
                (string-split s "\n")))]
         [pos (car (grid-indexes-of grid #\@))])
    (grid-set! grid pos #\.)
    (values grid pos)))

(define (read-puzzle-input/2 p)
  (let ([input (string-split (port->string p) "\n\n")])
    (let-values ([(warehouse robot) (read-warehouse/2 (car input))])
      (values robot warehouse (read-moves (cadr input))))))

;;; Utility functions for display

(define (show-puzzle robot warehouse)
  (let ([g (grid-copy warehouse)])
    (grid-set! g robot #\@)
    (display (string-join (map list->string (grid->lists g)) "\n"))))

;;; Dynamics

(define (direction-of c)
  (match c
   [#\^ '(-1 . 0)]
   [#\> '(0 . 1)]
   [#\v '(1 . 0)]
   [#\< '(0 . -1)]))

;; look-in-dir
;; Returns
;; - the location of the first position in direction dir that is empty
;;   including this position
;; - or #f
(define (look-in-dir g pos dir)
  (match (grid-ref g pos)
    [#\. pos]                                ; found it
    [#\# #f]                                 ; hit a wall!
    [#\O (look-in-dir g (pos+ pos dir) dir)] ; keep looking
    ))

;; Move robot once in direction move
;; Updates warehouse
;; Returns new position
(define (step-robot! warehouse robot move)
  (let* ([dir  (direction-of move)]
         [next (pos+ robot dir)]
         [maybe-empty-pos (look-in-dir warehouse next dir)])
    (cond
      [(not maybe-empty-pos) robot] ; blocked
      [(equal? next maybe-empty-pos) next] ; move into empty space
      [else 
       (begin ; move the O at the front to the . at the back
         (grid-set! warehouse maybe-empty-pos #\O)
         (grid-set! warehouse next #\.)
         next)])))

(define (follow-moves! warehouse robot moves)
  (for/fold ([robot robot])
            ([move (in-list moves)])
    (step-robot! warehouse robot move)))

(define (part1-answer g)
  (let ([boxes (grid-indexes-of g #\O)])
    (apply +
           (map (λ (pos) (+ (* 100 (car pos)) (cdr pos)))
                boxes))))

;; Part 2

;; posns (a set)  must include all "sideways" connections
(define (extend-force-linkages/vertical acc g posns dir)
  (let* ([nexts (map (curry pos+ dir) posns)]
         [extras (filter-map (λ (p) 
                               (match (grid-ref g p)
                                 [#\[ (pos+ p '(0 . 1))]
                                 [#\] (pos+ p '(0 . -1))]
                                 [_ #f])) nexts)]
         [nexts* (remove-duplicates (append nexts extras))])
    (cond
      [(not (null? (filter (λ (p) (char=? (grid-ref g p) #\#))
                           nexts*)))
       #f] ; At least one box is blocked.
      [(null? (filter (λ (p) (not (char=? (grid-ref g p) #\.)))
                      nexts*))
       acc] ; All the next spaces are empty
      [else
       (extend-force-linkages/vertical (cons nexts* acc) g nexts* dir)]
      )))

(define (extend-force-linkages/horizontal acc g pos dir)
  (let ([next (pos+ pos dir)])
    (match (grid-ref g next)
      [#\. acc]
      [#\[ (extend-force-linkages/horizontal (cons (list next) acc) g next dir)]
      [#\] (extend-force-linkages/horizontal (cons (list next) acc) g next dir)]
      [#\# #f])))


;; Given a position and a direction returns either
;;
;; - #f, if moving blocks in this direction eventually blocks, or
;;
;; - a list of sets of positions, such that the positions in each set
;; are in a line perpendicular to the direction, and the sets
;; themselves are ordered from the furthest from to the nearest to pos

(define (force-linkages g pos dir)
  (if (zero? (car dir))
      (extend-force-linkages/horizontal '() g pos dir)
      (extend-force-linkages/vertical '() g (list pos) dir)))

(define (move-block! g block dir)
  (for ([line (in-list block)])
    (for ([p (in-list line)])
      (grid-set! g (pos+ p dir) (grid-ref g p))
      (grid-set! g p #\.))))

(define (step-robot/2! warehouse robot move)
    (let* ([dir (direction-of move)]
         [maybe-block (force-linkages warehouse robot dir)])
    (if (not maybe-block)
        robot
        (begin
          (move-block! warehouse maybe-block dir)
          (pos+ robot dir)))))

(define (follow-moves/2! warehouse robot moves)
  (for/fold ([robot robot])
            ([move (in-list moves)])
    ;; (show-puzzle robot warehouse)
    ;; (displayln "")
    ;; (displayln move)
    ;; (read)
    (step-robot/2! warehouse robot move)))


;;; ------------------------------------------------------------------------------------------

(module+ test
  
  (define *eg* #<<END
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
END
    )
  
  ;; Part 1

  (define-values (*robot* *warehouse* *moves*)
    (call-with-input-string *eg* read-puzzle-input))
  
  (define *robot-final*
    (follow-moves! *warehouse* *robot* *moves*))

  (part1-answer *warehouse*)

  ;; Part 2

  (define *eg/2* #<<END
#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^
END
)
  
  (define-values (*robot/2* *warehouse/2* *moves/2*)
    (call-with-input-string *eg* read-puzzle-input/2))
  
  
  )
