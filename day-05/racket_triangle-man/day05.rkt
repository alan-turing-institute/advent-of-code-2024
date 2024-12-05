#lang racket

(module+ main

  (define-values (the-order the-updates) 
    (call-with-input-file "input.txt" read-puzzle-input))

  ;; Part 1
  
  (apply +
         (map string->number
              (map list-middle-value
                   (filter (curry correctly-ordered? the-order) the-updates))))

  ;; Part 2
  
  (define page<?
    (make-order-comparator the-order))

  (define *sorted-updates*
    (map (curryr sort page<?)
         (filter (λ (pgs) (not (correctly-ordered? the-order pgs))) the-updates)))
  
  (apply +
         (map string->number
              (map list-middle-value
                  *sorted-updates*)))
  
  )

;; ------------------------------------------------------------------------------------------

(define (read-puzzle-input p)
  (let ([in (string-split (port->string p) "\n\n")])
    (let ([the-order (map (λ (s) (string-split s "|")) (string-split (car in)))]
          [the-updates (map (λ (s) (string-split s ",")) (string-split (cadr in)))])
      (values the-order the-updates))))

;; Is every rule in `rules` satisfied in `update`?
(define (correctly-ordered? rules update)
  (for/and ([rule (in-list rules)])
    (let ([m (index-of update (car rule))]
          [n (index-of update (cadr rule))])
      (or (not m) ; If the rule is not in the update, it is vacuously true
          (not n)
          (< m n)))))

(define (list-middle-value xs)
  (list-ref xs (quotient (- (length xs) 1) 2)))

(define (make-order-comparator rules)
  (let ([rule-set (list->set (map (λ (pr) (cons (car pr) (cadr pr))) rules))])
    (λ (m n)
      (set-member? rule-set (cons m n)))))

;; ------------------------------------------------------------------------------------------
;; Testing

(module+ test
  (define *input* #<<END
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
END
    )

  (define-values (the-order the-updates) 
    (call-with-input-string *input* read-puzzle-input))

  ;; Part 1
  (apply +
         (map string->number
              (map list-middle-value
                   (filter (curry correctly-ordered? the-order) the-updates))))

  ;; Part 2
  (define page<?
    (make-order-comparator the-order))

  (define *sorted-updates*
    (map (curryr sort page<?)
         (filter (λ (pgs) (not (correctly-ordered? the-order pgs))) the-updates)))
  
  (apply +
         (map string->number
              (map list-middle-value
                  *sorted-updates*)))
  )



