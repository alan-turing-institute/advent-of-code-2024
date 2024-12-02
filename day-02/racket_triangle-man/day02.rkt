#lang racket

(require rackunit)

(define (read-reports p)
  (for/list ([l (in-lines p)])
    (map string->number (string-split l)))
  )

(define (first-differences xs)
  (for/list ([x (in-list xs)]
             [y (in-list (cdr xs))])
    (- y x)))

(define (report-safe? r)
  (let ([δs (first-differences r)])
    (let ([max-δ (apply max δs)]
          [min-δ (apply min δs)])
      (or (and (>= min-δ 1) (<= max-δ 3))
          (and (<= max-δ -1) (>= min-δ -3))))))

;; Remove element at position pos
;; Terribly inefficient!
(define (drop-at lst pos)
  (for/fold ([hd '()]
             [tl lst]
             #:result (reverse hd))
            ([n (in-range (length lst))])
    (if (= (+ n 1) pos)
        (values hd (cdr tl))
        (values (cons (car tl) hd) (cdr tl)))))

;; Are any variations on report r safe?
(define (report-safe/1? r)
  (for/or ([n (in-range (+ 1 (length r)))])
    (report-safe? (drop-at r n))))

;; ------------------------------------------------------------------------------------------

(module+ main

  (define *reports*
    (call-with-input-file "input.txt" read-reports))

  ;; Part 1
  (length (filter-map report-safe? *reports*))

  ;; Part 2
  (length (filter-map report-safe/1? *reports*))
    
  )


;; ------------------------------------------------------------------------------------------
;; Testing

(module+ test

  (define *input* #<<END
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
END
    )

  (define *reports*
    (call-with-input-string *input* read-reports))

  (check-equal?
   (length (filter-map report-safe? *reports*))
   2)

  (check-equal? 
   (length (filter-map report-safe/1? *reports*))
   4)
  
  )
