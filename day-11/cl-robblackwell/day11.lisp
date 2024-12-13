;;;; Advent of Code 2024 Day 11

(eval-when (:compile-toplevel :load-toplevel :execute)
  (ql:quickload :alexandria))

(defpackage :aoc
  (:use :cl :alexandria))

(in-package :aoc)

(defun integer-width (n)
  (if (< n 10) 1 (1+ (integer-width (floor n 10)))))

(defun rule (number)
  (if (eql number 0)
      1
      (let ((l (integer-width number)))
        (cond
          ((evenp l) (multiple-value-list (floor number (expt 10 (/ l 2)))))
          (t (* number 2024))))))

(defparameter *cache* (make-hash-table :test #'equal :size 1000000))

(defun num-stones (stone n)
  (let ((found (gethash (cons stone n) *cache*)))
    (cond
      (found found)
      ((= 0 n) 1)
      (t (let* ((stones (ensure-list (rule stone)))
                (l (apply #'+ (mapcar #'(lambda (x) (num-stones x (1- n))) stones))))
           (setf (gethash (cons stone n) *cache*) l))))))

(defun run (stones n)
  (apply #'+ (mapcar #'(lambda(x) (num-stones x n)) stones)))


;;(run '(4189 413 82070 61 655813 7478611 0 8) 25) 186203 (18 bits, #x2D75B)

;;(run '(4189 413 82070 61 655813 7478611 0 8) 75) 221291560078593 (48 bits, #xC94374D48D01)
