Types
-----

During validation, the abstract syntax types described above are
*elaborated* into types of a different structure, which are easier to
work with. Elaborated types are different from the original abstract
syntax types in three major aspects:

* They do not contain any indirections through type index spaces:
  since recursive types are explicitly not permitted by the component
  model, it is possible to simply inline all such indirections.

* Due to the above, instance and component types do not contain any
  embedded declarations; the type sharing that necesstated the use of
  type alias declarations is replaced with explicit binders and type
  variables.

* Value types have been *despecialised*: the value type constructors
  :math:`\VTTUPLE`, :math:`\VTFLAGS`, :math:`\VTENUM`,
  :math:`\VTOPTION`, :math:`\VTUNION`, :math:`\VTRESULT`, and
  :math:`\VTSTRING` have been replaced by equivalent types.

This elaboration also ensures that the type definitions themselves
have valid structures, and so may be considered as validation on
types.

.. _syntax-evaltype:
.. _syntax-evaltypead:
.. _elaborate-PVTtoEVT:

Primitive value types
~~~~~~~~~~~~~~~~~~~~~

Any :math:`\primvaltype`, :math:`\defvaltype`, or :math:`\valtype`
elaborates to a a :math:`\evaltype`. The syntax of :math:`\evaltype`
is specified by parts over the next several sections, as it becomes
relevant.

.. math::
  \begin{array}{llcl}
  \production{(evaltype)} & \evaltype &::=&
    \EVTBOOL\\&&|&
    \EVTS8 | \EVTU8 | \EVTS16 | \EVTU16 | \EVTS32 | \EVTU32 | \EVTS64 | \EVTU64\\&&|&
    \EVTFLOAT32 | \EVTFLOAT64\\&&|&
    \EVTCHAR\\&&|&
    \EVTLIST~\evaltype\\&&|&
    \dots\\
  \end{array}

Because values are used linearly, values in the context must be
associated with information about whether they are alive or dead. This
is accomplished by assigning them types from :math:`\evaltypead`:

.. math::
  \begin{array}{llcl}
  \production{(evaltypead)} & \evaltypead &::=&
    \evaltype\\&&|&
    \evaltype^\dagger
  \end{array}

:math:`\VTSTRING`
.................

* The primitive value type :math:`\VTSTRING` elaborates to the
  :math:`\evaltype` of :math:`\EVTLIST~\EVTCHAR`.

.. math::
  \frac{
  }{
    \tyctx \vdashh!PVTtoEVT \VTSTRING \leadstoh!PVTtoEVT \EVTLIST~\EVTCHAR
  }

:math:`\primvaltype` other than :math:`\VTSTRING`
.................................................

* Any :math:`\primvaltype` other than :math:`\VTSTRING` elaborates to
  the :math:`\evaltype` of the same name.

.. math::
  \frac{
    \primvaltype \neq \VTSTRING
  }{
    \tyctx \vdashh!PVTtoEVT \primvaltype \leadstoh!PVTtoEVT \primvaltype
  }

.. _syntax-erecordfield:
.. _elaborate-RFtoERF:

Record fields
~~~~~~~~~~~~~

Any :math:`\recordfield` elaborates to a :math:`\erecordfield` with
the following abstract syntax:

.. math::
  \begin{array}{llcl}
  \production{(erecordfield)} & \erecordfield &::=&
    \{ \ERFNAME~\name, \ERFTYPE~\evaltype \}\\
  \end{array}

* The type of the record field must elaborate to some :math:`\evaltype`

* Then the record field elaborates to an :math:`\erecordfield` of the
  same name with the type :math:`\evaltype`.

.. math::
  \frac{
    \tyctx \vdashh!VTtoEVT \valtype \leadstoh!VTtoEVT \evaltype
  }{
    \tyctx \vdashh!RFtoERF \{ \RFNAME~\name, \RFTYPE~\valtype \}
    \leadstoh!RFtoERF \{ \ERFNAME~\name, \ERFTYPE~\evaltype \}
  }

.. _syntax-evariantcase:
.. _syntax-vcctx:
.. _elaborate-VCtoEVC:

Variant cases
~~~~~~~~~~~~~

Because validation must ensure that a variant case which refines
another case has a compatible type, a variant case elaborates to an
:math:`\evariantcase` in a special context :math:`\vcctx`:

.. math::
  \begin{array}{llcl}
  \production{(vcctx)} & \vcctx &::=&
  \{ \VCCCTX~\tyctx, \VCCCASES~\evariantcase^{*} \}\\
  \production{(evariantcase)} & \evariantcase &::=&
    \{ \EVCNAME~\name, \EVCTYPE~\evaltype^?, \EVCREFINES~\u32^? \}\\
  \end{array}

* If the variant case contains a type, it must elaborate to some :math:`\evaltype`.

* If an index :math:`i` is present in the :math:`\VCREFINES` record of
  the variant case type, then :math:`\vcctx.\VCCCASES[i]` must be
  present, and:

  + If the variant case does not contain a type,
    :math:`\vcctx.\VCCCASES[i]` must not contain a type.

  + If the variant case contains a type, then
    :math:`\vcctx.\VCCCASES[i]` must also contain an elaborated type,
    and the elaborated form of the cases' type must be a subtype of
    that type.

* Then the variant case elaborates to an :math:`\erecordfield` of the
  same name, with:

  + If the variant case does not contain a type, then no type.

  + If the variant case does contain a type, then the
    :math:`\evaltype` to which it elaborates.

  + If the variant case does not contain a refines index, then no
    refines name.

  + If the variant case does contain a refines index :math:`i`, then a
    refines name of :math:`\vcctx.\VCCCASES[i].\EVCNAME`.

