#lang racket

(require racket/hash)

(module+ main

  (define *seeds*
    (with-input-from-file "input.txt"
      (thunk (map string->number (port->lines)))))

  ;; Part 1
  
  (for/sum ([seed (in-list *seeds*)])
    (iterate next-secret seed 2000))

  ;; Part 2
  
  (define *prices*
    (let ([prices (make-hash)])
      (for ([seed (in-list *seeds*)])
        (displayln seed)
        (hash-union! prices (price-map seed 2000) #:combine +))
      prices))

  (displayln (format "Maximum bananas: ~a" (apply max (hash-values *prices*))))
  
  )



(module+ test

  (require rackunit)
  
  (check-equal?
   (mix 42 15)
   37)
  
  (check-equal?
   (prune 100000000)
   16113920)

  (check-equal?
   (hash-ref (price-map 1 2000) '(-2 1 -1 3))
   7)
  
  (define *eg* #<<END
1
10
100
2024
END
    )

  (define *seeds*
    (with-input-from-string *eg*
      (thunk (map string->number (port->lines)))))

  ;; Part 1
  
  (for/sum ([seed (in-list *seeds*)])
    (iterate next-secret seed 2000))

  ;; Part 2
  
  (define *prices*
    (let ([prices (make-hash)])
      (for ([seed (in-list '(1 2 3 2024))])
        (displayln seed)
        (hash-union! prices (price-map seed 2000) #:combine +))
      prices))
  
  )

;; ------------------------------------------------------------------------------------------

;; Ring buffers

(struct ring-buffer (buf [head #:mutable]) #:transparent)
(define (make-ring-buffer len)
  (ring-buffer (make-vector len #f) 0))
(define (ring-buffer-insert! rb val)
  (let ([buf  (ring-buffer-buf rb)]
        [head (ring-buffer-head rb)])
    (vector-set! buf head val)
    (set-ring-buffer-head! rb (modulo (+ head 1) (vector-length buf)))))
(define (ring-buffer->list rb)
   (let* ([buf (ring-buffer-buf rb)]
          [head (ring-buffer-head rb)]
          [len (vector-length buf)])
     (for/list ([i (in-range len)])
       (vector-ref buf (modulo (+ head i) len)))))

;; Generate the secret codes

(define (iterate proc seed n)
  (let loop ([n n]
             [v seed])
    (if (zero? n)
        v
        (loop (- n 1) (proc v)))))

(define (iterate/list proc seed n)
  (for/fold ([x  seed]
             [xs '()]
             #:result (reverse xs))
            ([_ (in-range (+ n 1))])
    (values (proc x) (cons x xs))))

(define (mix a b)
  (bitwise-xor a b))

(define (prune x)
  (modulo x 16777216))

(define (next-secret v)
  (let* ([x1 (prune (mix (* v 64) v))]
         [x2 (prune (mix (quotient x1 32) x1))]
         [x3 (prune (mix (* x2 2048) x2))])
    x3
    )
  )

;; Compute prices and differences and construct price hash
;; price hash is a hash of 4-tuple => price, where 4-tuple is the first time this tuple was seen 
(define (price-map seed n)
  (let ([price-map (make-hash)]
        [secrets (iterate/list next-secret seed n)]
        [buffer (make-ring-buffer 4)])
    (for ([secret (in-list secrets)]
          [secret2 (in-list (cdr secrets))])
      (let ([p1 (remainder secret 10)]
            [p2 (remainder secret2 10)])
        (let ([δ (- p2 p1)])
          (ring-buffer-insert! buffer δ)
          (let ([last-four-δs (ring-buffer->list buffer)])
            (if (hash-has-key? price-map last-four-δs)
                void
                (hash-set! price-map last-four-δs p2))))))
    price-map))

;; For every f-tuple in p2 that's in p1, add the values, otherwise add the tuple in p2
;; (define (add-price-maps p1 p2)
;;   (let ([price-map (hash-copy p1)])
;;     (for ([(δs prices) (in-hash p2)])
;;       ))
  
  ;; )
