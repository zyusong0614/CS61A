(define (caar x) (car (car x)))
(define (cadr x) (car (cdr x)))
(define (cdar x) (cdr (car x)))
(define (cddr x) (cdr (cdr x)))

;; Problem 15
;; Returns a list of two-element lists

(define (enumerate s)
  ; BEGIN PROBLEM 15
  (define (helper s index)
    (cond
      ((eq? s nil)
        nil
      )
      (else
        (define index (+ 1 index))
        (cons (list index (car s)) (helper (cdr s) index))
      )
    )
  ) (helper s -1)
)
  ; END PROBLEM 15

;; Problem 16

;; Merge two lists LIST1 and LIST2 according to ORDERED? and return
;; the merged lists.

(define (merge ordered? list1 list2)
  ; BEGIN PROBLEM 16
  (cond
    ((equal? list1 nil)
      list2
    )
    ((equal? list2 nil)
      list1
    )
    (else
      (if (ordered? (car list1) (car list2))
        (cons (car list1) (merge ordered? (cdr list1) list2))
        (cons (car list2) (merge ordered? list1 (cdr list2)))
      )
    )
  )
)
  ; END PROBLEM 16

