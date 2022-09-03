.. index:: ! abstract syntax

Conventions
-----------

The WebAssembly component specification defines a language for
specifying components, which, like the WebAssembly core language, may
be represented by multiple complete representations (e.g. the
:ref:`binary format <binary>` and the :ref:`text format <text>`). In
order to avoid duplication, the static and dynamic semantics of the
WebAssembly component model are instead defined over an abstract
syntax.

.. index:: ! grammar notation, notation
   single: abstract syntax; grammar
   pair: abstract syntax; noatation
.. _grammar:

The following conventions are adopted in defining grammar rules for abstract syntax.

* Terminal symbols (atoms) are written in sans-serif font: :math:`\K{i32}, \K{end}`.

* Nonterminal symbols are written in italic font: :math:`\X{valtype}, \X{instr}`.

* :math:`A^n` is a sequence of :math:`n\geq 0` iterations  of :math:`A`.

* :math:`A^\ast` is a possibly empty sequence of iterations of :math:`A`.
  (This is a shorthand for :math:`A^n` used where :math:`n` is not relevant.)

* :math:`A^+` is a non-empty sequence of iterations of :math:`A`.
  (This is a shorthand for :math:`A^n` where :math:`n \geq 1`.)

* :math:`A^?` is an optional occurrence of :math:`A`.
  (This is a shorthand for :math:`A^n` where :math:`n \leq 1`.)

* Productions are written :math:`\X{sym} ::= A_1 ~|~ \dots ~|~ A_n`.

* Large productions may be split into multiple definitions, indicated by ending the first one with explicit ellipses, :math:`\X{sym} ::= A_1 ~|~ \dots`, and starting continuations with ellipses, :math:`\X{sym} ::= \dots ~|~ A_2`.

* Some productions are augmented with side conditions in parentheses, ":math:`(\iff \X{condition})`", that provide a shorthand for a combinatorial expansion of the production into many separate cases.

* If the same meta variable or non-terminal symbol appears multiple times in a production, then all those occurrences must have the same instantiation.
  (This is a shorthand for a side condition requiring multiple different variables to be equal.)
