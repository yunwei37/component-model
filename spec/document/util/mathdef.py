from sphinx.directives.patches import MathDirective
from sphinx.util.texescape import tex_replace_map
from sphinx.writers.html5 import HTML5Translator
from sphinx.writers.latex import LaTeXTranslator
from docutils import nodes
from docutils.nodes import math
from docutils.parsers.rst.directives.misc import Replace
from six import text_type
import re


# Transform \xref in math nodes

xref_re = re.compile('\\\\(core:|)xref\{([^}]*)\}\{([^}]*)\}', re.M)

def munge_file(file):
  if file[0] == "!":
    fileparts = file.split("!")
    if fileparts[1] == "S":
      if fileparts[2] in fileparts[3]:
        return fileparts[4]
      else:
        return fileparts[5]
  return file

def html_hyperlink(is_core, file, id):
  sub = (munge_file(file), id.replace('_', '-').lower())
  if is_core:
    return '\\href{https://webassembly.github.io/spec/core/%s.html#%s}' % sub
  else:
    return '\\href{../%s.html#%s}' % sub

def html_transform_math_xref(node):
  new_text = xref_re.sub(lambda m: html_hyperlink(m.group(1), m.group(2), m.group(3)), node.astext())
  node.children[0] = nodes.Text(new_text)

# Mirrors sphinx/writers/latex
def latex_hyperlink(is_core, file, id):
  if is_core:
    return '\\href{https://webassembly.github.io/spec/core/%s.html\\#%s}' \
      % (munge_file(file), id.replace('_', '-'))
  else:
    id = text_type(id).translate(tex_replace_map).\
      encode('ascii', 'backslashreplace').decode('ascii').\
      replace('_', '-').replace('\\', '_')
    return '\\hyperref[%s:%s]' % (munge_file(file), id)

def latex_transform_math_xref(node):
  new_text = xref_re.sub(lambda m: latex_hyperlink(m.group(1), m.group(2), m.group(3)), node.astext())
  node.children[0] = nodes.Text(new_text)

# Expand mathdef names in math roles and directives

def_re = re.compile('\\\\[A-Za-z][0-9A-Za-z:!]*', re.M)

auxcounter = 0

def corify_xrefs(str):
  corified = xref_re.sub(lambda m: '\\core:xref{%s}{%s}' % (m.group(2), m.group(3)), str)
  return corified

def lookup_mathdef(defs, name, is_core):
  split = name.split('!')
  name = split[0]
  if is_core:
    core_name = "\\core:" + name[1:]
    if core_name in defs:
      return lookup_mathdef(defs, core_name, False)
  if name in defs:
    [arity, s] = defs[name]
    if arity == 1 and name == "X":
      # stupid hack for reasons
      pass
    if arity > 0:
      global auxcounter
      auxcounter = auxcounter + 1
      name = "\\mathdef%d" % auxcounter
      s = "\\def%s#%d{%s}%s" % (name, arity, s, name)
    if arity < 0:
      for i in range(1, -arity+1):
        s = s.replace("#" + str(i), split[i])
    if name.startswith("\\core:"):
      s = corify_xrefs(s)
    return s
  return name

def replace_mathdefs(doc, s, is_core):
  if not hasattr(doc, 'mathdefs'):
    return s
  return def_re.sub(lambda m: lookup_mathdef(doc.mathdefs, m.group(0), is_core), s)

def ext_math_role(role, raw, text, line, inliner, options = {}, content = []):
  text = replace_mathdefs(inliner.document, raw.split('`')[1], False)
  return [math(raw, text)], []

class ExtMathDirective(MathDirective):
  def run(self):
    doc = self.state.document
    for i, s in enumerate(self.content):
      self.content[i] = replace_mathdefs(doc, s, False)
    for i, s in enumerate(self.arguments):
      self.arguments[i] = replace_mathdefs(doc, s, False)
    return super().run()

class MathdefDirective(Replace):
  def run(self):
    name = '\\' + self.state.parent.rawsource.split('|')[1]
    name = name.split('#')
    if len(name) > 1:
      arity = int(name[1])
    else:
      arity = 0
    name = name[0]
    doc = self.state.document
    if not hasattr(doc, 'mathdefs'):
      doc.mathdefs = {}
    # TODO: we don't ever hit the case where len(self.content) > 1
    for i, s in enumerate(self.content):
      self.content[i] = replace_mathdefs(doc, s, False)
    doc.mathdefs[name] = [arity, ''.join(self.content)]
    self.content[0] = ':math:`' + self.content[0]
    self.content[-1] = self.content[-1] + '`'
    return super().run()

class CoreMathdefDirective(Replace):
  def run(self):
    name = self.state.parent.rawsource.split('|')[1]
    name = '\\' + ("" if name.startswith("core:") else "core:") + name
    name = name.split('#')
    if len(name) > 1:
      arity = int(name[1])
    else:
      arity = 0
    name = name[0]
    doc = self.state.document
    if not hasattr(doc, 'mathdefs'):
      doc.mathdefs = {}
    # TODO: we don't ever hit the case where len(self.content) > 1
    for i, s in enumerate(self.content):
      self.content[i] = replace_mathdefs(doc, s, True)
    doc.mathdefs[name] = [arity, ''.join(self.content)]
    self.content[0] = ':math:`' + self.content[0]
    self.content[-1] = self.content[-1] + '`'
    return super().run()

class WebAssemblyHTML5Translator(HTML5Translator):
  """
  Customize HTML5Translator.
  Convert xref in math and math block nodes to hrefs.
  """
  def visit_math(self, node, math_env = ''):
    html_transform_math_xref(node)
    super().visit_math(node, math_env)

  def visit_math_block(self, node, math_env  = ''):
    html_transform_math_xref(node)
    super().visit_math_block(node, math_env)

class WebAssemblyLaTeXTranslator(LaTeXTranslator):
  """
  Customize LaTeXTranslator.
  Convert xref in math and math block nodes to hyperrefs.
  """
  def visit_math(self, node):
    latex_transform_math_xref(node)
    super().visit_math(node)

  def visit_math_block(self, node):
    latex_transform_math_xref(node)
    super().visit_math_block(node)

# Setup

def setup(app):
  app.set_translator('html', WebAssemblyHTML5Translator)
  app.set_translator('singlehtml', WebAssemblyHTML5Translator)
  app.set_translator('latex', WebAssemblyLaTeXTranslator)
  app.add_role('math', ext_math_role)
  app.add_directive('math', ExtMathDirective, override = True)
  app.add_directive('mathdef', MathdefDirective)
  app.add_directive('coremathdef', CoreMathdefDirective)
