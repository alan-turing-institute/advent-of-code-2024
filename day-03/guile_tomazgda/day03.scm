(use-modules (ice-9 regex))
(use-modules (ice-9 textual-ports))

;; Part One ------------------------------------------------------------------------------

(define (file->string path) 
  (get-string-all (open-input-file path)))

;; A regular expressions that matches 'mul(a,b)' where a and b are two numbers from 0 to 1000
(define r (make-regexp "mul\\([0-9]?[0-9]{1,2},[0-9]?[0-9]{1,2}\\)"))

;; for each multiply-expression, return the product of its two numbers
(define (eval-mul str)
  (apply * (map string->number (string-split (match:substring (string-match "[0-9]?[0-9]{1,2},[0-9]?[0-9]{1,2}" str)) #\,))))

;; given a string, evaluate each multiply-expression and return their sum
(define (eval-mul-str str)
  (apply + (map eval-mul (map match:substring (list-matches r str)))))

;; ---------------------------------------------------------------------------------------

(define (solve-part-one path) (eval-mul-str (file->string path)))

;; Part Two ------------------------------------------------------------------------------

;; catch do() and don't() in regex this time
(define r-prime (make-regexp "do\\(\\)|don't\\(\\)|mul\\([0-9]?[0-9]{1,2},[0-9]?[0-9]{1,2}\\)"))

;; remove invalid mul(a,b)s 
(define (seperate-donts old_list new_list valid_mul)
  (if (null? old_list)
      (reverse new_list)
      (if (equal? (car old_list) "do()")
	  (seperate-donts (cdr old_list) new_list #t)
	  (if (equal? (car old_list) "don't()")
	      (seperate-donts (cdr old_list) new_list #f)
	      (if valid_mul
		  (seperate-donts (cdr old_list) (cons (car old_list) new_list) valid_mul)
		  (seperate-donts (cdr old_list) new_list valid_mul))))))

(define (solve-part-two path) (apply + (map eval-mul (seperate-donts (map match:substring (list-matches r-prime (file->string path))) '() #t))))

;; ---------------------------------------------------------------------------------------

;; print results
(display (string-append "Part One Result: \n"
			(number->string (solve-part-one "input"))
			"\nPart Two Result: \n"
			(number->string (solve-part-two "input"))))

