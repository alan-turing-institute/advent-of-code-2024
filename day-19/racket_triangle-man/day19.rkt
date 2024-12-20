#lang racket

(module+ main

  (define-values (*towels* *designs*)
    (call-with-input-file "input.txt" read-puzzle-input))

  ;; Part 1
  
  ;; (length
  ;;  (filter-map (curry decompose *towels*) *designs*))
  
  ;; Part 2

  (define *organised-towels* (organise-towels *towels*))
  
  (for/sum ([d *designs*])
    (let ([n (cdr (assoc (length d) (let-me-count-the-ways d *organised-towels*)))])
      (displayln (format "~a: ~a" (list->string d) n))
      n))

  )


;; Organise the towels by size

;; -> association list [(length towels) ...]
(define (organise-towels towels)
  (let ([n-grams (group-by length towels)])
    (map (λ (ngs) (cons (length (car ngs)) ngs)) n-grams))
  )

;; towels should be an association list, as above
;; returns an association list of (n . count), where n is the length of a suffix of design, and count is the number of ways of making that suffix. 

(define (let-me-count-the-ways design towels)
  ;; (displayln (list->string design))
  (if (null? design)
      '((0 . 1))
      ;; The number of ways of making `design` of length n out of
      ;; things in towel is:
      ;; - the number of length-1 towels that match the first element, times
      ;;   the number of length-(n-1) ways; plus
      ;; - the number of length-2 towels that exactly match the first two elements, times
      ;;   the number of length-(n-2) ways; plus
      ;; - ...
      ;; - the number of length-n towels that exactly match.
      ;; - 
      (let ([n-1-counts (let-me-count-the-ways (cdr design) towels)]
            [N (length design)])
        (let ([n-count
               (for/sum ([n (in-range 1 (+ (length design) 1))])
                 (* (cdr (assoc (- N n) n-1-counts))
                    (count-exact-matches (take design n) towels)))])
          (cons (cons N n-count) n-1-counts)))))

(define (count-exact-matches xs towels)
  (let* ([n (length xs)]
         [ts (cdr (or (assoc n towels) '(() . ())))])
    (count (curry equal? xs) ts)))

(define (decompose towels design)
  (decompose/recur towels design 1))

(define (decompose/recur towels design N)
  (if (null? design)
      N
      (let loop ([ts towels]
                 [N1 0])
        (if (null? ts)
            (* N N1)
            (let ([next-towel (car ts)])
              (if (list-prefix? next-towel design)
                  (loop (cdr ts)
                        (+ N1
                           (decompose/recur towels
                                            (drop design (length next-towel))
                                            N)))
                  (loop (cdr ts) N1)))))))

;; (define (decompose towels design)
;;   (decompose/recur towels design '()))

;; (define (decompose/recur towels design so-far)
;;   (if (null? design)
;;       so-far
;;       (let try-next-towel ([ts towels])
;;         (if (null? ts)
;;             #f
;;             (let ([next-towel (car ts)])
;;               (or (and (list-prefix? next-towel design)
;;                        (decompose/recur towels
;;                                         (drop design (length next-towel))
;;                                         (cons next-towel so-far)))
;;                   (try-next-towel (cdr ts))))))))

(define (read-puzzle-input p)
  (match (string-split (port->string p) "\n\n")
    [(list towels designs)
     (values (map string->list (string-split towels ", "))
             (map string->list (string-split designs "\n")))]))

(module+ test

  (define *eg* #<<END
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
END
    )

  (define-values (*towels* *designs*)
    (call-with-input-string *eg* read-puzzle-input))

  (for/sum ([d *designs*])
    (let ([n (decompose *towels* d)])
      (displayln (format "~a: ~a" (list->string d) n))
      n))

  ;; (length
  ;;  (filter-map (curry decompose *towels*) *designs*))

  ;; (decompose *towels* (string->list "bwurrg"))
  
  )
