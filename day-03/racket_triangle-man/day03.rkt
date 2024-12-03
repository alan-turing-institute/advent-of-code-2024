#lang racket

(require rackunit)

(module+ main
  
  (define *input* (with-input-from-file "input.txt" port->string))
  
  ;; Part 1

  (apply +
         (map (curry apply *) 
              (part1-parser *input*)))
  
  ;; Part 2

  (execute-instructions
   (part2-parser *input*))
  )

;; ------------------------------------------------------------------------------------------

;; Match mul(9...,9...)
(define rx-part1 #px"mul\\(([[:digit:]]+),([[:digit:]]+)\\)")

;; Match either mul(9..,9..) or do() or don't()
(define rx-part2 #px"mul\\(([[:digit:]]+),([[:digit:]]+)\\)|do\\(\\)|don't\\(\\)")

;; Parse the input string as part 1
;; --------------------------------

;; -> a list of pairs of numbers
(define (part1-parser str)
  (map (curry map string->number)
       (regexp-match* rx-part1 str #:match-select cdr)))

;; Parse the input string as part 2
;; --------------------------------

;; Parse the input into a list of tokens
(define (part2-parser str)
  (let ([words (regexp-match* rx-part2 str #:match-select values)])
    (map tokenize words)))

;; Convert each element to a token. A token is either: 
;; - a number (the product, if a mul() was found)
;; - 'on (if a do() was found)
;; - 'off (if a (don't() was found)
(define (tokenize word)
  (match word
    [(list "do()" #f #f)    'on]
    [(list "don't()" #f #f) 'off]
    [(list _ (? string? m) (? string? n))
     (* (string->number m) (string->number n))]))

;; Process the list of tokens
(define (execute-instructions tokens)
  (for/fold ([total 0]
             [on?   #t]
             #:result total)
            ([tok (in-list tokens)])
    (match tok
      ['on  (values total #t)]
      ['off (values total #f)]
      [(? number? n)
       (values (if on? (+ total n) total) on?)])))

;; ------------------------------------------------------------------------------------------
;; Testing

(module+ test

  (define *input1*
    "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))")

  (check-equal? 161
                (apply +
                       (map (curry apply *) 
                            (part1-parser *input1*))))

  (define *input2*
    "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))")

  (check-equal? 48
                (execute-instructions 
                 (part2-parser *input2*)))


  
  )
