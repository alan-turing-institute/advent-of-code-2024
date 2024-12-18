#lang racket

(require "grid.rkt")

(module+ main

  (define *bytes*
    (call-with-input-file "input.txt" read-puzzle-input))
  (displayln (format "Length of input: ~a" (length *bytes*)))

  (define *mem* (make-grid 71 71 #\.))
  
  (drop-bytes! *mem* (take *bytes* 1024))

  ;; Part 1

  (shortest-path-length *mem* '(0 . 0) '(70 . 70))

  ;; Part 2

  ;; Well, this is inelegant ...
  (for/last ([byte (drop *bytes* 1024)])
    (displayln (format "~a ... " byte))
    (drop-bytes! *mem* (list byte))
    #:break (not (shortest-path-length *mem* '(0 . 0) '(70 . 70)))
    byte)
  
)

;;; ------------------------------------------------------------------------------------------

(define (shortest-path-length g start end)
  (let ([costg (grid-map (const #f) g)])
    (grid-set! costg end 0)
    (grid-ref 
     (shortest-path-length/recur! g costg (list end) 1)
     start)))

(define (shortest-path-length/recur! g costg frontier steps)
  (if (null? frontier)
      costg
      (let ([new-frontier
             (remove-duplicates
              (append-map
               (λ (p)
                 (filter (conjoin (unvisited? costg) (empty-space? g))
                         (grid-adjacents g p)))
               frontier))])
        (for-each (λ (p) (grid-set! costg p steps)) new-frontier)
        (shortest-path-length/recur! g costg new-frontier (+ steps 1)))))

(define ((unvisited? g) p)
  (not (grid-ref g p)))

(define ((empty-space? g) p)
  (char=? (grid-ref g p) #\.))

(define (drop-bytes! g posns)
  (for ([p (in-list posns)])
    (grid-set! g p #\#)))

(define (show-grid g)
  (for ([ln (in-list (grid->lists g))])
    (displayln (list->string ln))))

;;; ------------------------------------------------------------------------------------------

(define (xy->posn ps)
  (cons (cadr ps) (car ps)))

(define (read-puzzle-input p)
  (map (λ (line)
         (xy->posn (map string->number (string-split line ","))))
       (port->lines p)))

;;; ------------------------------------------------------------------------------------------

(module+ test

  (define *eg* "5,4\n4,2\n4,5\n3,0\n2,1\n6,3\n2,4\n1,5\n0,6\n3,3\n2,6\n5,1\n1,2\n5,5\n2,5\n6,5\n1,4\n0,4\n6,4\n1,1\n6,1\n1,0\n0,5\n1,6\n2,0")

  (define *bytes*
    (call-with-input-string *eg* read-puzzle-input))

  (define *mem* (make-grid 7 7 #\.))

  (drop-bytes! *mem* (take *bytes* 12))

  ;; Part 1

  (shortest-path-length *mem* '(0 . 0) '(6 . 6))

  ;; Part 2
  
  (for/last ([byte (drop *bytes* 12)])
    (displayln (format "~a ... " byte))
    (drop-bytes! *mem* (list byte))
    #:break (not (shortest-path-length *mem* '(0 . 0) '(6 . 6)))
    byte)
  
  )
