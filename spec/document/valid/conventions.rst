Conventions
-----------

As in Core WebAssembly, a *validation* stage checks that a component
is well-formed, and only valid components may be instantiated.

Similarly to Core WebAssembly, a *type system* over the abstract
syntax of a component is used to specify which modules are valid, and
the rules governing the validity of a component are given in both
prose and formal mathematical notation.

.. _syntax-tyctx:
.. _syntax-coretyctx:

Contexts
~~~~~~~~

Validation rules for individual definitions are interpreted within a
particular *context*, which contains the information about the
surrounding component and environment needed to validae a particular
definition. The validation contexts used in the component model
contain the types of every definition in every index space currently
accessible (including the index spaces of parent components, which may
be accessed via :math:`\ATOUTER` aliases).

Concretely, a validation context is defined as a record with the
following abstract syntax:

.. math::
  \begin{array}{llcl}
  \production{(coretyctx)} & \coretyctx &::=&
    \{
      \begin{array}[t]{l@{~}ll}
        \CTCTYPES & \ecoredeftype^\ast, \\
        \CTCFUNCS & \core:functype^\ast, \\
        \CTCMODULES & \ecoremoduletype^\ast, \\
        \CTCINSTANCES & \ecoreinstancetype^\ast, \\
        \CTCTABLES & \core:tabletype^\ast, \\
        \CTCMEMS & \core:memtype^\ast, \\
        \CTCGLOBALS & \core:globaltype^\ast\} \\
      \end{array}\\
  \production{(tyctx)} & \tyctx &::=&
    \{
      \begin{array}[t]{l@{~}ll}
        \TCPARENT & \tyctx, \\
        \TCCORE & \coretyctx, \\
        \TCUVARS & \boundedtyvar^\ast, \\
        \TCEVARS & (\boundedtyvar, \edeftype)^\ast \\
        \TCRTYPES & \eresourcetype^\ast, \\
        \TCTYPES & \edeftype^\ast, \\
        \TCCOMPONENTS & \ecomponenttype^\ast, \\
        \TCINSTANCES & {\einstancetype^\dagger}^\ast, \\
        \TCFUNCS & \efunctype^\ast, \\
        \TCVALUES & \evaltypead^\ast, \} \\
      \end{array}\\
  \end{array}

Notation
~~~~~~~~

Both the formal and prose notation share a number of constructs:

* When writing a value of the abstract syntax, any component of the
  abstract syntax which has the form :math:`\X{nonterminal}^n`,
  :math:`\X{nonterminal}^\ast`, :math:`\X{nonterminal}^{+}`, or
  :math:`\X{nonterminal}^{?}`, we may write
  :math:`\overline{\dots_i}^n` to mean that this position is filled by
  a series of :math:`n` abstract values, named :math:`\dots_1` to
  :math:`\dots_n`.
