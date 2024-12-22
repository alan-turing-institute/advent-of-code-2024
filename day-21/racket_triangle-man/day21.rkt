#lang racket

(module+ main

  ;; Part 1
  (complexity '("083A" "935A" "964A" "149A" "789A") 2)

  ;; Part 2
  (complexity '("083A" "935A" "964A" "149A" "789A") 25)

  )


(module+ test

  ;; Part 1
  (complexity '("029A" "980A" "179A" "456A" "379A") 2)

  )

;; ------------------------------------------------------------------------------------------

(define (swap pair)
  (cons (cdr pair) (car pair)))

(define NUMERIC-KEYPAD
  '((#\A . (3 . 2))
    (#\0 . (3 . 1))
    (#\1 . (2 . 0)) (#\2 . (2 . 1)) (#\3 . (2 . 2))
    (#\4 . (1 . 0)) (#\5 . (1 . 1)) (#\6 . (1 . 2))
    (#\7 . (0 . 0)) (#\8 . (0 . 1)) (#\9 . (0 . 2))))

(define NUMERIC-KEYPAD/LOOKUP
  (map swap NUMERIC-KEYPAD))

(define NUMERIC-KEYPAD-ILLEGAL
  '(3 . 0))

(define DIRECTIONAL-KEYPAD
  '((#\A . (0 . 2))
    (#\^ . (0 . 1))
    (#\< . (1 . 0))
    (#\v . (1 . 1))
    (#\> . (1 . 2))))

(define DIRECTIONAL-KEYPAD/LOOKUP
  (map swap DIRECTIONAL-KEYPAD))

(define DIRECTIONAL-KEYPAD-ILLEGAL
  '(0 . 0))

(define DIRECTIONS
  '((( 1 .  0) . #\v)
    (( 0 .  1) . #\>)
    ((-1 .  0) . #\^)
    (( 0 . -1) . #\<)
    (#\A       . #\A)))

;;; Utilities
;;; ---------

(define (cons-on-all v xs)
  (map (λ (x) (cons v x)) xs))

(define (add-to-all v xs)
  (map (λ (x) (append x (list v))) xs))

(define (pos+ p1 p2)
  (cons (+ (car p1) (car p2)) (+ (cdr p1) (cdr p2))))

(define (pos- p1 p2)
  (cons (- (car p1) (car p2)) (- (cdr p1) (cdr p2))))

;; Conversion between keypad and position

(define (char->pos/numeric char)
  (cdr (assoc char NUMERIC-KEYPAD)))
(define (char->pos*/numeric chars)
  (map char->pos/numeric chars))

(define (pos->char/numeric posn)
  (cdr (assoc posn NUMERIC-KEYPAD/LOOKUP)))
(define (pos->char*/numeric posns)
  (map pos->char/numeric posns))

(define (char->pos/directional char)
  (cdr (assoc char DIRECTIONAL-KEYPAD)))
(define (char->pos*/directional chars)
  (map char->pos/directional chars))

(define (pos->char/directional posn)
  (cdr (assoc posn DIRECTIONAL-KEYPAD/LOOKUP)))
(define (pos->char*/directional posns)
  (map pos->char/directional posns))

(define (δ->direction δ)
  (cdr (assoc δ DIRECTIONS)))
(define (δ->direction* δs)
  (map δ->direction δs))

;;; Routes
;;; ------

;; Returns a list of routes, where a route is a list of
;; instructions needed to move.
(define (a-r-b/recur δr r+ δc c+)
  (if (zero? δr)
      (if (zero? δc)
          '(())
          (cons-on-all (cons 0 c+) (a-r-b/recur δr r+ (- δc c+) c+)))
      (if (zero? δc)
          (cons-on-all (cons r+ 0) (a-r-b/recur (- δr r+) r+ δc c+))
          (append
           (cons-on-all (cons 0 c+) (a-r-b/recur δr r+ (- δc c+) c+))
           (cons-on-all (cons r+ 0) (a-r-b/recur (- δr r+) r+ δc c+))
           ))))

;; List of all legal routes from pos1 to pos2
(define (all-routes-between pos1 pos2 illegal)
  (let* ([δ (pos- pos2 pos1)]
         [δr (car δ)]
         [δc (cdr δ)]
         [r+ (sgn δr)]
         [c+ (sgn δc)])
    (let ([routes
           (a-r-b/recur δr r+ δc c+)])
      (filter-map (λ (route)
                    (and (legal-route? pos1 route illegal)
                         (δ->direction* route)))
                  routes))))

(define (legal-route? start route illegal)
  (not
   (ormap (λ (p) (equal? p illegal))
    (for/fold ([pos start]
               [acc '()]
               #:result acc)
              ([δ route])
      (let ([new-pos (pos+ pos δ)])
        (values new-pos (cons new-pos acc)))))))

;; Reusing memoise from day 11

(define-syntax-rule
  (define/memoise (fn x ...) body ...)
  (define fn
    (let ([lookup (make-hash)])
      (λ (x ...)
        (let* ([arg (list x ...)]
               [val (hash-ref lookup arg #f)])
          (if val
              val
              (let ([result body ...])
                (begin
                  (hash-set! lookup arg result)
                  result))))))))


;; NB: all routes necessarily start from A (because that's where they ended up last time) 
(define (shortest-route-length*/directional route depth)
  (let loop ([keys   (cons #\A route)]
             [total 0])
    (if (null? (cdr keys))
        total
        (let ([this-key (car keys)]
              [next-key (cadr keys)])
          (loop (cdr keys) (+ total (shortest-route-length/directional this-key next-key depth)))))))

;; What is the length of the shortest set of (ultimate) keypresses that will take you from
;; start to end on the directional keypad, including pressing A to input end?
;; depth = 0 means compute the keypresses on the next keypad that will move you on this one
(define/memoise (shortest-route-length/directional start end depth)
  (let ([routes
         (add-to-all #\A
                     (all-routes-between (char->pos/directional start) (char->pos/directional end) DIRECTIONAL-KEYPAD-ILLEGAL))])
    (if (zero? depth)
        (apply min (map length routes))
        (apply min (map (λ (route) (shortest-route-length*/directional route (- depth 1))) routes)))))


;; depth is the number of robot-controlled directional keypads
;; (one less than the total number of directional keypads)
(define (shortest-route-length*/numeric route depth)
  (let loop ([keys   (cons #\A route)]
             [total 0])
    (if (null? (cdr keys))
        total
        (let ([this-key (car keys)]
              [next-key (cadr keys)])
          (loop (cdr keys) (+ total (shortest-route-length/numeric this-key next-key depth)))))))

(define (shortest-route-length/numeric start end depth)
  (let ([routes
         (add-to-all #\A
                     (all-routes-between (char->pos/numeric start) (char->pos/numeric end) NUMERIC-KEYPAD-ILLEGAL))])
    (if (zero? depth)
        (apply min (map length routes))
        (apply min (map (λ (route) (shortest-route-length*/directional route (- depth 1))) routes)))))


(define (complexity codes depth)
  (for/sum ([code codes])
    (* (string->number (substring code 0 3))
       (shortest-route-length*/numeric (string->list code) depth))))


;;; Testing utilities
;;; -----------------

;; Given route to numeric keypad robot, emit digits
(define (use-numeric-keypad seq)
  (let loop ([pos (char->pos/numeric #\A)]
             [seq seq]
             [output '()])
    (if (null? seq)
        (reverse output)
        (match (car seq)
          [#\A (loop pos                  (cdr seq)
                     (cons (cdr (assoc pos NUMERIC-KEYPAD/LOOKUP)) output))]
          [#\^ (loop (pos+ pos '(-1 . 0)) (cdr seq) output)]
          [#\> (loop (pos+ pos '(0 . 1))  (cdr seq) output)]
          [#\v (loop (pos+ pos '(1 . 0))  (cdr seq) output)]
          [#\< (loop (pos+ pos '(0 . -1)) (cdr seq) output)]))))

