(add-to-load-path "/home/tomaz/code/advent-of-code-2024/day-09/guile_tomazgda/my_modules")
(use-modules (utils))

(use-modules (ice-9 textual-ports)
	     (srfi srfi-1))

;;; check against compressed_blocks, if there is space already -> put in there somehow
(define (compress_blocks input_blocks)
  (let loop [(compressed_blocks '())
	     (blocks input_blocks)]
    (cond
     [(null? blocks)
      (flatten (reverse compressed_blocks))]
     
     [(and (empty-block? (car blocks)) (empty-block? (car (reverse blocks))))
      (loop
       compressed_blocks
       (reverse (cdr (reverse blocks))))]
     [else
      (loop
       (cons (car blocks) compressed_blocks)
       (cdr blocks))])))


(define (update-checksum compressed_blocks)
  (apply + (map (λ (id index) (* id index))
		compressed_blocks
		(iota (length compressed_blocks)))))

;;; Part One ---------------------------------------------------------------------------------------

(define puzzle_input (get-string-all (open-input-file "/home/tomaz/code/advent-of-code-2024/day-09/guile_tomazgda/input")))

(display (update-checksum (compress_blocks (input->blocks puzzle_input))))


