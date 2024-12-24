#lang racket

(require graph
         racket/hash)

(module+ main

    (define *circuit*
      (call-with-input-file "input.txt" read-puzzle-input))

    ;; Part 1

    (energise! *circuit*)
    (extract-output-val (:vals *circuit*))

    ;; Part2

    ;; Print out the circuit and ... debug it by hand
    (with-output-to-file "graph.dot"
      (thunk
       (display (graphviz (:net *circuit*)
                          #:colors (make-hash (hash-map (:ops *circuit*) op-colour))))))

    )


;; A circuit is a graph, a dictionary [node => op], and a dictionary [node => val]
(struct <circuit> (network ops vals) #:transparent)

(define :net <circuit>-network)
(define :ops <circuit>-ops)
(define :vals <circuit>-vals)

;; ------------------------------------------------------------------------------------------

(define (read-puzzle-input p)
  (let-values ([(sets circ) (splitf-at (port->lines p) (λ (s) (not (string=? s ""))))])
    (let ([vals (parse-settings sets)])
      (let-values ([(network ops) (parse-circuit (cdr circ))])
        (hash-union! ops (make-hash (hash-map vals (λ (nd _) (cons nd 'set)))))
        (<circuit> network
                   ops
                   vals)))))

;; Seetings are a dictionary [node => value]
(define (parse-settings lns)
  (make-hash (map parse-initial-setting lns)))

(define (parse-initial-setting s)
  (let ([ln (string-split s ": ")])
    (cons (car ln) (string->number (cadr ln)))))

(define (parse-circuit lns)
  (let ([elems (map parse-circuit-element lns)])
    (let ([g (directed-graph (append (map third elems) (map fourth elems)))]
          [ops (make-hash (map (λ (e) (cons (car e) (cadr e))) elems))])
      (values g ops))))

(define (parse-circuit-element s)
  (match-let ([(list in1 op in2 "->" out) (string-split s " ")])
    (list out                     ; the name of this node
          (match op               ; the operation
            ["AND" 'and]
            ["OR"  'or]
            ["XOR" 'xor])
          (list in1 out)          ; first edge
          (list in2 out))         ; second edge
    ))

;;; Compute outputs

(define (do-op op in1 in2)
  (match op
    ['and (bitwise-and in1 in2)]
    ['or  (bitwise-ior in1 in2)]
    ['xor (bitwise-xor in1 in2)]))

(define (energise! circuit)
  (match-let ([(<circuit> net ops vals) circuit])
    (let ([ins (transpose net)]) ; for lookup of predecessors
      (for ([node (in-list (tsort net))])
        (unless (hash-has-key? vals node)
          (match-let ([(list in1 in2) (get-neighbors ins node)])
            (let ([v1 (hash-ref vals in1)]
                  [v2 (hash-ref vals in2)]
                  [op (hash-ref ops node)])
              (hash-set! vals node (do-op op v1 v2)))))))))

(define (get-the-z v)
  (let ([node (car v)])
    (and (char=? (string-ref node 0) #\z)
         (cons (string->number (substring node 1)) (cdr v)))))

(define (extract-output-val vals)
  (let ([bits (filter-map get-the-z (hash->list vals))])
     (for/sum ([b bits])
       (* (cdr b)
          (expt 2 (car b))))))

(define (op-colour nd op)
  (cons nd (index-of '(and or xor set) op)))

;;; ------------------------------------------------------------------------------------------

(module+ test

  (define *eg* #<<END
x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02
END
    )
  
  
  (define *eg2* #<<END
x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj
END
    )

  (define *circuit*
    (call-with-input-string *eg2* read-puzzle-input))

  
  
  )
