#lang racket

(module+ main

  (define *eg* '(125 17))

  (define *input*
    (map string->number
         (string-split
          (call-with-input-file "input.txt" port->string))))

  ;; Part 1
  (apply + (map (curryr blink 25) *input*))

  ;; Part 2
  (apply + (map (curryr blink 75) *input*))
  
  )

;;; ------------------------------------------------------------------------------------------

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

(define/memoise (blink stone blinks)
  (cond
    [(zero? blinks) 1]
    [(eq? stone 0)  (blink 1 (- blinks 1))]
    [(odd? (order-of-magnitude stone))
     (let-values ([(lft rgt) (split-stone stone)])
       (+ (blink lft (- blinks 1)) (blink rgt (- blinks 1))))]
    [else
     (blink (* stone 2024) (- blinks 1))]))

(define (split-stone stone)
  (let ([pow (quotient (+ (order-of-magnitude stone) 1) 2)])
    (quotient/remainder stone (expt 10 pow))))



