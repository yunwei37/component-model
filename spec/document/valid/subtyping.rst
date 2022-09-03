Subtyping
---------

Subtyping defines when a value of one type may be used when a value of
another type is expected.

TODO: This is not complete, pending further discussion, especially in
re the special treatment that may or may not be required or specialized value types.

Value types
~~~~~~~~~~~

Reflexivity
...........

* Any value type is a subtype of itself

.. math::
  \frac{
  }{
    \evaltype \subtypeof \evaltype
  }

Numeric types
.............

* :math:`\EVTS8` is a subtype of :math:`\EVTS16`, :math:`\EVTS32`, and
  :math:`\EVTS64`.

* :math:`\EVTS16` is a subtype of :math:`\EVTS32` and :math:`\EVTS64`.

* :math:`\EVTS32` is a subtype of :math:`\EVTS64`.

* :math:`\EVTU8` is a subtype of :math:`\EVTU16`, :math:`\EVTU32`,
  :math:`\EVTU64`, :math:`\EVTS16`, :math:`\EVTS32`, and
  :math:`\EVTS64`.

* :math:`\EVTU16` is a subtype of :math:`\EVTU32`, :math:`\EVTU64`,
  :math:`\EVTS32`, and :math:`\EVTS64`.

* :math:`\EVTU32` is a subtype of :math:`\EVTU64` and :math:`\EVTS64`.

* :math:`\EVTFLOAT32` is a subtype of :math:`\EVTFLOAT64`.

.. math::
  \frac{
    m > n
  }{
    \K{s}n \subtypeof \K{s}m
  }

.. math::
  \frac{
    m > n
  }{
    \K{u}n \subtypeof \K{u}m
  }

.. math::
  \frac{
    m > n
  }{
    \K{u}n \subtypeof \K{s}m
  }

.. math::
  \frac{
  }{
    \EVTFLOAT32 \subtypeof \EVTFLOAT64
  }

Records
.......

* A type :math:`\EVTRECORD~\overline{{\erecordfield}_i}` is a subtype
  of a type :math:`\EVTRECORD~\overline{{\erecordfield'}_j}` if, for
  each named field of the latter type, a field with the same name is
  present in the former, and the type of the field in the former is a
  subtype of the type of the field in the latter.

Todo: We may need to move despecialization later because of subtyping?