.. math::
  \frac{
    \begin{array}{@{}c@{}}
    \forall i, \vcctx.\VCCCTX \vdashh!VTtoEVT \valtype_i \leadstoh!VTtoEVT {\evaltype}_i\\
    \forall j, \vcctx.\VCCCASES[\u32_j] = \{ \EVCNAME~\name_j, \EVCTYPE~\overline{{\evaltype'}_k}, \dots \} \land \forall i, {\evaltype}_i \subtypeof {\evaltype'}_i
    \end{array}
  }{
    \vcctx \vdashh!VCtoEVC \{ \VCNAME~\name, \VCTYPE~\overline{\valtype_i}, \VCREFINES~\overline{\u32_j} \}
    \leadstoh!VCtoEVC \{ \EVCNAME~\name, \EVCTYPE~\overline{{\evaltype}_i}, \VCREFINES~\overline{\name_j} \}
  }

.. _syntax-evaltype2:
.. _syntax-refscope:
.. _elaborate-DVTtoEVT:

Definition value types
~~~~~~~~~~~~~~~~~~~~~~

A definition value type elaborates to a :math:`\evaltype`. The syntax
of :math:`\evaltype` is broader than shown earlier:

.. math::
  \begin{array}{llcl}
  \production{(evaltype2)} & \evaltype &::=&
    \dots\\&&|&
    \EVTRECORD~\erecordfield^{+}\\&&|&
    \EVTVARIANT~\evariantcase^{+}\\&&|&
    \EVTOWN~\edeftype\\
    \EVTREF~\refscope~\edeftype\\
  \end{array}

:math:`\VTPRIM~\primvaltype`
............................

* The primitive value type :math:`\primvaltype` must elaborate to some
  :math:`\evaltype`.

* Then the definition value type :math:`\VTPRIM~\primvaltype`
  elaborates to the the the same :math:`\evaltype`.

.. math::
  \frac{
    \tyctx \vdashh!PVTtoEVT \primvaltype \leadstoh!PVTtoEVT \evaltype
  }{
    \tyctx \vdashh!DVTtoEVT \VTPRIM~\primvaltype \leadstoh!DVTtoEVT \evaltype
  }

:math:`\VTRECORD~\recordfield^{+}`
..................................

* Each record field declaration :math:`\recordfield_i` must elaborate
  to some :math:`{\erecordfield}_i`.

* The :math:`\ERFNAME`\ s of the :math:`{\erecordfield}_i` must all be
  distinct.

* Then the definition value type :math:`\VTRECORD~\overline{\recordfield_i}^n`
  elaborates to :math:`\EVTRECORD~\overline{{\erecordfield}_i}^n`.

.. math::
  \frac{
    \begin{array}{@{}c@{}}
    \forall i, \tyctx \vdashh!RFtoERF \recordfield_i \leadstoh!RFtoERF {\erecordfield}_i\\
    \forall i j, {\erecordfield}_i.\ERFNAME = {\erecordfield}_j.\ERFNAME \Rightarrow i = j
    \end{array}
  }{
    \tyctx \vdashh!DVTtoEVT \VTRECORD~\overline{{\recordfield}_i}^n
    \leadstoh!DVTtoEVT \EVTRECORD~\overline{{\erecordfield}_i}^n
  }

:math:`\VTVARIANT~\variantcase^{+}`
...................................

* Each variant case declaration :math:`\variantcase_i` must elaborate
  to some :math:`{\evariantcase}_i`, in a variant-case context
  :math:`\vcctx_i` where:

  + :math:`\vcctx_i.\VCCCTX = \Gamma`

  + :math:`\vcctx_i.\VCCCASES = {\evariantcase}_1, \dots,
    {\evariantcase}_{i-1}`

* The :math:`\EVCNAME`\ s of the :math:`{\evariantcase}_i` must all be
  distinct.

* Then the definition value type :math:`\VTVARIANT~\overline{\variantcase_i}^n`
  elaborates to :math:`\EVTVARIANT~\overline{{\evariantcase}_i}^n`.

.. math::
  \frac{
    \begin{array}{@{}c@{}}
    \forall i, \{ \VCCCTX~\Gamma, \VCCCASES~{\evariantcase}_1,\dots,{\evariantcase}_{i-1} \}  \vdashh!VCtoEVC \variantcase_i \leadstoh!VCtoEVC {\evariantcase}_i\\
    \forall i, j {\evariantcase}_i.\EVCNAME = {\evariantcase}_j.\EVCNAME \Rightarrow i = j
    \end{array}
  }{
    \tyctx \vdashh!DVTtoEVT \VTVARIANT~\overline{\variantcase_i}^n
    \leadstoh!DVTtoEVT \EVTVARIANT~\overline{{\evariantcase}_i}^n
  }

:math:`\VTLIST~\valtype`
........................

* The list element type :math:`\valtype` must elaborate to some
  :math:`\evaltype`.

* Then the definition value type :math:`\VTLIST~\valtype` elaborates
  to :math:`\EVTLIST~\evaltype`.

.. math::
  \frac{
    \tyctx \vdashh!VTtoEVT \valtype \leadstoh!VTtoEVT \evaltype
  }{
    \tyctx \vdashh!DVTtoEVT \VTLIST~\valtype \leadstoh!DVTtoEVT \EVTLIST~\evaltype
  }

:math:`\VTTUPLE~\overline{\valtype_i}`
......................................

* Each tuple element type :math:`\valtype_i` must elaborate to some
  :math:`{\evaltype}_i`.

* Then the definition value type
  :math:`\VTTUPLE~\overline{\valtype_i}` elaborates to
  :math:`\EVTRECORD~\overline{\{\ERFNAME~''i'',\ERFTYPE~{\evaltype}_i\}}`.

.. math::
  \frac{
    \forall i, \tyctx \vdashh!VTtoEVT \valtype_i \leadstoh!VTtoEVT {\evaltype}_i
  }{
    \tyctx \vdashh!DVTtoEVT \VTTUPLE~\overline{\valtype_i}
    \leadstoh!DVTtoEVT \EVTRECORD~\overline{\{\ERFNAME~''i'',\ERFTYPE~{\evaltype}_i\}}
  }

:math:`\VTFLAGS~\overline{\name_i}`
...................................

* The definition value type :math:`\VTFLAGS~\overline{\name_i}`
  elaborates to :math:`\VTRECORD~\overline{\{\ERFNAME~\name_i,
  \ERFTYPE~\EVTBOOL\}}`

.. math::
  \frac{
  }{
    \tyctx \vdashh!DVTtoEVT \VTFLAGS~\overline{\name_i}
    \leadstoh!DVTtoEVT \EVTRECORD~\overline{\{\ERFNAME~\name_i, \ERFTYPE~\EVTBOOL\}}
  }

:math:`\VTENUM~\overline{\name_i}`
..................................

* The definition value type :math:`\VTENUM~\overline{\name_i}`
  elaborates to :math:`\VTVARIANT~\overline{\{\EVCNAME~\name_i\}}`.

.. math::
  \frac{
  }{
    \tyctx \vdashh!DVTtoEVT \VTENUM~\overline{\name_i}
    \leadstoh!DVTtoEVT \VTVARIANT~\overline{\{\EVCNAME~\name_i\}}
  }

:math:`\VTOPTION~\valtype`
..........................

* The type contained in the option :math:`\valtype` must elaborate to
  some :math:`\evaltype`.

* Then the definition value type :math:`\VTOPTION~\valtype` elaborates
  to :math:`\EVTVARIANT~\{ \EVCNAME~''none'' \}~\{ \EVCNAME~''some'',
  \EVCTYPE~\evaltype \}`.

.. math::
  \frac{
    \tyctx \vdashh!VTtoEVT \valtype \leadstoh!VTtoEVT \evaltype
  }{
    \tyctx \vdashh!DVTtoEVT \VTOPTION~\valtype
    \leadstoh!DVTtoEVT \EVTVARIANT~\{ \EVCNAME~''none'' \}~\{ \EVCNAME~''some'', \EVCTYPE~\evaltype \}
  }

:math:`\VTUNION~\overline{\valtype_i}`
......................................

* Each value type `\valtype_i` must elaborate to some :math:`{\evaltype}_i`.

* Then the definition value type
  :math:`\VTUNION~\overline{\valtype_i}` elaborates to
  :math:`\EVTVARIANT~\overline{\{\EVCNAME~''i'', \EVCTYPE~{\evaltype}_i\}}`.

.. math::
  \frac{
    \forall i, \tyctx \vdashh!VTtoEVT \valtype_i \leadstoh!VTtoEVT {\evaltype}_i
  }{
    \tyctx \vdashh!DVTtoEVT \VTUNION~\overline{\valtype_i}
    \leadstoh!DVTtoEVT \EVTVARIANT~\overline{\{\EVCNAME~''i'', \EVCTYPE~{\evaltype}_i\}}
  }

:math:`\VTRESULT~\overline{\valtype_i}~\overline{\valtype'_j}`
..............................................................

* Each value type :math:`\valtype_i` must elaborate to some :math:`{\evaltype}_i`.

* Each value type :math:`\valtype'_j` must elaborate to some
  :math:`{\evaltype}'_j`.

* Then the definition value type
  :math:`\VTRESULT~\overline{\valtype_i}~\overline{\valtype'_j}`
  elaborates to :math:`\EVTVARIANT~\{\EVCNAME~''ok'', \EVCTYPE~\overline{{\evaltype}_i}\}~\{\EVCNAME~''error'', \EVCTYPE~\overline{{\evaltype'}_j}\}`.

.. math::
  \frac{
    \begin{array}{@{}c@{}}
    \forall i, \tyctx \vdashh!VTtoEVT \valtype_i \leadstoh!VTtoEVT {\evaltype}_i\\
    \forall j, \tyctx \vdashh!VTtoEVT \valtype'_j \leadstoh!VTtoEVT {\evaltype'}_j\\
    \end{array}
  }{
    \begin{aligned}
    \tyctx\vdashh!DVTtoEVT{}&\VTRESULT~\overline{\valtype_i}~\overline{\valtype'_j}\\
    \leadstoh!DVTtoEVT{}&\EVTVARIANT~\{\EVCNAME~''ok'', \EVCTYPE~\overline{{\evaltype}_i}\}~\{\EVCNAME~''error'', \EVCTYPE~\overline{{\evaltype'}_j}\}\\
    \end{aligned}
  }

:math:`\VTOWN~\typeidx`
.......................

* The type :math:`\tyctx.\TCTYPES[\typeidx]` must be defined in the
  context, and must be a subtype of :math:`\K{resource}`.

* Then the definition value type :math:`\VTOWN~\typeidx` elaborates
  to :math:`\EVTOWN~\evaltype`.

.. math::
  \frac{
    \begin{array}{@{}c@{}}
    \tyctx.\TCTYPES[\typeidx] = \evaltype\\
    \evaltype \subtypeof \K{resource}\\
    \end{array}
  }{
    \tyctx \vdashh!DVTtoEVT \VTOWN~\typeidx \leadstoh!DVTtoEVT \EVTOWN~\evaltype
  }

:math:`\VTBORROW~\typeidx`
..........................

* The type :math:`\tyctx.\TCTYPES[\typeidx]` must be defined in the
  context, and must be a subtype of :math:`\K{resource}`.

* Then the definition value type :math:`\VTBORROW~\typeidx` elaborates
  to :math:`\EVTREF~\RSCALL~\evaltype`.

.. math::
  \frac{
    \begin{array}{@{}c@{}}
    \tyctx.\TCTYPES[\typeidx] = \evaltype\\
    \evaltype \subtypeof \K{resource}\\
    \end{array}
  }{
    \tyctx \vdashh!DVTtoEVT \VTBORROW~\typeidx \leadstoh!DVTtoEVT \EVTREF~\RSCALL~\evaltype
  }

.. _elaborate-VTtoEVT:

Value types
~~~~~~~~~~~

:math:`\primvaltype`
....................

* A value type of the form :math:`\primvaltype` must be a
  :math:`\primvaltype` which elaborates to some :math:`\evaltype`.
* Then the value type elaborates to the same :math:`\evaltype`.

.. math::
  \frac{
    \tyctx \vdashh!PVTtoEVT \primvaltype \leadstoh!PVTtoEVT \evaltype
  }{
    \tyctx \vdashh!VTtoEVT \primvaltype \leadstoh!VTtoEVT \evaltype
  }

:math:`\typeidx`
................

* The type :math:`\tyctx.\TCTYPES[\typeidx]` must be defined in the
  context.

* Then the value type :math:`\typeidx` elaborates to
  :math:`\tyctx.\TCTYPES[\typeidx]`.

.. math::
  \frac{
  }{
    \tyctx \vdashh!VTtoEVT \typeidx \leadstoh!VTtoEVT \tyctx.\TCTYPES[\typeidx]
  }

.. _syntax-evaltypepos:
.. _elaborate-EVT:

Value type well-formedness
~~~~~~~~~~~~~~~~~~~~~~~~~~

Since certain value types cannot appear in certain places (most
notably, :math:`\EVTREF~\RSCALL` may not appear anywhere save a
function parameter type), we define a family of well-formedness
judgments. Each context which may require a :math:`\evaltype` uses one
of these well-formedness judgments to ensure that it is of correct
form.

Note that the variable scoping constraints should already be enforced
by earlier elaboration stages, which never generate free type
variables, but they are included here for completeness.

We define a formal syntax of the position parameters which may be used:

.. math::
  \begin{array}{llcl}
  \production{(evaltypepos)} & \evaltypepos &::=&
    \EVTPGENERAL\\&&|&
    \EVTPPARAM\\
  \end{array}

:math:`\EVTBOOL`
................

* In any context and any position, :math:`\EVTBOOL` is well-formed.

.. math::
  \frac{
  }{
    \tyctx \vdashh!EVT_\evaltypepos \EVTBOOL
  }

:math:`\EVTS8`
..............

* In any context and any position, :math:`\EVTS8` is well-formed.

.. math::
  \frac{
  }{
    \tyctx \vdashh!EVT_\evaltypepos \EVTS8
  }

:math:`\EVTU8`
..............

* In any context and any position, :math:`\EVTU8` is well-formed.

.. math::
  \frac{
  }{
    \tyctx \vdashh!EVT_\evaltypepos \EVTU8
  }

:math:`\EVTS16`
...............

* In any context and any position, :math:`\EVTS16` is well-formed.

.. math::
  \frac{
  }{
    \tyctx \vdashh!EVT_\evaltypepos \EVTS16
  }

:math:`\EVTU16`
...............

* In any context and any position, :math:`\EVTU16` is well-formed.

.. math::
  \frac{
  }{
    \tyctx \vdashh!EVT_\evaltypepos \EVTU16
  }

:math:`\EVTS32`
...............

* In any context and any position, :math:`\EVTS32` is well-formed.

.. math::
  \frac{
  }{
    \tyctx \vdashh!EVT_\evaltypepos \EVTS32
  }

:math:`\EVTU32`
...............

* In any context and any position, :math:`\EVTU32` is well-formed.

.. math::
  \frac{
  }{
    \tyctx \vdashh!EVT_\evaltypepos \EVTU32
  }

:math:`\EVTS64`
...............

* In any context and any position, :math:`\EVTS64` is well-formed.

.. math::
  \frac{
  }{
    \tyctx \vdashh!EVT_\evaltypepos \EVTS64
  }

:math:`\EVTU64`
...............

* In any context and any position, :math:`\EVTU64` is well-formed.

.. math::
  \frac{
  }{
    \tyctx \vdashh!EVT_\evaltypepos \EVTU64
  }

:math:`\EVTFLOAT32`
...................

* In any context and any position, :math:`\EVTFLOAT32` is well-formed.

.. math::
  \frac{
  }{
    \tyctx \vdashh!EVT_\evaltypepos \EVTFLOAT32
  }

:math:`\EVTFLOAT64`
...................

* In any context and any position, :math:`\EVTFLOAT64` is well-formed.

.. math::
  \frac{
  }{
    \tyctx \vdashh!EVT_\evaltypepos \EVTFLOAT64
  }

:math:`\EVTCHAR`
................

* In any context and any position, :math:`\EVTCHAR` is well-formed.

.. math::
  \frac{
  }{
    \tyctx \vdashh!EVT_\evaltypepos \EVTCHAR
  }

:math:`\EVTLIST~\evaltype`
..........................

* In any context and any position, if :math:`\evaltype` is
  well-formed, then :math:`\EVTLIST~\evaltype` is well-formed.

.. math::
  \frac{
    \tyctx \vdashh!EVT_\evaltypepos \evaltype
  }{
    \tyctx \vdashh!EVT_\evaltypepos \EVTLIST~\evaltype
  }

:math:`\EVTRECORD~\erecordfield^{\ast}`
.......................................

* In any context and any position, if each :math:`\name_i` is
  distinct, and each :math:`{\evaltype}_i` is well-formed, then
  :math:`\EVTRECORD~\overline{\ERFNAME~\name_i,
  \ERFTYPE~{\evaltype}_i}` is well-formed.

.. math::
  \frac{
    \begin{array}{@{}c@{}}
    \forall i j, i \neq j \Rightarrow \name_i \neq name_j\\
    \forall i, \tyctx \vdashh!EVT_\evaltypepos {\evaltype}_i\\
    \end{array}
  }{
    \tyctx \vdashh!EVT_\evaltypepos
    \EVTRECORD~\overline{\ERFNAME~\name_i, \ERFTYPE~{\evaltype}_i}
  }

:math:`\EVTVARIANT~\evariantcase^{+}`
.....................................

* In any context and any position, if each :math:`\name_i` is
  distinct, and each :math:`{\evaltype}_i` is well-formed, and each
  :math:`\u32^?_i` does not refer to a non-existent or
  self-referential case, then
  :math:`\EVTVARIANT~\overline{\EVCNAME~\name_i,
  \EVCTYPE~{\evaltype^?}_i, \EVCREFINES}` is well-formed.

.. math::
  \frac{
    \begin{array}{@{}c@{}}
    \forall i j, i \neq j \Rightarrow \name_i \neq \name_j\\
    \forall i, \forall \evaltype, {\evaltype^?}_i = \evaltype \Rightarrow \tyctx \vdashh!EVT_\evaltypepos \evaltype\\
    \end{array}
  }{
    \tyctx \vdashh!EVT_\evaltypepos
    \EVTVARIANT~\overline{\EVCNAME~\name_i, \EVCTYPE~{\evaltype^?}_i, \EVCREFINES~\u32^?_i}^n
  }

:math:`\EVTOWN~\EDTRESOURCE~\rtidx`
...................................

* The resource type :math:`\tyctx.\TCRTYPES[\rtidx]` must be defined
  in the context.

* Then in any position, :math:`\EVTOWN~\EDTRESOURCE~\rtidx` is
  well-formed.

.. math::
  \frac{
    \exists \eresourcetype, \tyctx.\TCRTYPES[\rtidx] = \eresourcetype
  }{
    \tyctx \vdashh!EVT_\evaltypepos \EVTOWN~\EDTRESOURCE~\rtidx
  }

:math:`\EVTOWN~\tyvar`
......................

* The type variable :math:`\tyvar` must be defined in the context with
  a bound of :math:`\ETBSUBR`.

* Then in any position, :math:`\EVTOWN~\tyvar` is well-formed.

.. math::
  \frac{
    (\tyvar : \ETBSUBR) \in \tyctx.\TCUVARS \lor \exists \eresourcetype, (\tyvar : \ETBSUBR, \eresourcetype) \in \tyctx.\TCEVARS
  }{
    \tyctx \vdashh!EVT_\evaltypepos \EVTOWN~\tyvar
  }

:math:`\EVTREF~\edeftype`
.........................

* The value type :math:`\EVTOWN~\edeftype` must be well-formed in the
  context in parameter position.

* Then :math:`\EVTREF~\RSCALL~\edeftype` is well-formed in parameter
  position.

.. math::
  \frac{
    \tyctx \vdashh!EVT_\EVTPPARAM \EVTOWN~\edeftype
  }{
    \tyctx \vdashh!EVT_\EVTPPARAM \EVTREF~\RSCALL~\edeftype
  }

.. _syntax-eresulttype:
.. _elaborate-RTtoERT:

Result types
~~~~~~~~~~~~

Because a :math:`\resulttype` may appear in a parameter position or in
a return position, its elaboration is parametrized by which position
it appears in.

Any :math:`\resulttype` elaborates to a :math:`\eresulttype` with the
following abstract syntax:

.. math::
  \begin{array}{llcl}
  \production{(eresulttype)} & \eresulttype &::=&
    \evaltype\\&&|&
    \{ \ERTNAME~\name, \ERTTYPE~\evaltype \}^\ast
  \end{array}

:math:`\valtype`
................

* :math:`\valtype` must elaborate to some :math:`\evaltype`

* :math:`\evaltype` must be valid in the appropriate position.

* Then the result type :math:`\valtype` elaborates to :math:`\evaltype`.

.. math::
  \frac{
    \begin{array}{@{}c@{}}
    \tyctx \vdashh!VTtoEVT \valtype \leadstoh!VTtoEVT \evaltype\\
    \tyctx \vdashh!EVT_\evaltypepos \evaltype\\
    \end{array}
  }{
    \tyctx \vdashh!RTtoERT_\evaltypepos \valtype \leadstoh!RTtoERT \evaltype
  }

:math:`\overline{\{\RTNAME~\name_i, \RTTYPE~\valtype_i\}}`
..........................................................

* Each :math:`\valtype_i` must elaborate to some :math:`{\evaltype}_i`.

* Then the result type :math:`\overline{\{\RTNAME~\name_i,
  \RTTYPE~\valtype_i\}}` elaborates to
  :math:`\overline{\{\ERTNAME~\name_i, \ERTTYPE~{\evaltype}_i\}}`.

.. math::
  \frac{
    \begin{array}{@{}c@{}}
    \forall i, \tyctx \vdashh!VTtoEVT \valtype_i \leadstoh!VTtoEVT {\evaltype}_i\\
    \forall i, \tyctx \vdashh!EVT_\evaltypepos {\evaltype}_i\\
    \end{array}
  }{
    \tyctx \vdashh!RTtoERT_\evaltypepos \overline{\{\RTNAME~\name_i,
    \RTTYPE~\valtype_i\}} \leadstoh!RTtoERT \overline{\{\ERTNAME~\name_i,
    \ERTTYPE~{\evaltype}_i\}}
  }

.. _syntax-efunctype:
.. _elaborate-FTtoEFT:

Function types
~~~~~~~~~~~~~~

Any :math:`\functype` elaborates to a :math:`\efunctype` with the
following abstract syntax:

.. math::
  \begin{array}{llcl}
  \production{(efunctype)} & \efunctype &::=&
    \eresulttype\to\eresulttype
  \end{array}

:math:`\resulttype_1 \to \resulttype_2`
.......................................

* :math:`\resulttype_1` must elaborate in parameter position to some
  :math:`{\eresulttype}_1`.

* :math:`\resulttype_2` must elaborate to some :math:`{\eresulttype}_2`.

* Then the function type :math:`\resulttype_1\to\resulttype_2`
  elaborates to :math:`{\eresulttype}_1\to{\eresulttype}_2`.

.. math::
  \frac{
    \begin{array}{@{}c@{}}
      \tyctx \vdashh!RTtoERT_\EVTPPARAM \resulttype_1 \leadstoh!RTtoERT {\eresulttype}_1\\
      \tyctx \vdashh!RTtoERT \resulttype_2 \leadstoh!RTtoERT {\eresulttype}_2\\
    \end{array}
  }{
    \tyctx \vdashh!FTtoEFT \resulttype_1\to\resulttype_2
    \leadstoh!FTtoEFT {\eresulttype}_1\to{\eresulttype}_2
  }

.. _syntax-etypebound:
.. _elaborate-TBtoETB:

Type bound
~~~~~~~~~~

A type bound elaborates to a :math:`\etypebound` with the following
abstract syntax:

.. math::
  \begin{array}{llcl}
  \production{(etypebound)} & \etypebound &::=& \ETBEQ~\edeftype\\&&|&
  \ETBSUBR\\
  \end{array}

:math:`\TBEQ~\typeidx`
......................

* The type :math:`\tyctx.\TCTYPES[\typeidx]` must be defined in the context.

* Then the type bound :math:`\TBEQ~\typeidx` elaborates to
  :math:`\ETBEQ~\tyctx.\TCTYPES[\typeidx]`.

.. math::
  \frac{
  }{
    \tyctx \vdashh!TBtoETB \TBEQ~\typeidx \leadstoh!TBtoETB \ETBEQ~\tyctx.\TCTYPES[\typeidx]
  }

:math:`\TBSUBR`
...............

* The type bound :math:`\TBSUBR` elaborates to :math:`\ETBSUBR`.

.. math::
  \frac{
  }{
    \tyctx \vdashh!TBtoETB \TBSUBR \leadstoh!TBtoETB \ETBSUBR
  }

.. _syntax-einstancetype:
.. _syntax-einstancetypead:
.. _syntax-eexterndecl:
.. _syntax-eexterndeclad:
.. _syntax-eexterndesc:
.. _syntax-boundedtyvar:

Instance types
~~~~~~~~~~~~~~

An elaborated instance type is nothing more than a list of its exports
behind existential quantifiers for exported types:

.. math::
  \begin{array}{llcl}
  \production{(einstancetype)} & \einstancetype &::=& \exists \boundedtyvar^\ast. \eexterndecl^{*}\\
  \production{(boundedtyvar)} & \boundedtyvar &::=& (\tyvar : \etypebound)\\
  \production{(eexterndecl)} & \eexterndecl &::=& \{ \EEDNAME~\name, \EEDDESC~\eexterndesc \}\\
  \production{(eexterndesc)} & \eexterndesc &::=&
    \EEMDCOREMODULE~\ecoremoduletype\\&&|&
    \EEMDFUNC~\efunctype\\&&|&
    \EEMDVALUE~\evaltype\\&&|&
    \EEMDTYPE~\edeftype\\&&|&
    \EEMDINSTANCE~\einstancetype\\&&|&
    \EEMDCOMPONENT~\ecomponenttype\\
  \end{array}

Because instance value exports must be used linearly in the context,
instances in the contexts are, by analogy with :math:`\evaltypead`,
assigned types from :math:`\einstancetypead`.

.. math::
  \begin{array}{llcl}
  \production{(einstancetypead)} & \einstancetypead &::=&
    \exists\boundedtyvar^\ast. \eexterndeclad^{*}\\
  \production{(eexterndeclad)} & \eexterndeclad &::=&
    \eexterndecl\\&&|&
    \eexterndecl^\dagger\\
  \end{array}

Notational conventions
......................

* We write :math:`\einstancetype \oplus \einstancetype'` to mean the
  instance type formed by the concationation of the export
  declarations of :math:`\einstancetype` and :math:`\einstancetype'`.

* We write :math:`\bigoplus_i {\einstancetype}_i` to mean the instance
  type formed by :math:`{\einstancetype}_1 \oplus \dots \oplus
  {\einstancetype}_n`.

.. _auxiliary-ifinalize:

Finalize: :math:`\lifinalize \einstancetype \rifinalize`
........................................................

Finalizing an instance type eliminates unnecessary type variables with
equality constraints, ensures that all type variables are well-scoped,
and that all quantified types are exported.

* Each type variable existentially quantified in
  :math:`\einstancetype` must either be exported or have an equality
  type bound.

* Then the finalized version of :math:`\einstancetype` is that type,
  with each type variable which is not exported replaced by the type
  that it is equality-bounded to.

.. math::
  \frac{
  \begin{array}{@{}c@{}}
  \F{defined}(\tyvar) =
  \begin{cases}
    \edeftype & \text{if } \exists i, \tyvar_i = \tyvar \land {\etypebound}_i = \ETBEQ~\edeftype\\
    \bot & \text{otherwise}\\
  \end{cases}\\
  \F{externed}(\tyvar) =
  \begin{cases}
    \top & \text{if } \exists i, \tyvar_i = \tyvar \land \exists\name, \{ \EEDNAME~\name, \EEDDESC~\EEMDTYPE~\tyvar \} \in \overline{{\eexterndecl}_j}\\
    \bot & \text{otherwise}\\
  \end{cases}\\
  \forall i, \F{defined}(\tyvar_i) \lor \F{externed}(\tyvar_i)\\
  \delta(\tyvar) = \begin{cases}
    \F{defined}(\tyvar) & \text{if }\neg\F{externed}(\tyvar)\\
    \bot & \text{otherwise}\\
  \end{cases}\\
  \overline{i} = \{ i \mid \F{externed}(\tyvar_i) \}\\
  \end{array}
  }{
   \begin{aligned}
   &\lifinalize \exists \overline{(\tyvar_i : {\etypebound}_i)}. \overline{{\eexterndecl}'_j} \rifinalize\\
   ={}&\delta(\exists \overline{(\tyvar_i : {\etypebound}_i)}^{i \in \overline{i}}. \overline{{\eexterndecl}'_j})\\
   \end{aligned}
  }

.. _elaborate-ITtoEIT:

:math:`\overline{\instancedecl_i}`
..................................

* :math:`\instancedecl_1` must elaborate to some
  :math:`{\einstancetype}_1` in the context
  :math:`\{\TCPARENT~\tyctx\}`.

* For each :math:`i > 1`, the instance declarator
  :math:`\instancedecl_i` must elaborate in the context produced by
  the elaboration of :math:`\instancedecl_{i-1}` to some
  :math:`{\einstancetype}_i`.

* Then the instance type :math:`\overline{\instancedecl_i}` elaborates
  to :math:`\bigoplus_i {\einstancetype}_i`.

.. math::
  \frac{
    \begin{array}{@{}c@{}}
      \tyctx_0 = \{ \TCPARENT~\tyctx \}\\
      \forall i, \tyctx_{i-1} \vdashh!IDtoEIT \instancedecl_i
      \leadstoh!IDtoEIT {\einstancetype}_i \dashv \tyctx_i
    \end{array}
  }{
    \tyctx \vdashh!ITtoEIT \overline{\instancedecl_i}
    \leadstoh!ITtoEIT \lifinalize \bigoplus_i {\einstancetype}_i \rifinalize
  }

.. _elaborate-IDtoEIT:

Instance declarators
~~~~~~~~~~~~~~~~~~~~

Each instance declarator elaborates to a (partial)
:math:`\einstancetype`.

:math:`\IDALIAS~\alias`
.......................

* The :math:`\alias.\ASORT` must be :math:`\STYPE`.

* The :math:`\alias.\ATARGET` must be of the form
  :math:`\ATOUTER~\u32_o~\u32_i`.

* The type :math:`\tyctx.\TCPARENT[\u32_o].\TCTYPES[\u32_i]` must be
  defined in the context.

* The type :math:`\tyctx.\TCPARENT[\u32_o].\TCTYPES[\u32_i]` must not
  be of the form :math:`\EDTRESOURCE~i` for any `i`.

* Then the instance declarator :math:`\IDALIAS~\alias` elaborates to the empty
  list of exports, and sets :math:`\TCTYPES` in the context to the
  original :math:`\tyctx.\TCTYPES` followed by
  :math:`\tyctx.\TCPARENT[\u32_o].\TCTYPES[\u32_i]`.

.. math::
  \frac{
    \begin{array}{@{}c@{}}
    \alias.\ASORT = \STYPE\\
    \alias.\ATARGET = \ATOUTER~\u32_o~\u32_i\\
    \forall i, \tyctx.\TCPARENT[\u32_o].\TCTYPES[\u32_i] \neq \EDTRESOURCE~i\\
    \end{array}
  }{
    \tyctx \vdashh!IDtoEIT \IDALIAS~\alias \leadstoh!IDtoEIT
    \exists\varnothing. \varnothing \dashvh!IDtoEIT \tyctx \oplus \{ \TCTYPES~\tyctx.\TCPARENT[\u32_o].\TCTYPES[\u32_i] \}
  }


:math:`\IDCORETYPE~\core:type`
..............................

* The core type definition :math:`\core:type` must elaborate to some
  elaborated core type :math:`\ecoredeftype`.

* Then the instance declarator :math:`\IDCORETYPE~\core:type`
  elaborates to the empty list of exports, and sets
  :math:`\TCCORE.\CTCTYPES` in the context to the original
  :math:`\tyctx.\TCCORE.\CTCTYPES` followed by the
  :math:`\ecoredeftype`.

.. math::
  \frac{
    \tyctx \vdash \core:type \leadsto \ecoredeftype
  }{
    \tyctx \vdashh!IDtoEIT \IDCORETYPE~\core:type \leadstoh!IDtoEIT
    \exists\varnothing. \varnothing \dashvh!IDtoEIT \tyctx \oplus \{ \TCCORE~\CTCTYPES~\ecoredeftype \}
  }

:math:`\IDTYPE~\deftype`
..........................

* The definition type :math:`\deftype` must elaborate to some
  elaborated definition type :math:`\edeftype`.

* Let :math:`\tyvar` be a fresh type variable.

* Then the instance declarator :math:`\IDTYPE~\deftype` elaborates to
  the empty list of exports behind an existential quantifier
  associating :math:`\tyvar` with :math:`\edeftype`, and sets
  :math:`\TCTYPES` in the context to the original
  :math:`\tyctx.\TCTYPES` followed by the :math:`\tyvar`.

.. math::
  \frac{
    \tyctx \vdashh!DTtoEDT \deftype \leadstoh!DTtoEDT \edeftype
  }{
    \tyctx \vdashh!IDtoEIT \IDTYPE~\deftype \leadstoh!IDtoEIT
    \exists(\tyvar : \ETBEQ~\edeftype). \varnothing
    \dashvh!IDtoEIT \tyctx \oplus \{ \TCEVARS~(\tyvar : \ETBEQ~\edeftype, \edeftype), \TCTYPES~\tyvar \}
  }

* Notice that because this type variable is equality-bounded and not
  exported, it will always be inlined by :math:`\lifinalize
  \einstancetype \rifinalize`.

:math:`\IDEXPORT~\exportdecl`
.............................

* The extern descriptor :math:`\exportdecl.\EDDESC` must elaborate to
  some :math:`\forall\boundedtyvar^\ast.\eexterndesc`.

* Then the instance declarator :math:`\IDEXPORT~\exportdecl`
  elaborates to the singleton list of exports containing
  :math:`\{\EEDNAME~\exportdecl.\EDNAME, \EEDDESC~\eexterndesc \}` and
  quantified by :math:`\boundedtyvar`, and adds an appropriately typed
  entry to the context.

.. math::
  \frac{
    \tyctx \vdashh!EDtoEED \exportdecl.\EDDESC \leadstoh!EDtoEED \forall\boundedtyvar^\ast.\eexterndesc
  }{
    \begin{aligned}
    \tyctx \vdashh!IDtoEIT{}& \exportdecl\\
    \leadstoh!IDtoEIT{}&\exists\boundedtyvar^\ast. \{ \EEDNAME~\exportdecl.\EDNAME, \EEDDESC~\eexterndesc \}\\
    \dashvh!IDtoEIT{}&\tyctx \oplus \{ \TCUVARS~\boundedtyvar^\ast, \eexterndesc \}
    \end{aligned}
  }

.. _elaborate-EDtoEED:

Extern descriptors
~~~~~~~~~~~~~~~~~~

An extern descriptor elaborates to a quantified :math:`\eexterndesc`
with the following abstract syntax:

:math:`\EDTYPE~\typebound`
..........................

* The :math:`\typebound` must elaborate to some :math:`\etypebound`.

* Let :math:`\tyvar` be a fresh type variable.

* Then the import descriptor :math:`\EDTYPE~\typebound` elaborates to
  :math:`\forall(\tyvar : \etypebound).\EEMDTYPE~\tyvar`.

.. math::
  \frac{
    \tyctx \vdashh!TBtoETB \typebound \leadstoh!TBtoETB \etypebound
  }{
    \tyctx \vdashh!EDtoEED \EDTYPE~\typebound \leadstoh!EDtoEED \forall(\tyvar : \etypebound).\EEMDTYPE~\tyvar
  }

:math:`\EDCOREMODULE~\core:typeidx`
...................................

* The type :math:`\tyctx.\TCCORE.\CTCTYPES[\core:typeidx]` must be
  defined in the context, and must be of the form
  :math:`\ecoremoduletype`.

* Then the import descriptor :math:`\EDCOREMODULE~\core:typeidx`
  elaborates to :math:`\forall\varnothing.\EEMDCOREMODULE~\ecoremoduletype`.

.. math::
  \frac{
    \tyctx.\TCCORE.\CTCTYPES[\core:typeidx] = \ecoremoduletype
  }{
    \tyctx \vdashh!EDtoEED \forall\varnothing.\EDCOREMODULE~\core:typeidx \leadstoh!EDtoEED \EEMDCOREMODULE~\ecoremoduletype
  }

:math:`\EDFUNC~\typeidx`
........................

* The type :math:`\tyctx.\TCTYPES[\typeidx]` must be defined in the
  context, and must be of the form :math:`\efunctype`.

* Then the import descriptor :math:`\EDFUNC~\typeidx` elaborates to
  :math:`\forall\varnothing.\EEMDFUNC~\efunctype`

.. math::
  \frac{
    \tyctx.\TCTYPES[\typeidx] = \efunctype
  }{
    \tyctx \vdashh!EDtoEED \EDFUNC~\typeidx \leadstoh!EDtoEED \forall\varnothing.\EEMDFUNC~\efunctype
  }

:math:`\EDVALUE~\typeidx`
.........................

* The type :math:`\tyctx.\TCTYPES[\typeidx]` must be defined in the
  context, and must be of the form to some :math:`\evaltype`.

* :math:`\evaltype` must be well-formed.

* Then the import descriptor :math:`\EDVALUE~\typebound` elaborates to
  :math:`\forall\varnothing.\EEMDVALUE~\evaltype`

.. math::
  \frac{
    \begin{array}{@{}c@{}}
    \tyctx.\TCTYPES[\typeidx] = \evaltype\\
    \tyctx \vdashh!EVT \evaltype\\
    \end{array}
  }{
    \tyctx \vdashh!EDtoEED \EDVALUE~\typeidx \leadstoh!EDtoEED \EEMDVALUE~\evaltype
  }

:math:`\EDINSTANCE~\typeidx`
............................

* The type :math:`\tyctx.\TCTYPES[\typeidx]` must be defined in the
  context, and must be of the form :math:`\exists\boundedtyvar^\ast.\eexterndecl^\ast`.

* Then the import descriptor :math:`\EDINSTANCE~\typeidx` elaborates
  to :math:`\forall\boundedtyvar^\ast.\EEMDINSTANCE~\exists\varnothing.\eexterndecl^\ast`

.. math::
  \frac{
    \tyctx.\TCTYPES[typeidx] = \exists\boundedtyvar^\ast.\eexterndecl^\ast
  }{
    \tyctx \vdashh!EDtoEED \EDINSTANCE~\typeidx \leadstoh!EDtoEED \forall\boundedtyvar^\ast.\EEMDINSTANCE~\exists\varnothing.\eexterndecl^\ast
  }

:math:`\EDCOMPONENT~\typeidx`
.............................

* The type :math:`\tyctx.\TCTYPES[\typeidx]` must be defined in the
  context, and must be of the form :math:`\ecomponenttype`.

* Then the import descriptor :math:`\EDCOMPONENT~\typeidx` elaborates
  to :math:`\forall\varnothing.\EEMDCOMPONENT~\ecomponenttype`

.. math::
  \frac{
    \tyctx.\TCTYPES[\typeidx] = \ecomponenttype
  }{
    \tyctx \vdashh!EDtoEED \EDCOMPONENT~\typeidx \leadstoh!EDtoEED \forall\varnothing.\EEMDCOMPONENT~\ecomponenttype
  }

.. _syntax-ecomponenttype:

Component types
~~~~~~~~~~~~~~~

In a similar manner to instance types above, component types change
significantly upon elaboration: an elaborated component type is
described as a mapping from a quantified list of imports to the type
of the instance that it will produce upon instantiation:

.. math::
  \begin{array}{llcl}
  \production{(ecomponenttype)} & \ecomponenttype &::=&
    \forall \boundedtyvar^\ast. \eexterndecl^\ast \to \einstancetype\\
  \end{array}

Notational conventions
......................

* Much like with instance types above, we write :math:`\ecomponenttype
  \oplus \ecomponenttype'` to mean the combination of two component
  types; in this case, the component type whose imports are the
  concatenation of the import lists of :math:`\ecomponenttype` and
  :math:`\ecomponenttype'` and whose instantiation result (instance)
  type is the result of applying :math:`\oplus` to the instantiation
  result (instance) types of :math:`\ecomponenttype` and
  :math:`\ecomponenttype'`.

.. _auxiliary-cfinalize:

Finalize: :math:`\lcfinalize \ecomponenttype \rcfinalize`
.........................................................

As with instance types above, finalizing a component type eliminates
unnecessary type variables with equality constraints, ensures that all
type variables are well-scoped, and that all quantified types are
imported or exported.

* Each type variable universally quantified in :math:`\ecomponenttype`
  must either be imported (either directly or as a type export of an
  imported instance) or have an equality type bound.

* Each type variable existentially quantified in
  :math:`\ecomponenttype` must either be exported or have an equality
  type bound.

* Each type variable existentially quantified in
  :math:`\ecomponenttype` that is exported must not be present in the
  type of any import.

* Then the finalized version of :math:`\ecomponenttype` is that type,
  with each type variable which is not imported or exported replaced
  by the type that it is equality-bounded to.

.. math::
  \frac{
  \begin{array}{@{}c@{}}
  \F{defined}(\tyvar) =
  \begin{cases}
    \edeftype & \text{if } \exists i, \tyvar_i = \tyvar \land {\etypebound}^\alpha_i = \ETBEQ~\edeftype\\
    \edeftype & \text{if } \exists k, \tyvarb_k = \tyvar \land {\etypebound}^\beta_k = \ETBEQ~\edeftype\\
    \bot & \text{otherwise}\\
  \end{cases}\\
  \F{externed}(\tyvar) =
  \begin{cases}
    \top & \text{if } \exists i, \tyvar_i = \tyvar \land \exists\name, \{ \EEDNAME~\name, \EEDDESC~\EEMDTYPE~\tyvar \} \in \overline{{\eexterndecl}_j}\\
    \top & \text{if } \exists j, {\eexterndecl}_j = \exists \overline{\tyvar''}. \overline{\eexterndecl''} \land \{ \EEDNAME~\name, \EEDDESC~\EEMDTYPE~\tyvar \} \in \overline{\eexterndecl''}\\
    \top & \text{if } \exists i, \tyvarb_k = \tyvar \land \exists\name, \{ \EEDNAME~\name, \EEDDESC~\EEMDTYPE~\tyvar \} \in \overline{{\eexterndecl'}_k}\\
    \bot & \text{otherwise}\\
  \end{cases}\\
  \forall i, \F{defined}(\tyvar_i) \lor \F{externed}(\tyvar_i)\\
  \forall k, \F{defined}(\tyvarb_k) \lor \F{externed}(\tyvarb_k)\\
  \forall k, \F{externed}(\tyvarb_k) \Rightarrow \tyvarb_k \notin \F{free\_tyvars}(\overline{{\eexterndecl}_j})\\
  \delta(\tyvar) = \begin{cases}
    \F{defined}(\tyvar) & \text{if }\neg\F{externed}(\tyvar)\\
    \bot & \text{otherwise}\\
  \end{cases}\\
  \overline{i} = \{ i \mid \F{externed}(\tyvar_i) \}\\
  \overline{k} = \{ k \mid \F{externed}(\tyvarb_k) \}\\
  \end{array}
  }{
   \begin{aligned}
   &\lcfinalize \forall \overline{(\tyvar_i : {\etypebound}^\alpha_i)}. \overline{{\eexterndecl}_j} \to \exists \overline{(\tyvarb_k : {\etypebound}^\beta_k)}. \overline{{\eexterndecl}'_l} \rcfinalize\\
   ={}&\delta(\forall \overline{(\tyvar_i : {\etypebound}^\alpha_i)}^{i \in \overline{i}}. \overline{{\eexterndecl}_j} \to \exists \overline{(\tyvarb_k : {\etypebound}^\beta_k)}^{k \in \overline{k}}. \overline{{\eexterndecl}'_l})\\
   \end{aligned}
  }

.. _elaborate-CTtoECT:

:math:`\overline{\componentdecl_i}`
...................................

* :math:`\componentdecl_1` must elaborate to some
  :math:`{\ecomponenttype}_1` in the context
  :math:`\{\TCPARENT~\Gamma\}`.

* For each :math:`i > 1`, the component declarator
  :math:`\componentdecl_i` must elaborate in the context produced by
  the elaboration of :math:`\componentdecl_{i-1}` to some
  :math:`{\ecomponenttype}_i`.

* Then the component type :math:`\overline{\componentdecl_i}`
  elaborates to the type produced by finalizing :math:`\bigoplus_i
  {\ecomponenttype}_i`.

.. math::
  \frac{
    \begin{array}{@{}c@{}}
      \tyctx_0 = \{ \TCPARENT~\tyctx \}\\
      \forall i, \tyctx_{i-1} \vdashh!CDtoECT \componentdecl_i
      \leadstoh!CDtoECT {\ecomponenttype}_i \dashvh!CDtoECT \tyctx_i
    \end{array}
  }{
    \tyctx \vdashh!CTtoECT \overline{\componentdecl_i}
    \leadstoh!CTtoECT \lcfinalize \bigoplus_i {\ecomponenttype}_i \rcfinalize
  }

.. _elaborate-CDtoECT:

Component declarators
~~~~~~~~~~~~~~~~~~~~~

Each component declarator elaborates to a (partial)
:math:`\ecomponenttype`.

:math:`\instancedecl`
.....................

* The instance declarator :math:`\instancedecl` must elaborate to some
  instance type :math:`\einstancetype` (and may affect the context).

* Then the component declarator :math:`\instancedecl` elaborates to
  the component type :math:`\forall\varnothing. \varnothing \to \einstancetype` and alters
  the context in the same way.

.. math::
  \frac{
    \tyctx \vdashh!IDtoEIT \instancedecl \leadstoh!IDtoEID \einstancetype \dashvh!IDtoEID \tyctx'
  }{
    \tyctx \vdashh!CDtoECT \instancedecl \leadstoh!CDtoECT \forall\varnothing. \varnothing \to \einstancetype \dashvh!CDtoECT \tyctx'
  }

:math:`\importdecl`
...................

* The extern descriptor :math:`\importdecl.\IDDESC` must elaborate to
  some :math:`\forall\boundedtyvar^\ast.\eexterndesc`.

* Then the component declarator :math:`\importdecl` elaborates to the
  component type with no results, the same quantifiers, and a
  singleton list of imports containing
  :math:`\{\EEDNAME~\importdecl.\IDNAME, \EEDDESC~\eexterndesc\}`, and
  updates the context with :math:`\eexterndesc`.

.. math::
  \frac{
    \tyctx \vdashh!EDtoEED \importdecl.\IDDESC \leadstoh!EDtoEED \forall\boundedtyvar^\ast. \eexterndesc
  }{
    \begin{aligned}
    \tyctx \vdashh!CDtoECT{}&\importdecl\\
    \leadstoh!CDtoECT{}&\forall\boundedtyvar^\ast. \{\EEDNAME~\importdecl.\IDNAME, \EEDDESC~\eexterndesc\} \to \varnothing\\
    \dashvh!CDtoECT{}&\tyctx \oplus \{ \TCUVARS~\boundedtyvar^\ast, \eexterndesc \}
    \end{aligned}
  }

.. _syntax-edeftype:
.. _elaborate-DTtoEDT:

Definition types
~~~~~~~~~~~~~~~~

A :math:`\deftype` elaborates to a :math:`\edeftype` with the
following abstract syntax:

.. math::
  \begin{array}{llcl}
  \production{(edeftype)} & \edeftype &::=&
  \tyvar\\&&|&
  \EDTRESOURCE~\rtidx\\&&|&
  \evaltype\\&&|&
  \efunctype\\&&|&
  \ecomponenttype\\&&|&
  \einstancetype\\
  \end{array}

In general, a :math:`\deftype` of the form :math:`\resourcetype` does
not elaborate to any :math:`\edeftype`; however, the component
:math:`\DTYPE` declarator
:math:`\xref{valid/components}{cdecl-rtype}{\text{generates}}` a new
context entry for the resource in question and produces an appropriate
:math:`\EDTRESOURCE` type.

:math:`\defvaltype`
...................

* The definition value type :math:`\defvaltype` must elaborate to some
  :math:`\evaltype`.

* Then the definition type :math:`\defvaltype` elaborates to
  :math:`\evaltype`.

.. math::
  \frac{
    \tyctx \vdashh!DVTtoEVT \defvaltype \leadstoh!DVTtoEVT \evaltype
  }{
    \tyctx \vdashh!DTtoEVT \defvaltype \leadstoh!DTtoEVT \evaltype
  }

:math:`\functype`
.................

* The function type :math:`\functype` must elaborate to some
  :math:`\efunctype`.

* Then the definition type :math:`\functype` elaborates to
  :math:`\efunctype`.

.. math::
  \frac{
    \tyctx \vdashh!FTtoEFT \functype \leadstoh!FTtoEFT \efunctype
  }{
    \tyctx \vdashh!DTtoEDT \functype \leadstoh!DTtoEDT \efunctype
  }

:math:`\componenttype`
......................

* The component type :math:`\componenttype` must elaborate to some
  :math:`\ecomponenttype`.

* Then the definition type :math:`\componenttype` elaborates to
  :math:`\ecomponenttype`.

.. math::
  \frac{
    \tyctx \vdashh!CTtoECT \componenttype \leadstoh!CTtoECT \ecomponenttype
  }{
    \tyctx \vdashh!DTtoEDT \componenttype \leadstoh!DTtoEDT \ecomponenttype
  }

:math:`\instancetype`
.....................

* The instance type :math:`\instancetype` must elaborate to some
  :math:`\einstancetype`.

* Then the definition type :math:`\instancetype` elaborates to
  :math:`\einstancetype`.

.. math::
  \frac{
    \tyctx \vdashh!ITtoEIT \instancetype \leadstoh!ITtoEIT \einstancetype
  }{
    \tyctx \vdashh!DTtoEDT \instancetype \leadstoh!DTtoEDT \einstancetype
  }

.. _syntax-ecoreinstancetype:

Core instance types
~~~~~~~~~~~~~~~~~~~

Although there are no core instance types present at the surface
level, it is useful to define the abstract syntax of (elaborated) core
instance types, as they will be needed to characterise the results of
instantiationg core modules. As with a component instance type, an
(elaborated) core instance type is nothing more than a list of its
exports:

.. math::
  \begin{array}{llcl}
  \production{(ecoreinstancetype)} & \ecoreinstancetype &::=&
    \coreexportdecl^\ast
  \end{array}

Notational conventions
......................

* We write :math:`\ecoreinstancetype \oplus \ecoreinstancetype'` to
  mean the instance type formed by the concationation of the export
  declarations of :math:`\ecoreinstancetype` and
  :math:`\ecoreinstancetype'`.

.. _syntax-ecoremoduletype:

Core module types
~~~~~~~~~~~~~~~~~

Core module types are defined much like component types above: as a
mapping from import descriptions to the type of the instance that will
be produced upon instantiating the module:

.. math::
  \begin{array}{llcl}
  \production{(ecoremoduletype)} & \ecoremoduletype &::=&
    \coreimportdecl^\ast \to \coreexportdecl^\ast
  \end{array}

Notational conventions
......................

* Much like with core instance types above, we write
  :math:`\ecoremoduletype \oplus \ecoremoduletype'` to mean the
  combination of two module types; in this case, the module type whose
  imports are the concatenation of the import lists of
  :math:`\ecoremoduletype` and :math:`\ecoremoduletype'` and whose
  instantiation result (instance) type is the result of applying
  :math:`\oplus` to the instantiation result (instance) types of
  :math:`\ecoremoduletype` and :math:`\ecoremoduletype'`.

:math:`\overline{\coremoduledecl_i}`
....................................

* :math:`\coremoduledecl_1` must elaborate to some
  :math:`{\ecoremoduletype}_1` in the context
  :math:`\{\TCPARENT~\Gamma\}`.

* For each :math:`i > 1`, the core module declarator
  :math:`\coremoduledecl_i` must elaborate in the context produced by
  the elaboration of :math:`\coremoduledecl_{i-1}` to some
  :math:`{\ecoremoduletype}_i`.

* Then the core module type :math:`\overline{\coremoduledecl_i}` to
  :math:`\bigoplus_i {\ecoremoduletype}_i`.

.. math::
  \frac{
    \begin{array}{@{}c@{}}
      \tyctx_0 = \{ \TCPARENT~\tyctx \}\\
      \forall i, \tyctx_{i-1} \vdash \coremoduledecl_i
      \leadsto {\ecoremoduletype}_i \dashv \tyctx_i
    \end{array}
  }{
    \tyctx \vdash \overline{\coremoduledecl_i}
    \leadsto \bigoplus_i {\ecoremoduletype}_i
  }

Core module declarators
~~~~~~~~~~~~~~~~~~~~~~~

Each core module declarator elaborates to a (partial)
:math:`\ecoremoduletype`.

:math:`\coreimportdecl`
.......................

* The core module declarator :math:`\coreimportdecl` elaborates to the
  core module type with no results and a singleton list of imports
  containing :math:`\coreimportdecl`, and does not modify the context.

.. math::
  \frac{
  }{
    \tyctx \vdash \coreimportdecl \leadsto \coreimportdecl \to \varnothing \dashv \tyctx
  }

:math:`\coredeftype`
....................

* The core definition type :math:`\coredeftype` must elaborate to some
  elaborated core definition type :math:`\ecoredeftype`.

* Then the core module declarator :math:`\coredeftype` elaborates to
  the empty core module type, and sets :math:`\TCCORE.\CTCTYPES` in
  the context to the original :math:`\tyctx.\TCCORE.\CTCTYPES`
  followed by the :math:`\edeftype`.

.. math::
  \frac{
    \tyctx \vdash \coredeftype \leadsto \ecoredeftype
  }{
    \tyctx \vdash \coredeftype \leadsto
    \varnothing \to \varnothing \dashv \tyctx \oplus \{ \TCCORE.\CTCTYPES~\ecoredeftype \}
  }

:math:`\corealias`
..................

* The :math:`\corealias.\CASORT` must be :math:`\CSTYPE`.

* The :math:`\corealias.\ATARGET` must be of the form
  :math:`\CATOUTER~\u32_o~\u32_i`.

* The type :math:`\tyctx.\TCPARENT[\u32_o].\TCCORE.\CTCTYPES[\u32_i]`
  must be defined in the context.

* Then the core module declarator :math:`\corealias` elaborates to the
  empty core module type and sets :math:`\TCCORE.\CTCTYPES` in the
  context to the original :math:`\tyctx.\TCCORE.\CTCTYPES` followed by
  :math:`\tyctx.\TCPARENT[\u32_o].\TCCORE.\CTCTYPES[\u32_i]`.

.. math::
  \frac{
    \begin{array}{@{}c@{}}
    \corealias.\CASORT = \CSTYPE\\
    \corealias.\CATARGET = \CATOUTER~\u32_o~\u32_i\\
    \end{array}
  }{
    \tyctx \vdash \alias \leadsto
    \varnothing \to \varnothing \dashv \tyctx \oplus \{ \TCCORE.\CTCTYPES~\tyctx.\TCPARENT[\u32_o].\TCCORE.\CTCTYPES[\u32_i] \}
  }

:math:`\coreexportdecl`
.......................

* The core module declarator :math:`\coreexportdecl` elaborates to the
  core module type with no imports and a singleton list of exports
  containing :math:`\coreexportdecl`, and does not modify the context.

.. math::
  \frac{
  }{
    \tyctx \vdash \coreexportdecl \leadsto \varnothing \to \coreexportdecl \dashv \tyctx
  }

.. _syntax-ecoredeftype:

Core definition types
~~~~~~~~~~~~~~~~~~~~~

A core definition type elaborates to a :math:`\ecoredeftype` with the
following abstract syntax:

.. math::
  \begin{array}{llcl}
  \production{(ecoredeftype)} & \ecoredeftype &::=&
  \core:functype\\&&|&
  \ecoremoduletype
  \end{array}

:math:`\core:functype`
......................

* The core definition type :math:`\core:functype` elaborates to
  :math:`\core:functype`.

.. math::
  \frac{
  }{
    \tyctx \vdash \core:functype \leadsto \core:functype
  }

:math:`\coremoduletype`
.......................

* The core module type :math:`\coremoduletype` must elaborate to some
  :math:`\ecoremoduletype`.

* Then the core definition type :math:`\coremoduletype` elaborates to
  :math:`\ecoremoduletype`.

.. math::
  \frac{
    \tyctx \vdash \coremoduletype \leadsto \ecoremoduletype
  }{
    \tyctx \vdash \coremoduletype \leadsto \ecoremoduletype
  }
