;; (defun get-file (filename)
;;    (with-open-file (stream filename)
;;         (loop for line = (read-line stream nil)
;;             while line
;;             collect line)))

;; (defun handle-file (filename)
;;     (with-open-file (stream filename)
;;         (do ((line (read-line stream nil)
;;                 (read-line stream nil)))
;;             ((null line))
;;             (print line))))

(defmacro while (condition &body body)
  `(loop while ,condition do (progn ,@body)))

(defun lcs (a b)
  (cond
    ((or (null a) (null b)) nil)
    ((eql (car a) (car b))
       (cons (car a) (lcs (cdr a) (cdr b))))
    (t (longest (lcs a (rest b)) (lcs (rest a) b)))))

(defun longest (a b)
  (if (> (length a) (length b)) a b))


(defun print-elements-of-list (list)
       "Print each element of LIST on a line of its own."
       (loop while list do
         (print (car list))
         (setq list (cdr list))))
     
     
(print-elements-of-list (lcs '(0 1 2 3 4) '(0 1 2 4 3)))

