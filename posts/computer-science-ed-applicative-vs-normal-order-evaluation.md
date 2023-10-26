---
title: Computer Science Ed - Applicative vs. Normal Order Evaluation
author: Chris
date: 10/26/2023 13:12:19 
tags: computer science, technology
---

I recently started reading [*Structure and Interpretation of Computer Programs*](https://sarabander.github.io/sicp/html/index.xhtml#SEC_Contents) (the first recommended book in the [Teach Yourself CS](www.teachyourselfcs.com) curriculum). I'm not even past the first section of the first chapter, and there are already concepts I'm coming across that never crossed my mind before, despite working with Python and Javascript for the last few years.

One concept I found interesting and yet difficult to grasp at first is the idea of the order in which computeres evaluate procedures. In SICP, they write of Scheme (a subset of the Lisp programming language) that it is an applicative-order language. That is,

>> All the arguments to Scheme procedures are evaluated when the procedure is applied. In contrast, normal-order languages dalay evaluation of procedure arguments until the actual argument values are needed.
--1.1.5, ["Applicative order versus normal order"](https://sarabander.github.io/sicp/html/1_002e1.xhtml#g_t1_002e1_002e5:~:text=Applicative%20order%20versus%20normal%20order)

The example problem used to confirm that Scheme is an applicative-order language is the definition of two procedures and a calling of the test procedure:

`
    (define (p) (p))
    (define (test x y)
        (if (= x 0)
        0
        y))
    (test 0 (p))
`

Because Scheme is an applicative-order language, the interpreter attempts to evaluate all the arguments within the test procedure *first* before the full procedure is applied. When it tries to do this, (p) is called infinitely because (p) calls itself. The interpreter can never finish calling the actual procedure we're attempting to call because it's trying to determine a true value for (p) before determining whether x = 0 or not.