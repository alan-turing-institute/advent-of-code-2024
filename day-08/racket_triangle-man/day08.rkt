#lang racket

(module+ main

  (define *the-city*
    (call-with-input-file "input.txt" read-puzzle-input))

  (define *the-city-nrows* (length *the-city*))
  (define *the-city-ncols* (length (car *the-city*)))
  
  (define *antennae* (locate-antennae *the-city*))

  ;; Part 1
  
  (length
   (remove-duplicates
    (append-map (curry antinodes/1 *the-city-nrows* *the-city-ncols*)
                (group-by car *antennae*))))

  ;; Part 2

  (length
   (remove-duplicates
    (append-map (curry antinodes/2 *the-city-nrows* *the-city-ncols*)
                (group-by car *antennae*))))

  
  )


;; Returns a list of lists
(define (read-puzzle-input p)
  (map string->list (sequence->list (in-lines p))))

;; Returns ((#\a . (1 . 2)) ... )
(define (locate-antennae rows)
  (for*/list ([(row nr) (in-indexed rows)]
              [(col nc) (in-indexed row)]
              #:unless (char=? col #\.))
    (cons col (cons nr nc))))

;; as : a list of antennae with the same frequency
;; filters out those beyond the bounds of the map

(define (in-bounds? nrows ncols pos)
  (match-let ([(cons r c) pos])
    (and (>= r 0)
         (< r nrows)
         (>= c 0)
         (< c ncols))))

(define (antinodes/1 nrows ncols as)
  (filter (curry  in-bounds? nrows ncols)
          (append-map antinodes-of/1
                      (sequence->list (in-combinations as 2)))))

;; Both antinode of antennae a1 and a2 (for Part 1)
(define (antinodes-of/1 aa)
  (match-let ([(cons _ (cons r1 c1)) (car aa)]
              [(cons _ (cons r2 c2)) (cadr aa)])
    (list
     (cons (- r1 (- r2 r1)) (- c1 (- c2 c1)))
     (cons (+ r2 (- r2 r1)) (+ c2 (- c2 c1))))))

(define (antinodes/2 nrows ncols as)
  (append-map (curry antinodes-of/2 nrows ncols)
              (sequence->list (in-combinations as 2))))

;; Both antinode of antennae a1 and a2 (for Part 1)
(define (antinodes-of/2 nrows ncols aa)
  (match-let ([(cons _ (cons r1 c1)) (car aa)]
              [(cons _ (cons r2 c2)) (cadr aa)])
    (let ([δr (- r2 r1)]
          [δc (- c2 c1)])
      (append
       ;; All the antinodes a1 -> a2 (including a1 and a2)
       (for/list ([n (in-naturals 0)])
         (define antinode
           (cons (+ r1 (* n δr)) (+ c1 (* n δc))))
         #:break (not (in-bounds? nrows ncols antinode))
         antinode)
       (for/list ([n (in-naturals 1)])
         (define antinode
           (cons (- r1 (* n δr)) (- c1 (* n δc))))
         #:break (not (in-bounds? nrows ncols antinode))
         antinode)))))



(module+ test

  (define *input* #<<END
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
END
    )

  (define *the-city*
    (call-with-input-string *input* read-puzzle-input))

  (define *the-city-nrows* (length *the-city*))
  (define *the-city-ncols* (length (car *the-city*)))
  
  (define *antennae* (locate-antennae *the-city*))

  ;; Part 1

  (length
   (remove-duplicates
    (append-map (curry antinodes/1 *the-city-nrows* *the-city-ncols*)
                (group-by car *antennae*))))

  ;; Part 2
  (length
   (remove-duplicates
    (append-map (curry antinodes/2 *the-city-nrows* *the-city-ncols*)
                (group-by car *antennae*))))

  )
 
