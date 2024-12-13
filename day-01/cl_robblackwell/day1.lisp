;;;; Advent of Code 2024 Day 1

(eval-when (:compile-toplevel :load-toplevel :execute)
  (ql:quickload :alexandria))

(defpackage :aoc
  (:use :cl :alexandria))

(in-package :aoc)

(defun safesort (sequence predicate)
  "Non destructive sort."
  (let ((copy (copy-seq sequence)))
    (sort copy predicate)))

(defun aoc1 (list1 list2)
  (apply #'+ (mapcar #'(lambda(x y) (abs (- x y))) (safesort list1 #'<) (safesort list2 #'<))))

(defparameter *list1* '(3 4 2 1 3 3))
(defparameter *list2* '(4 3 5 3 9 3))

(aoc1 *list1* *list2*) ; => 11 (4 bits, #xB, #o13, #b1011)

(defparameter *data*
  (with-open-file (stream "day1.txt" :direction :input)
    (loop for line = (read-line stream nil nil)
          while line
          collect (with-input-from-string (in line)
                    (list (read in) (read in))))))

(let ((list1 (mapcar #'first  *data*))
      (list2 (mapcar #'second *data*)))
  (aoc1 list1 list2)) ; => 1506483 (21 bits, #x16FCB3)

(defun aoc2(list1 list2)
  (apply #'+ (mapcar #'(lambda (x) (* x (count x list2))) list1)))

(let ((list1 (mapcar #'first  *data*))
      (list2 (mapcar #'second *data*)))
  (aoc2 list1 list2)) ; => 23126924 (25 bits, #x160E38C)
