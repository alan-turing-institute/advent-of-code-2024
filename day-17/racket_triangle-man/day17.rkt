#lang racket

(module+ main

  ;; Part 1

  (define-values (*state* *memory*)
    (values (<state> 64751475 0 0 0)
            #(2 4 1 2 7 5 4 5 1 3 5 5 0 3 3 0)))
  
  (machine/run *state* *memory*)

  ;; Part 2

  ;; Oh, this doesn't work
  ;; (search-for-quine #(2 4 1 2 7 5 4 5 1 3 5 5 0 3 3 0))  

  ;; .start
  ;; 2 4 | B <- (A mod 8)         ; B is lowest three bits of A
  ;; 1 2 | B <- B xor b010        ; flip bit 2 of B
  ;; 7 5 | C <- A >> B            ; C is A >> B (anywhere from 0 to 3 shift) 
  ;; 4 5 | B <- B xor C           ; flip C bits of B
  ;; 1 3 | B <- B xor b011        ; flip bits 1 and 2 of B
  ;; 5 5 | out (B mod 8)          ; output the lowest three bits of B
  ;; 0 3 | A <- A >> 3            ; get the next three bits of A
  ;; 3 0 | jump (ne? A 0) .start  ; and repeat

  (define (find-As-to-produce val starts memory)
    (append-map
     (λ (start)
       (filter-map
        (λ (A)
          (let ([output
                 (machine/run (<state> A 0 0 0) memory)])
            ;; (displayln (format "A = ~a: ~a" A output))
            (and (equal? (car output) val)
                 A)))
        (range start (+ start 8))))
     starts))

  ;; How to replace failure by a list of successes!
  
  (for/fold ([As '(0)])
            ([op (reverse (vector->list *memory*))])
    (let ([next-As 
           (find-As-to-produce op As *memory*)])
      (displayln next-As)
      (map (curryr arithmetic-shift 3) next-As)))
  
  )


(struct <ins> (opcode operand) #:transparent)
(define :opc <ins>-opcode)
(define :opa <ins>-operand)

(struct <state> (A B C ip) #:transparent)
(define-values (:A :B :C :ip)
  (values <state>-A <state>-B <state>-C <state>-ip))

(define (read mem addr)
  (vector-ref mem addr))
(define (write! mem addr val)
  (vector-set! mem addr val))

(define (combo opa state)
  (match opa
    [0 0]
    [1 1]
    [2 2]
    [3 3]
    [4 (:A state)]
    [5 (:B state)]
    [6 (:C state)]
    ;; No 7 -- crash
    ))

;; The output 
(define out (make-parameter '()))

;; Returns a new state, writes to port out
(define (machine/step state memory)
  (let ([ip (:ip state)])
    (let ([opc (read memory ip)]
          [opa (read memory (+ ip 1))])
      (match opc
        [0 ; adv
         (struct-copy <state> state
                      [A (arithmetic-shift (:A state) (- (combo opa state)))]
                      [ip (+ ip 2)])] 
        [1 ; bxl
         (struct-copy <state> state
                      [B (bitwise-xor (:B state) opa)]
                      [ip (+ ip 2)])]
        [2 ; bst
         (struct-copy <state> state
                      [B (modulo (combo opa state) 8)]
                      [ip (+ ip 2)])] 
        [3 ; jnz
         (if (zero? (:A state))
             (struct-copy <state> state
                          [ip (+ ip 2)])
             (struct-copy <state> state
                          [ip opa]))]
        [4 ; bxc
         (struct-copy <state> state
                      [B (bitwise-xor (:B state) (:C state))]
                      [ip (+ ip 2)])]
        [5 ; out
         (out (cons (modulo (combo opa state) 8) (out)))
         (struct-copy <state> state
                      [ip (+ ip 2)])] 
        [6 ; bdv
         (struct-copy <state> state
                      [B (arithmetic-shift (:A state) (- (combo opa state)))]
                      [ip (+ ip 2)])] 
        [7 ; cdv
         (struct-copy <state> state
                      [C (arithmetic-shift (:A state) (- (combo opa state)))]
                      [ip (+ ip 2)])]))))

(define (machine/run state memory)
  (parameterize ([out '()])
    (let loop ([state state])
      ;; (display (format "[~a]" (:ip state)))
      (if (>= (:ip state) (vector-length memory))
          (reverse (out))
          (loop (machine/step state memory))))))

;; For part 2
;; (define (search-for-quine memory)
;;   (let ([original-program (reverse (vector->list memory))])
;;     (for ([A (in-naturals 161480704)])
;;       (when (zero? (modulo A 1048576)) (displayln (format "~a " A)))
;;       (when (equal? original-program
;;                     (machine/run (<state> A 0 0 0) memory))
;;         (displayln (format "Found it! At A = ~a" A)))
;;       )
;;     ))
  

  ;; ------------------------------------------------------------------------------------------

(module+ test
  
  (require rackunit)
  
  ;; Produces 0,1,2,
  (machine/run (<state> 10 0 0 0) #(5 0 5 1 5 4))
  
  ;; Infinite loop?
  (machine/run (<state> 2024 0 0 0) #(0 1 5 4 3 0))
  
  ;; B shoulbe be 26 
  (machine/run (<state> 0 29 0 0) #(1 7))
  
  ;; B should be 44354
  (machine/run (<state> 0 2024 43690 0) #(4 0))

  ;; Part 2

  (machine/run (<state> 117440 0 0 0) #(0 3 5 4 3 0))
  
  ;; (search-for-quine #(0 3 5 4 3 0))
  )

