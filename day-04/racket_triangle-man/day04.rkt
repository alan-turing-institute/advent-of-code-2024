#lang racket

(require "grid.rkt") ; Stolen from my 2023 code.

(module+ main

  (define *word-search-grid*
    (with-input-from-file "input.txt"
      (thunk
       (lists->grid
        (map string->list
             (sequence->list (in-lines)))))))

  (displayln (format "Read a ~a x ~a grid." (grid-nrows *word-search-grid*) (grid-ncols *word-search-grid*)))
  
  ;; Part 1
  
  (for*/sum ([x (in-range (grid-nrows *word-search-grid*))]
             [y (in-range (grid-ncols *word-search-grid*))]
             [dir (in-list *compass*)])
      (if (word-at? *word-search-grid* *search-word* `(,x . ,y) dir)
        1
        0))

 ;; Part 2

  (for*/sum ([x (in-range 1 (- (grid-nrows *word-search-grid*) 1))]
             [y (in-range 1 (- (grid-ncols *word-search-grid*) 1))])
    (let ([here (cons x y)])
      (if (and (char=? (grid-ref *word-search-grid* here) #\A)
               (let ([ne (grid-ref *word-search-grid* (pos+ here '(-1 .  1)))]
                     [se (grid-ref *word-search-grid* (pos+ here '( 1 .  1)))]
                     [sw (grid-ref *word-search-grid* (pos+ here '( 1 . -1)))]
                     [nw (grid-ref *word-search-grid* (pos+ here '(-1 . -1)))])
                 (and (or (and (char=? ne #\M) (char=? sw #\S))
                          (and (char=? ne #\S) (char=? sw #\M)))
                      (or (and (char=? nw #\M) (char=? se #\S))
                          (and (char=? nw #\S) (char=? se #\M))))))
          1
          0))))

;; ------------------------------------------------------------------------------------------

(define *compass* '((0 . 1) (1 . 1) (1 . 0) (1 . -1) (0 . -1) (-1 . -1) (-1 . 0) (-1 . 1)))

(define *search-word* (string->list "XMAS"))

;; word-at? : grid? (list-of char?) posn? dir? -> bool?
;; Does word chars exist in the grid at position pos and direction dir?

(define (word-at? grid chars pos dir)
  ;; (displayln (format "Looking for ~a at ~a heading ~a" (car chars) pos dir))
  (or (null? chars)                    ; if we're at the end of the search word, we're done
      (and (grid-pos-inside? grid pos) ; if we're outside the grid, we have not found the word
           (char=? (car chars) (grid-ref grid pos))
           (word-at? grid (cdr chars) (pos+ pos dir) dir)))) ; and recurse on the rest of the word

;; ------------------------------------------------------------------------------------------

(module+ test

  (define *input* #<<END
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
END
    )

  (define *word-search-grid*
    (lists->grid (map string->list (string-split *input*))))

  ;; Part 1 
  
  (for*/sum ([x (in-range (grid-nrows *word-search-grid*))]
             [y (in-range (grid-ncols *word-search-grid*))]
             [dir (in-list *compass*)])
    (if (word-at? *word-search-grid* *search-word* `(,x . ,y) dir)
        1
        0))

  ;; Part 2

  (for*/sum ([x (in-range 1 (- (grid-nrows *word-search-grid*) 1))]
             [y (in-range 1 (- (grid-ncols *word-search-grid*) 1))])
    (let ([here (cons x y)])
      (if (and (char=? (grid-ref *word-search-grid* here) #\A)
               (let ([ne (grid-ref *word-search-grid* (pos+ here '(-1 .  1)))]
                     [se (grid-ref *word-search-grid* (pos+ here '( 1 .  1)))]
                     [sw (grid-ref *word-search-grid* (pos+ here '( 1 . -1)))]
                     [nw (grid-ref *word-search-grid* (pos+ here '(-1 . -1)))])
                 (and (or (and (char=? ne #\M) (char=? sw #\S))
                          (and (char=? ne #\S) (char=? sw #\M)))
                      (or (and (char=? nw #\M) (char=? se #\S))
                          (and (char=? nw #\S) (char=? se #\M))))))
          1
          0))))

