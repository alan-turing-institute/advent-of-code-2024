#lang racket


(module+ main

  ;; (define *eg* "2333133121414131402")
  ;; (define *disk-map*
  ;;   (call-with-input-string *eg* read-puzzle-input))

(define *disk-map*
  (call-with-input-file "input.txt" read-puzzle-input))

;; Part 1
(checksum
 (reverse (compact *disk-map*)))

;; Part 2
(checksum (defrag *disk-map*))


  )
;; An item is either (id . size) or ('free . size)
(define (<item> type size)
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
      (<item> (if (even? i) (quotient i 2) 'free)
              (- (char->integer c) 48)))))

;; Little display utility
(define (stringify-map items)
  (apply string-append
         (for/list ([item items])
           (if (free? item)
               (make-string (item-size item) #\.)
               (make-string (item-size item) (integer->char (+ 48 (file-id item))))))))

;; Checksum

(define (checksum items)
  (for/fold ([checksum 0]
             [start    0])
            ([i (in-list items)])
     (let ([size (item-size i)])
      (if (free? i)
          (values checksum (+ start size))
          (let ([id (file-id i)])
            (values (+ checksum
                       (for/sum ([n (in-range start (+ start size))]) (* n id)))
                    (+ start size)))))))

;; Compactifier

(define (skip-free-space items)
  (cond
    [(null? items) '()]
    [(free? (car items)) (cdr items)]
    [else items]))

(define (compact *disk-map*)
  (compactor-loop '() *disk-map* (skip-free-space (reverse *disk-map*))))

;; --- Begin mutually recursive functions ---

;; Assumes disk-tail has free space removed from the head
(define (compactor-loop compacted disk disk-tail)
  ;; (displayln (format "~a : ~a | ~a"  (stringify-map (reverse compacted)) (stringify-map disk) (stringify-map disk-tail)))
  (cond
    [(null? disk) ; we've run out of items
     compacted]
    [(free? (car disk))
     (move-item-from-tail compacted (cdr disk) disk-tail (item-size (car disk)))]
    [else
     (keep-item-from-head compacted disk disk-tail)]))

;; Free space has already been removed from disk
(define (move-item-from-tail compacted disk disk-tail free-space)
  (let* ([to-move        (car disk-tail)]
         [id             (file-id to-move)]
         [required-space (item-size to-move)])
    (cond
      [(< id (file-id (car disk)))
       compacted]
      [(equal? required-space free-space) ; Move the entire item, removing free space
       (compactor-loop (cons to-move compacted)
                       disk
                       (skip-free-space (cdr disk-tail)))]
      [(> free-space required-space)      ; Move the entire item, adding back remaining free space
       (compactor-loop (cons to-move compacted)
                       (cons (<item> 'free (- free-space required-space)) disk)
                       (skip-free-space (cdr disk-tail)))]
      [else                               ; Move as much as possible, leaving residue
       (compactor-loop  (cons (<item> id free-space) compacted)
                        disk
                        (cons (<item> id (- required-space free-space)) (cdr disk-tail)))])))

(define (keep-item-from-head compacted disk disk-tail)
  ;; Tricky bit is checking whether we've already compacted all these items and can stop
  (let ([to-keep (car disk)]
        [next-tail (car disk-tail)])
    (cond
      [(> (file-id to-keep) (file-id next-tail)) ; we've compacted all items beyond this point already 
       compacted]
      [(equal? (file-id to-keep) (file-id next-tail)) ; we've compacted some of this item. Move the rest
       (compactor-loop (cons next-tail compacted) (cdr disk) (skip-free-space (cdr disk-tail)))]
      [else
       (compactor-loop (cons to-keep compacted) (cdr disk) disk-tail)])))

;; -- End of recursive defintions ---

(define (defrag *disk-map*)
  (defrag-loop *disk-map* (skip-free-space (reverse *disk-map*))))

(define (defrag-loop disk disk-tail)
  (if (null? disk-tail)
      disk
      (let ([next (car disk-tail)])
        (defrag-loop (insert-into disk next) (skip-free-space (cdr disk-tail))))))

;; Add a free space block to the head of items unless free-space is zero
(define (push-free items free-space)
  (if (zero? free-space) items (cons (<item> 'free free-space) items)))

(define (insert-into disk item)
  ;; (displayln (format "Inserting ~a into ~a" item (stringify-map disk)))
  (let loop ([result '()]
             [rest disk])
    ;; (displayln (format "  ~a : ~a" (stringify-map result) (stringify-map rest)))
    (cond
      [(null? rest)
       result]
      [(free? (car rest)) ; Try to insert item here
       (let ([space-required (item-size item)]
             [space-free     (item-size (car rest))])
         (if (> space-required space-free)
             (loop (push-free result space-free) (cdr rest))
             (append-in-reverse (cons item result)
                                (push-free
                                 (cdr (replace item (<item> 'free space-required) rest))
                                 (- space-free space-required)))))]
      [else
       (if (equal? (file-id item) (file-id (car rest)))
           (append-in-reverse result rest)
           (loop (cons (car rest) result) (cdr rest)))])))

;; equivalent to (append (reverse rev) list)
(define (append-in-reverse rev lst)
  (if (null? rev)
      lst
      (append-in-reverse (cdr rev) (cons (car rev) lst))))

;; Replcae the first occurence of x with v in xs
(define (replace x v xs)
  (let-values ([(hd tl) (splitf-at xs (λ (p) (not (equal? p x))))])
    (if (null? tl)
        hd
        (append hd (cons v (cdr tl))))))
