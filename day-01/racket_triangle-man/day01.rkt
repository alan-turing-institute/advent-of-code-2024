#lang racket

(require rackunit)

;; Helper function. Why isn't this in the standard library?
(define (zip xss) (apply map list xss))

;; parse-input : lines -> two lists of sorted numbers
(define (parse-input p)
  (let* ([input-pairs
         (for/list ([l (in-lines p)])
           (map string->number (string-split l)))]
         [input-lists
          (zip input-pairs)])
    (values (sort (car input-lists) <) (sort (cadr input-lists) <))))


;; ------------------------------------------------------------------------------------------

(module+ main

  (define-values (*in1* *in2*)
    (call-with-input-file "input.txt" parse-input))

  ;; Part 1

  (define *answer-to-part1*
    (for/sum ([x *in1*]
              [y *in2*])
      (abs (- x y))))

  (displayln (format "Part 1: ~a" *answer-to-part1*) )

  ;; Part 2

  (define *answer-to-part2*
    (for/fold ([rest *in2*]
               [total 0]
               #:result total)
              ([x (in-list *in1*)])
      #:break (null? rest)
      (let ([rest* (dropf rest (λ (y) (< y x)))]) ; skip to next position in *rest*
        (let ([ns (length (takef rest* (curry = x)))])
          (values rest* (+ total (* x ns)))))))

  (displayln (format "Part 2: ~a" *answer-to-part2*)))

;; ----------------------------------------------------------------------------------------
;; Testing

(module+ test 

  (define *input* #<<END
3   4
4   3
2   5
1   3
3   9
3   3
END
    )

  (define-values (*in1* *in2*)
    (call-with-input-string *input* parse-input))

  (define *answer-to-part1*
    (for/sum ([x *in1*]
              [y *in2*])
      (abs (- x y))))

  (check-equal? *answer-to-part1* 11)
  
  (define *answer-to-part2*
    (for/fold ([rest *in2*]
               [total 0]
               #:result total)
              ([x (in-list *in1*)])
      #:break (null? rest)
      (displayln (format "~a ~a" total rest))
      (let ([rest* (dropf rest (λ (y) (< y x)))]) ; skip to next position in *rest*
        (let ([ns (length (takef rest* (curry = x)))])
          (values rest* (+ total (* x ns)))))))

  (check-equal? *answer-to-part2* 31)
  
  )








