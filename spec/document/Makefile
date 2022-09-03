# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?= -d _build/.doctrees
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

SOURCE_DATE_EPOCH = $(shell date +"%s")

ALLSPHINXOPTS = -d $(BUILDDIR)/doctrees $(SPHINXOPTS) .

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: html
html:
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html
	for file in `ls $(BUILDDIR)/html/*.html`; \
	do \
	  sed s:BASEDIR:.:g <$$file >$$file.out; \
	  mv -f $$file.out $$file; \
	done
	for file in `ls $(BUILDDIR)/html/*/*.html`; \
	do \
	  sed s:BASEDIR:..:g <$$file >$$file.out; \
	  mv -f $$file.out $$file; \
	done
	@echo
	@echo "Build finished. The HTML pages are in `pwd`/$(BUILDDIR)/html/."

NAME=webassemblycomponentmodel

.PHONY: docs
docs: html latexpdf
	mkdir -p ../../docs/multihtml/
	cp -r $(BUILDDIR)/html/* ../../docs/multihtml/
	rm ../../docs/multihtml/objects.inv
	mkdir -p ../../docs/_download/
	cp $(BUILDDIR)/latex/$(NAME).pdf ../../docs/_download/
