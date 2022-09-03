.. _syntax-type:

Types
-----

The component model introduces two new kinds of types: value types,
which are used to classify shared-nothing interface values, and
definition types, which are used to characterize the core and
component modules, instances, and functions which form part of a a
component's interface.

.. _syntax-recordfield:
.. _syntax-variantcase:
.. _syntax-primvaltype:
.. _syntax-defvaltype:
.. _syntax-valtype:

Value types
~~~~~~~~~~~

A *value type* classifies a component-level abstract value. Unlike for
Core WebAssembly values, no specified abstract syntax of component
values exist; they serve simply to define the interface of lifted
component functions (which currently may be produced only via
canonical definitions).

Value types are further divided into primitive value types, which have
a compact representation and can be found in most places where types
are allowed, and defined value types, which must appear in a type
definition before they can be used (via a :math:`\typeidx` into the
type index space):

.. math::
   \begin{array}{llcl}
   \production{(primvaltype)} & \primvaltype &::=&
     \VTBOOL\\&&|&
     \VTS8 ~|~ \VTU8 ~|~ \VTS16 ~|~ \VTU16 ~|~ \VTS32 ~|~ \VTU32 ~|~ \VTS64 ~|~ \VTU64\\&&|&
     \VTFLOAT32 ~|~ \VTFLOAT64\\&&|&
     \VTCHAR ~|~ \VTSTRING\\&&|&\\
   \production{(defvaltype)} & \defvaltype &::=&
     \VTPRIM~\primvaltype\\&&|&
     \VTRECORD~\recordfield^{+}\\&&|&
     \VTVARIANT~\variantcase^{+}\\&&|&
     \VTLIST~\valtype\\&&|&
     \VTTUPLE~\valtype^{*}\\&&|&
     \VTFLAGS~\name^{*}\\&&|&
     \VTENUM~\name^{+}\\&&|&
     \VTUNION~\valtype^{+}\\&&|&
     \VTOPTION~\valtype\\&&|&
     \VTRESULT~\valtype^{?}~\valtype^{?}\\&&|&
     \VTOWN~\typeidx\\&&|&
     \VTBORROW~\typeidx\\
   \production{(valtype)} &\valtype &::=&
     \primvaltype ~|~ \typeidx
   \end{array}

.. math::
   \begin{array}{llll}
   \production{(recordfield)} & \recordfield &::=&
     \{ \RFNAME~\name, \RFTYPE~\valtype \}\\
   \production{(variantcase)} & \variantcase &::=&
     \{ \VCNAME~\name, \VCTYPE~\valtype, \VCREFINES~\u32^? \}
   \end{array}

.. _syntax-resourcetype:

Resource types
~~~~~~~~~~~~~~

.. math::
  \begin{array}{llll}
  \production{(resourcetype)} & \resourcetype &::= &
    \{ \RTREP~\mathtt{i32}, \RTDTOR~\funcidx \}
  \end{array}

.. _syntax-functype:
.. _syntax-funclist:

Function types
~~~~~~~~~~~~~~

A component-level shared-nothing function is classified by the types
of its parameters and return values. Such a function may take as
parameters zero or more named values, and will return as results zero
or more namde values. If a function takes a single parameter, or
returns a single result, said parameter or result may be unnamed:

.. math::
   \begin{array}{llll}
   \production{(functype)} & \functype &::=&
     \resulttype \to \resulttype
   \end{array}

The input or output of a function is classified by a result type:

.. math::
   \begin{array}{llcl}
   \production{(resulttype)} & \resulttype &::=&
     \valtype\\&&|&
     \{ \RTNAME~\name, \RTTYPE~\valtype \}^{*}
   \end{array}

.. _syntax-instancetype:
.. _syntax-instancedecl:
.. _syntax-exportdecl:
.. _syntax-typebound:

Instance types
~~~~~~~~~~~~~~

