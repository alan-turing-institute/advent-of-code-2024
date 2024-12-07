#lang racket

(module+ main

  (define *eqns*
    (call-with-input-file "input.txt" read-puzzle-input))

  ;; Part 1
  
  (define *soluble-eqns/1*
    (filter
     (λ (eqn) (soluble? (car eqn) (cdr eqn) (list + *)))
     *eqns*))

  (apply + (map car *soluble-eqns/1*))

  ;; Part 2
  
  (define *soluble-eqns/2*
    (filter
     (λ (eqn) (soluble? (car eqn) (cdr eqn) (list + * ||)))
     *eqns*))

  (apply + (map car *soluble-eqns/2*))
  
  )

;; ------------------------------------------------------------------------------------------

(define (read-puzzle-input p)
  (map
   (λ (line)
     (let ([tmp (string-split line ": ")])
       (cons (string->number (car tmp))
             (map string->number (string-split (cadr tmp))))))
   (sequence->list (in-lines p))))

;; Concatenation operator
(define (|| a b)
  (+ (* a 10 (expt 10 (order-of-magnitude b)))
     b))

;; Is this equation soluble? 
(define (soluble? ans ns ops)
  (for/or ([ops (apply cartesian-product (repeat (- (length ns) 1) ops))])
    (equal? ans (eval-equation ns ops))))

;; Build a list of length n consisting of v
(define (repeat n v)
  (build-list n (const v)))

;; ns -- a list of numbers
;; ops -- a list of binary operators, one fewer the the count of the numbers
(define (eval-equation ns ops)
  (foldl
   (λ (n op total)
     (op total n))
   (car ns)
   (cdr ns)
   ops))


;; ------------------------------------------------------------------------------------------

(module+ test

  (define *input* #<<END
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
END
    )

  (define *eqns*
    (call-with-input-string *input* read-puzzle-input))

  ;; Part 1
  
  (define *soluble-eqns/1*
    (filter
     (λ (eqn) (soluble? (car eqn) (cdr eqn) (list + *)))
     *eqns*))

  (apply + (map car *soluble-eqns/1*))

  ;; Part 2
  
  (define *soluble-eqns/2*
    (filter
     (λ (eqn) (soluble? (car eqn) (cdr eqn) (list + * ||)))
     *eqns*))

  (apply + (map car *soluble-eqns/2*))
  
  )
