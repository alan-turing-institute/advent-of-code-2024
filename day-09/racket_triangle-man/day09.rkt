#lang racket



(module+ main

  (define *eg* "2333133121414131402")

  (define *disk-map*
    (call-with-input-string *eg* read-puzzle-input))
  
  (compact-blocks *disk-map*)
  
  )

;; An item is either (id . size) or ('free . size)
(define (item type size)
  (cons type size))

(define (file-id item)
  (car item))

(define (free? item)
  (eq? (car item) 'free))

(define (item-size item)
  (cdr item))

;; string -> list-of item
(define (read-puzzle-input p)
  (let ([in (string->list (port->string p))])
    (for/list ([i (in-naturals)]
               [c (in-list in)])
      (cons (if (even? i) (quotient i 2) 'free)
            (- (char->integer c) 48)))))

(define (stringify-map items)
  (apply string-append
         (for/list ([item items])
           (if (free? item)
               (make-string (item-size item) #\.)
               (make-string (item-size item) (integer->char (+ 48 (file-id item))))))))

(define (compact-blocks *disk-map*)
  (let compacter ([compacted '()]
                  [map       *disk-map*]
                  [map-tail  (reverse *disk-map*)])
    (displayln (format "~a : ~a | ~a"  (stringify-map (reverse compacted)) (stringify-map map) (stringify-map map-tail)))
    (if (null? map) 
        compacted
        (let ([next-item (car map)])
          (if (not (free? next-item)) ;; TODO: stop if we've moved this item 
              (compacter (cons next-item compacted) (cdr map) map-tail)
              (let ([next-to-move (car map-tail)])
                (if (free? next-to-move) ;; Skip free items from the end
                    (compacter compacted map (cdr map-tail))
                    ;; Move as much as we can of the end item
                    (let ([id             (file-id next-to-move)]
                          [required-space (item-size next-to-move)]
                          [free-space     (item-size next-item)])
                      (cond 
                        [(equal? required-space free-space) ; Move all, removing free space
                         (compacter (cons next-to-move compacted) (cdr map) (cdr map-tail))]
                        [(> free-space required-space)      ; Move all, adding remaining free space
                         (compacter (cons next-to-move compacted)
                                    (cons (cons 'free (- free-space required-space)) (cdr map))
                                    (cdr map-tail))]
                        [else                               ; Move as much as possible, leaving residue
                         (compacter  (cons (cons (file-id next-to-move) free-space) compacted)
                                     (cdr map)
                                     (cons (cons (file-id next-to-move) (- required-space free-space)) (cdr map-tail)))])))))))
    
    ))
