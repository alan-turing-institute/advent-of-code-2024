;;;; Advent of Code 2024 Day 2

(eval-when (:compile-toplevel :load-toplevel :execute)
  (ql:quickload :alexandria))

(defpackage :aoc
  (:use :cl :alexandria))

(in-package :aoc)

(defparameter *data1* '((7 6 4 2 1)
                       (1 2 7 8 9)
                       (9 7 6 2 1)
                       (1 3 2 4 5)
                       (8 6 4 4 1)
                       (1 3 6 7 9)))

(defun increasingp (list)
  (or (eql (length list) 1)
      (and (< (first list) (second list)) (increasingp (rest list)))))

(defun decreasingp (list)
  (or (eql (length list) 1)
      (and (> (first list) (second list)) (decreasingp (rest list)))))

(defun intervals (numbers)
  (mapcar  #'(lambda (x y) (abs (- x y))) (cdr numbers) numbers))

(defun safep (list)
  (and (or (increasingp list) (decreasingp list)) ( < (apply #'max (intervals list)) 4)))

(count t (mapcar #'safep *data1*)) ; => 2 (2 bits, #x2, #o2, #b10)

(defun read-ints (string)
  (with-input-from-string (stream string)
    (loop for num = (read stream nil :end)
          until (eq num :end)
          collect num)))

(defparameter *data*
  (with-open-file (stream "day2.txt" :direction :input)
    (loop for line = (read-line stream nil nil)
          while line
          collect (read-ints line))))


(count t (mapcar #'safep *data*)) ; => 631 (10 bits, #x277)

;;; Part 2

(defun remove-one-element (list)
  (loop for i from 0 below (length list)
        collect (append (subseq list 0 i)
                        (subseq list (1+ i)))))

(defun safep-with-dampener (list)
  (some #'identity (mapcar #'safep (remove-one-element list))))

(count t (mapcar #'safep-with-dampener *data*)) ; => 665 (10 bits, #x299)
