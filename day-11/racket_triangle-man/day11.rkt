#lang racket

(module+ main

  (define *eg* '(125 17))

  (define *input*
    (map string->number
         (string-split
          (call-with-input-file "input.txt" port->string))))

  ;; Part 1
  (blink/list *input* 25)

  ;; Part 2
  (blink/list *input* 75)
  
  )

;;; ------------------------------------------------------------------------------------------

(define (blink/list stones blinks)
  ;; (displayln (format "~a" stones))
  (if (null? stones)
      0
      (let ([fst (blink (car stones) blinks)])
        (+ fst (blink/list (cdr stones) blinks)))))

(define (blink/1 stone blinks)
  (cond
    [(zero? blinks) 1]
    [(eq? stone 0)  (blink 1 (- blinks 1))]
    [(odd? (order-of-magnitude stone)) (blink/list (split-stone stone) (- blinks 1))]
    [else (blink (* stone 2024) (- blinks 1))]))

(define (split-stone stone)
  (let ([pow (quotient (+ (order-of-magnitude stone) 1) 2)])
    (let-values ([(fst snd) (quotient/remainder stone (expt 10 pow))])
      (list fst snd))))

;; fn is a function of two arguments
(define (memoise fn)
 (let ([lookup (make-hash)])
   (λ (x y)
     (let* ([arg (cons x y)]
            [val (hash-ref lookup arg #f)])
       (if val
           val
           (let ([result (fn x y)])
             (begin
               (hash-set! lookup arg result)
               result)))))))

(define blink
  (memoise blink/1))
