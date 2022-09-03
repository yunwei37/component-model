Components
----------

.. _syntax-coresort:
.. _syntax-sort:

Sorts
~~~~~

A component's definitions define objects, each of which is of one of
the following *sort*\ s:

.. math::
  \begin{array}{llcl}
  \production{(coresort)} & \coresort &::=&
    \CSFUNC | \CSTABLE | \CSMEMORY | \CSGLOBAL | \CSTYPE | \CSMODULE | \CSINSTANCE\\
  \production{(sort)} & \sort &::=&
    \SCORE~\coresort\\&&|&
    \SFUNC | \SVALUE | \STYPE | \SCOMPONENT | \SINSTANCE
  \end{array}

.. _syntax-coremoduleidx:
.. _syntax-componentidx:
.. _syntax-instanceidx:
.. _syntax-funcidx:
.. _syntax-corefuncidx:
.. _syntax-typeidx:
.. _syntax-coretypeidx:
.. _syntax-sortidx:
.. _syntax-coresortidx:
.. _syntax-coreinstanceidx:
.. _syntax-valueidx:

Indices
~~~~~~~

Each object defined by a component exists within an *index space* made
up of all objects of the same sort. Unlike in Core WebAssembly, a
component definition may only refer to objects that were defined prior
to it in the current component. Future definitions refer to past
definitions by means of an *index* into the appropriate index space:

.. math::
  \begin{array}{llll}
  \production{(coremoduleidx)} & \coremoduleidx &::=& \u32\\
  \production{(coreinstanceidx)} & \coreinstanceidx &::=& \u32\\
  \production{(componentidx)} & \componentidx &::=& \u32\\
  \production{(instanceidx)} & \instanceidx &::=& \u32\\
  \production{(funcidx)} & \funcidx &::=& \u32\\
  \production{(corefuncidx)} & \corefuncidx &::=& \u32\\
  \production{(valueidx)} & \valueidx &::=& \u32\\
  \production{(typeidx)} & \typeidx &::=& \u32\\
  \production{(coretypeidx)} & \coretypeidx &::=& \u32
  \end{array}

.. math::
  \begin{array}{llll}
  \production{(coresortidx)} & \coresortidx &::=& \{ \CSISORT~\coresort, \CSIIDX~\u32 \}\\
  \production{(sortidx)} & \sortidx &::=& \{ \SISORT~\sort, \SIIDX~\u32 \}
  \end{array}

.. _syntax-definition:

Definitions
~~~~~~~~~~~

Each object within a component is defined by a *definition*, of which
there are several kinds:

.. math::
  \begin{array}{llcl}
  \production{(definition)} & \definition &::=&
  \DCOREMODULE~\core:module\\&&|&
  \DCOREINSTANCE~\coreinstance\\&&|&
  \DCORETYPE~\coredeftype\\&&|&
  \DCOMPONENT~\component\\&&|&
  \DINSTANCE~\instance\\&&|&
  \DALIAS~\alias\\&&|&
  \DTYPE~\deftype\\&&|&
  \DCANON~\canon\\&&|&
  \DSTART~\start\\&&|&
  \DIMPORT~\import\\&&|&
  \DEXPORT~\export\\
  \end{array}

.. _syntax-coreinstance:
.. _syntax-coreinstantiatearg:
.. _syntax-coreexport:

Core instances
~~~~~~~~~~~~~~

A core instance may be defined either by instantiating a core module
with other core instances taking the place of its first-level imports,
or by creating a core module from whole cloth by combining core
definitions already present in our index space:

.. math::
  \begin{array}{llcl}
  \production{(coreinstance)} & \coreinstance &::=&
  \CIINSTANTIATE~\coremoduleidx~\coreinstantiatearg^{*}\\&&|&
  \CIEXPORTS~\coreexport^{*}\\
  \production{(coreinstantiatearg)} & \coreinstantiatearg &::=&
  \{ \CIANAME~\name, \CIAINSTANCE~\coreinstanceidx \}\\
  \production{(coreexport)} & \coreexport &::=& \{ \CENAME~\name, \CEDEF~\coresortidx \}\\
  \end{array}

.. _syntax-component:

Components
~~~~~~~~~~

A component is merely a sequence of definitions:

.. math::
  \begin{array}{llll}
  \production{(component)} & \component &::=& \definition^{*}
  \end{array}

.. _syntax-instance:
.. _syntax-instantiatearg:

Instances
~~~~~~~~~

Component-level instance declarations are nearly identical to
core-level instance declarations, with the caveat that more sorts of
definitions may be supplied as imports:

.. math::
  \begin{array}{llcl}
  \production{(instance)} & \instance &::=&
  \IINSTANTIATE~\componentidx~\instantiatearg^{*}\\&&|&
  \IEXPORTS~\export^{*}\\
  \production{(instantiatearg)} & \instantiatearg &::=&
  \{ \IANAME~\name, \IAARG~\sortidx \}
  \end{array}

.. _syntax-alias:
.. _syntax-aliastarget:

Aliases
~~~~~~~

An alias definition copies a definition from some other module,
component, or instance into an index space of the current component:

.. math::
  \begin{array}{llcl}
  \production{(alias)} & \alias &::=& \{ \ASORT~\sort, \ATARGET~\aliastarget \}\\
  \production{(aliastarget)} & \aliastarget &::=&
  \ATEXPORT~\instanceidx~\name\\&&|&
  \ATCOREEXPORT~\coreinstanceidx~\name\\&&|&
  \ATOUTER~\u32~\u32\\
  \end{array}

.. _syntax-canon:
.. _syntax-canonopt:

Canonical definitions
~~~~~~~~~~~~~~~~~~~~~

Canonical definitions are the only way to convert between Core
WebAssembly functions and component-level shared-nothing functions
which produce and consume values of type :math:`valtype`. A *canon
lift* definition converts a core WebAssembly function into a
component-level function which may be exported or used to satisfy the
imports of another component; a *canon lower* definition converts an
lifted function (often imported) into a core function.

.. math::
  \begin{array}{llcl}
  \production{(canon)} & \canon &::=&
  \CLIFT~\core:funcidx~\canonopt^{*}~\typeidx\\&&|&
  \CLOWER~\funcidx~\canonopt^{*}\\
  \production{(canonopt)} & \canonopt &::=&
  \COSTRINGENCODINGUTF8\\&&|&
  \COSTRINGENCODINGUTF16\\&&|&
  \COSTRINGENCODINGLATIN1UTF16\\&&|&
  \COMEMORY~\core:memidx\\&&|&
  \COREALLOC~\core:funcidx\\&&|&
  \COPOSTRETURN~\core:funcidx\\
  \end{array}

.. _syntax-start:

Start definitions
~~~~~~~~~~~~~~~~~

A start definition specifies a component function which this component
would like to see called at instantiation type in order to do some
sort of initialization.

.. math::
  \begin{array}{llcl}
  \production{(start)} & \start &::=& \{ \FFUNC~\funcidx, \FARGS~\valueidx^{*} \}
  \end{array}

.. _syntax-import:

Imports
~~~~~~~

Since an imported value is described entirely by its type, an actual
import definition is effectively the same thing as an import
declaration:

.. math::
  \begin{array}{llcl}
  \production{(import)} & \import &::=& \importdecl
  \end{array}

.. _syntax-export:

Exports
~~~~~~~

An export definition is simply a name and a reference to another
definition to export:

.. math::
  \begin{array}{llll}
  \production{(export)} & \export &::=& \{ \ENAME~\name, \EDEF~\sortidx \}
  \end{array}