A component instance is conceptually classified by the types of its
exports. However, an instance's type is concretely represented as a
series of *declarations* manipulating index spaces (particular to the
instance type; these index spaces are entirely unrelated to both the
index spaces of any instance which has this type and those of any
instance importing or exporting something of this type). This allows
for better type sharing and, in the future, uses of private types from
parent components.

.. math::
   \begin{array}{llcl}
   \production{(instancetype)} & \instancetype &::=& \instancedecl^{*}\\
   \production{(instancedecl)} & \instancedecl &::=&
   \IDALIAS~\alias\\&&|&
   \IDCORETYPE~\core:type\\&&|&
   \IDTYPE~\deftype\\&&|&
   \IDEXPORT~\exportdecl\\
   \production{(externdesc)} & \externdesc &::=&
     \EDTYPE~\typebound\\&&|&
     \EDCOREMODULE~\core:typeidx\\&&|&
     \EDFUNC~\typeidx\\&&|&
     \EDVALUE~\valtype\\&&|&
     \EDINSTANCE~\typeidx\\&&|&
     \EDCOMPONENT~\typeidx\\
   \production{(typebound)} & \typebound &::=&
   \TBEQ~\typeidx\\&&|&
   \TBSUBR\\&&|&
   \dots\\
   \production{(exportdecl)} & \exportdecl &::=& \{ \EDNAME~\name, \EDDESC~\externdesc \}
   \end{array}

.. _syntax-componenttype:
.. _syntax-componentdecl:
.. _syntax-importdecl:
.. _syntax-externdesc:

Component types
~~~~~~~~~~~~~~~

A component is conceptually classified by the types of its imports and
exports. However, like instances, this is concretely represented as a
series of declarations; in particular, a similar set of declarations
allowing also for imports.

.. math::
   \begin{array}{llcl}
   \production{(componenttype)} & \componenttype &::=& \componentdecl^{*}\\
   \production{(componentdecl)} & \componentdecl &::=&
   \instancedecl\\&&|&
   \CDIMPORT~\importdecl\\
   \production{(importdecl)} & \importdecl &::=& \{ \IDNAME~\name, \IDDESC~\externdesc \}\\
   \end{array}

.. _syntax-deftype:

Definition types
~~~~~~~~~~~~~~~~

A type definition may name a value, resource, function, component, or instance type:

.. math::
   \begin{array}{llcl}
   \production{(deftype)} & \deftype &::=&
   \defvaltype\\&&|&
   \resourcetype\\&&|&
   \functype\\&&|&
   \componenttype\\&&|&
   \instancetype\\
   \end{array}
.. _syntax-coredeftype:
.. _syntax-coremoduletype:
.. _syntax-coreimportdecl:
.. _syntax-coreexportdecl:
.. _syntax-corealias:
.. _syntax-corealiastarget:
.. _syntax-coremoduledecl:

Core definition types
~~~~~~~~~~~~~~~~~~~~~

The component module specification also defines an expanded notion of
what a core type is, which may eventually be subsumed by a core module
linking extension.

.. math::
  \begin{array}{llcl}
  \production{(coredeftype)} & \coredeftype &::=&
  \core:functype\\&&|&
  \coremoduletype\\
  \production{(coremoduletype)} & \coremoduletype &::=& \coremoduledecl^{*}\\
  \production{(coremoduledecl)} & \coremoduledecl &::=&
  \coreimportdecl\\&&|&
  \coredeftype\\&&|&
  \corealias\\&&|&
  \coreexportdecl\\
  \production{(corealias)} & \corealias &::=& \{ \CASORT~\coresort, \CATARGET~\corealiastarget \}\\
  \production{(corealiastarget)} & \corealiastarget &::=& \CATOUTER~\u32~\u32\\
  \production{(coreimportdecl)} & \coreimportdecl &::=& \core:import\\
  \production{(coreexportdecl)} & \coreexportdecl &::=& \{ \CEDNAME~\name, \CEDDESC~\core:importdesc \}
  \end{array}
