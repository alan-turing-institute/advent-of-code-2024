#lang racket

(require graph) ; not messing around any more.

(module+ main

    (define *network*
    (unweighted-graph/undirected
     (call-with-input-file "input.txt" read-puzzle-input)))

    ;; Part 1
    
    (define *3cliques* (three-cliques *network*))

    (count (λ (st) (ormap starts-with-t? (set->list st))) (set->list *3cliques*))
    
    ;; Part 2

    (define *maximal-cliques*
      (bron-kerbosch *network* (set) (list->set (get-vertices *network*)) (set)))
    (displayln (format "Number of maximal cliques: ~a" (length *maximal-cliques*)))
    
    (define *max-n*
      (apply max (map set-count *maximal-cliques*)))
    (displayln (format "Size of maximal clique: ~a" *max-n*))
    
    (define *max-clique*
      (car
       (filter (λ (c) (equal? (set-count c) *max-n*)) *maximal-cliques*)))

    (string-join 
     (sort (set->list *max-clique*) string<=?)
     ",")
    
    )
           


    
(define (read-puzzle-input p)
  (map (curryr string-split "-") (port->lines p))
  )

;; Return all cliques with three vertices
(define (three-cliques g)
  (for/fold ([cliques (set)])
            ([v₁ (in-vertices g)])
    (let ([nbrs (get-neighbors g v₁)])
      (let* ([adjs 
              (filter (λ (vs) (has-edge? g (car vs) (cadr vs)))
                      (combinations nbrs 2))]
             [adjs-set (apply set
                              (map (λ (vs) (apply set v₁ vs)) adjs))])
        (set-union cliques
                   adjs-set)))))

(define (starts-with-t? c)
  (char=? (string-ref c 0) #\t))


;; The Bron-Kerbosch algorithm (1973), without pivoting, for finding
;; all maximal cliques
;; See: https://en.wikipedia.org/wiki/Bron%E2%80%93Kerbosch_algorithm
;; Relies very heavily on Racket's (immutable) set data structure! 
;; Call with R and X empty sets, and P a set of vertices 
(define (bron-kerbosch g R P X)
  (if (and (set-empty? P)
           (set-empty? X))
      R
      (for/fold ([cliques '()]
                 [P P]
                 [X X]
                 #:result (flatten cliques))
                ([v (in-set P)])
        (let ([nbrs (list->set (get-neighbors g v))])
          (values
           (cons (bron-kerbosch g
                                (set-add R v)
                                (set-intersect P nbrs)
                                (set-intersect X nbrs))
                 cliques)
           (set-remove P v)
           (set-add X v))))))

  
(module+ test

  (define *eg* #<<END
kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
END
    )

  (define *network*
    (unweighted-graph/undirected
     (call-with-input-string *eg* read-puzzle-input)))

  (define 3cliques (three-cliques *network*))

  (count (λ (st) (ormap starts-with-t? (set->list st))) (set->list 3cliques))
  
  )

