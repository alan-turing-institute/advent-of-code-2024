#lang racket

(module+ main

  (define *eg* #<<END
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
END
    )

  ;; (define *machines*
  ;;   (call-with-input-string *eg* read-puzzle-input))
  
  (define *machines*
    (call-with-input-file "input.txt" read-puzzle-input))

  ;; Part 1

  (apply +
         (filter-map (λ (m) (apply tokens-for m))
                     *machines*))
  
  ;; Part 2

  (define (recalibrate machine)
    (match-let ([(list A B (cons X Y)) machine])
      (list A B (cons (+ X 10000000000000) (+ Y 10000000000000)))))
  
  (apply +
         (filter-map (λ (m) (apply tokens-for m))
                     (map recalibrate  *machines*)))
  
  )


;; ------------------------------------------------------------------------------------------

(define (read-puzzle-input p)
  (map read-machine (string-split (port->string p) "\n\n"))
  )

(define rxa #px"Button A: X\\+([[:digit:]]+), Y\\+([[:digit:]]+)")
(define rxb #px"Button B: X\\+([[:digit:]]+), Y\\+([[:digit:]]+)")
(define rxp #px"Prize: X=([[:digit:]]+), Y=([[:digit:]]+)")

(define (read-machine s)
  (let ([parts (string-split s "\n")])
    (list (read-coords rxa (car parts))
          (read-coords rxb (cadr parts))
          (read-coords rxp (caddr parts)))))

(define (read-coords rx s)
  (let ([m
         (regexp-match rx s)])
    (cons (string->number (cadr m)) (string->number (caddr m)))))

;; Find 3 m + n subject to
;;
;; m A_x + n B_x = P_x
;; m A_y + n B_y = P_y
;;
;; and m <= 100, n <= 100

;; m = (P_x B_y - P_y B_x) / (A_x B_y - A_y B_x)
;; n = (P_x A_y - P_y A_x) / (B_x A_y - B_y A_x)

(define (tokens-for A B P)
  (let ([mn (solve A B P)])
    (and mn
         (match-let ([(cons m n) mn])
           (and
            ;; (<= m 100) 
            ;; (<= n 100)
            (+ (* 3 m) n))))))

(define (solve A B P)
  (match-let ([(cons Ax Ay) A]
              [(cons Bx By) B]
              [(cons Px Py) P])
    (let-values
        ([(mq mr) (quotient/remainder (- (* Px By) (* Py Bx))
                                      (- (* Ax By) (* Ay Bx)))]
         [(nq nr) (quotient/remainder (- (* Px Ay) (* Py Ax))
                                      (- (* Bx Ay) (* By Ax)))])
      (if (and (zero? mr) (zero? nr))
          (cons mq nq)
          #f))))

;; ------------------------------------------------------------------------------------------


(module+ test
  (require rackunit)

  (check-equal?
   (tokens-for '(94 . 34) '(22 . 67) '(8400 . 5400))
   280)

  (check-equal?
   (tokens-for '(26 . 66) '(67 . 21) '(12748 . 12176))
   #f)

  (check-equal?
   (tokens-for '(17 . 86) '(84 . 37) '(7870 . 6450))
   200)

  (check-equal?
   (tokens-for '(69 . 23) '(27 . 71) '(18641 . 10279))
   #f)


  )