.. math::
  \frac{
    \begin{aligned}
    \forall j, \exists i,&{\erecordfield}_i.\ERFNAME = {\erecordfield'}_j.\ERFNAME\\ \land{}& {\erecordfield}_i.\ERFTYPE \subtypeof {\erecordfield}_j.\ERFTYPE
    \end{aligned}
  }{
    \EVTRECORD~\overline{{\erecordfield}_i} \subtypeof
    \EVTRECORD~\overline{{\erecordfield'}_j}
  }

Variants
........

* A type :math:`\EVTVARIANT~\overline{{\evariantcase}_i}` is a subtype
  of a type :math:`\EVTVARIANT~\overline{{\evariantcase'}_j}` if, or
  each named case of the former type, either:

  + A case of the same name exists in the latter type, such that the
    type of the field in the former is a subtype of the type of the
    field in the latter; or

  + No case of the same name exists in the latter type, and the case
    in the former contains a :math:`\EVCREFINES`.

.. math::
  \frac{
    \begin{alignedat}{2}
    \forall i,&&(\exists j,&{\evariantcase'}_j.\EVCNAME = {\evariantcase}_i.\EVCNAME\\&& \land{}& {\evariantcase}_i \subtypeof {\evariantcase'}_j)\\
    \lor{}&&(\forall j,&{\evariantcase'}_j.\EVCNAME \neq {\evariantcase}_i.\EVCNAME\\&& \land{}&\exists \name, {\evariantcase}_i.\EVCREFINES = \name)
    \end{alignedat}
  }{
    \EVTVARIANT~\overline{{\evariantcase}_i} \subtypeof
    \EVTVARIANT~\overline{{\evariantcase'}_j}
  }

Lists
.....

* A type :math:`\EVTLIST~\evaltype` is a subtype of a type
  :math:`\EVTLIST~\evaltype'` if :math:`\evaltype` is a subtype of
  :math:`\evaltype'`

.. math::
  \frac{
    \evaltype \subtypeof \evaltype'
  }{
    \EVTLIST~\evaltype \subtypeof \EVTLIST~\evaltype'
  }

Result types
~~~~~~~~~~~~

* A result type of the form :math:`\evaltype` is a subtype of a result
  type of te form :math:`\evaltype'` if :math:`\evaltype` is a subtype
  of :math:`\evaltype'`.

  .. math::
    \frac{
      \evaltype \subtypeof \evaltype'
    }{
      \evaltype \subtypeof \evaltype'
    }

* A result type of the form :math:`\overline{\{ \ERTNAME~\name_i,
  \ERTTYPE~{\evaltype}_i \}}` is a subtype of a result type of the form
  :math:`\overline{\{ \ERTNAME~\name'_j, \ERTTYPE~{\evaltype'}_j \}}`
  when:

  + For each :math:`\name'_j`, there is some :math:`i` such that
    :math:`\name'_j = \name_i` and :math:`{\evaltype}_i \subtypeof
    {\evaltype}'_j`.

  .. math::
    \frac{
      \forall j, \exists i, \name_i = \name'_j \land {\evaltype}_i \subtypeof {\evaltype}'_j
    }{
      \overline{\{ \ERTNAME~\name_i, \ERTTYPE~{\evaltype}_i \}}
      \subtypeof
      \overline{\{ \ERTNAME~\name'_j, \ERTTYPE~{\evaltype'}_j \}}
    }

Function types
~~~~~~~~~~~~~~

* A function type :math:`{\eresulttype}_1 \to {\eresulttype}_2` is a
  subtype of a function :math:`{\eresulttype'}_1 \to
  {\eresulttype'}_2` if :math:`{\eresulttype'}_1 \subtypeof
  {\eresulttype}_1` and :math:`{\eresulttype}_2 \subtypeof
  {\eresulttype'}_2`.

.. math::
  \frac{
    \begin{array}{@{}c@{}}
    {\eresulttype'}_1 \subtypeof {\eresulttype}_1\\
    {\eresulttype}_2 \subtypeof {\eresulttype'}_2
    \end{array}
  }{
    {\eresulttype}_1 \to {\eresulttype}_2
    \subtypeof
    {\eresulttype'}_1 \to {\eresulttype'}_2
  }

Type bound
~~~~~~~~~~

:math:`\ETBEQ~\edeftype`
........................

* A type bound :math:`\ETBEQ~\edeftype` is a subtype of
  :math:`\ETBEQ~\edeftype'` if :math:`\edeftype` is a subtype of
  :math:`\edeftype'`.

.. math::
  \frac{
    \edeftype \subtypeof \edeftype'
  }{
    \ETBEQ~\edeftype \subtypeof \ETBEQ~\edeftype'
  }

Extern descriptors
~~~~~~~~~~~~~~~~~~

:math:`\EEMDCOREMODULE~\ecoremoduletype`
........................................

* A extern descriptor :math:`\EEMDCOREMODULE~\ecoremoduletype` is a
  subtype of :math:`\EEMDCOREMODULE~\ecoremoduletype'` if
  :math:`\ecoremoduletype` is a subtype of :math:`\ecoremoduletype'`.

.. math::
  \frac{
    \ecoremoduletype' \subtypeof \coremoduletype'
  }{
    \EEMDCOREMODULE~\ecoremoduletype \subtypeof
    \EEMDCOREMODULE~\ecoremoduletype'
  }

:math:`\EEMDFUNC~\efunctype`
............................

* An extern descriptor :math:`\EEMDFUNC~\efunctype` is a subtype of
  :math:`\EEMDFUNC~\efunctype'` if :math:`\efunctype` is a subtype of
  :math:`\efunctype'`.

.. math::
  \frac{
    \efunctype \subtypeof \efunctype'
  }{
    \EEMDFUNC~\efunctype \subtypeof \EEMDFUNC~\efunctype'
  }

:math:`\EEMDVALUE~\evaltype`
............................

* An extern descriptor :math:`\EEMDVALUE~\evaltype` is a subtype of
  :math:`\EEMDVALUE~\evaltype'` if :math:`\evaltype` is a subtype of
  :math:`\evaltype'`.

.. math::
  \frac{
    \evaltype \subtypeof \evaltype'
  }{
    \EEMDVALUE~\evaltype \subtypeof \EEMDVALUE~\evaltype'
  }

:math:`\EEMDTYPE~\etypebound`
.............................

* An extern descriptor :math:`\EEMDTYPE~\etypebound` is a subtype of
  :math:`\EEMDTYPE~\etypebound'` if :math:`\etypebound` is a subtype of
  :math:`\etypebound'`.

.. math::
  \frac{
    \etypebound \subtypeof \etypebound'
  }{
    \EEMDTYPE~\etypebound \subtypeof \EEMDTYPE~\etypebound'
  }

:math:`\EEMDINSTANCE~\einstancetype`
....................................

* An extern descriptor :math:`\EEMDINSTANCE~\einstancetype` is a subtype of
  :math:`\EEMDINSTANCE~\einstancetype'` if :math:`\einstancetype` is a subtype of
  :math:`\einstancetype'`.

.. math::
  \frac{
    \einstancetype \subtypeof \einstancetype'
  }{
    \EEMDINSTANCE~\einstancetype \subtypeof \EEMDINSTANCE~\einstancetype'
  }

:math:`\EEMDCOMPONENT~\ecomponenttype`
......................................

* An extern descriptor :math:`\EEMDCOMPONENT~\ecomponenttype` is a subtype of
  :math:`\EEMDCOMPONENT~\ecomponenttype'` if :math:`\ecomponenttype` is a subtype of
  :math:`\ecomponenttype'`.

.. math::
  \frac{
    \ecomponenttype \subtypeof \ecomponenttype'
  }{
    \EEMDCOMPONENT~\ecomponenttype \subtypeof \EEMDCOMPONENT~\ecomponenttype'
  }


Instance types
~~~~~~~~~~~~~~

* An instance type :math:`\overline{{\eexterndecl}_i}` is a subtype of
  an instance type :math:`\overline{{\eexterndecl'}_j}` if:

  + For each :math:`j`, there exists some :math:`i` such that
    :math:`{\eexterndecl}_i.\EEDNAME = {\eexterndecl'}_j.\EEDNAME` and
    :math:`{\eexterndecl}_i.\EEDDESC \subtypeof {\eexterndecl'}_j.\EEDDESC`.

.. math::
  \frac{
    \forall j, \exists i, {\eexterndecl}_i.\EEDNAME = {\eexterndecl'}_j.\EEDNAME \land {\eexterndecl}_i.\EEDDESC \subtypeof {\eexterndecl'}_j.\EEDDESC.
  }{
    \overline{{\eexterndecl}_i} \subtypeof \overline{{\eexterndecl'}_j}
  }

Component types
~~~~~~~~~~~~~~~

* A component type :math:`\overline{{\eexterndecl}_i} \to
  \einstancetype` is a subtype of a
  :math:`\overline{{\eexterndecl'}_j} \to \einstancetype'` if:

  + For each :math:`i`, there exists some :math:`j`, such that
    :math:`{\eexterndecl'}_j.\EEDNAME = {\eexterndecl}_i.\EEDNAME` and
    :math:`{\eexterndecl'}_j.\EEDDESC \subtypeof {\eexterndecl}_i.\EEDDESC`;
    and

  + :math:`\einstancetype \subtypeof \einstancetype'`

.. math::
  \frac{
    \begin{array}{@{}c@{}}
    \forall i, \exists j, {\eexterndecl'}_j.\EEDNAME = {\eexterndecl}_i.\EEDNAME \land {\eexterndecl'}_j.\EEDDESC \subtypeof {\eexterndecl}_i.\EEDDESC\\
    \einstancetype \subtypeof \einstancetype'
    \end{array}
  }{
    \overline{{\eexterndecl}_i} \to \einstancetype
    \subtypeof
    \overline{{\eexterndecl'}_j} \to \einstancetype'
  }
