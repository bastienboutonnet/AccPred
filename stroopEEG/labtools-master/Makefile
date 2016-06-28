.PHONY: tests* demos* docs*

tests: 
	python -m labtools.tests.generator_functions_tests
	python -m labtools.tests.trials_functions_tests

demos-run:
	runipy -o demos/simple-trial-generation.ipynb
	runipy -o demos/using-generators.ipynb

demos-convert:
	ipython nbconvert --to rst demos/simple-trial-generation.ipynb
	ipython nbconvert --to rst demos/using-generators.ipynb

demos-add:
	cp demos/simple-trial-generation.rst ../docs/demos/generating-trial-lists/simple-trial-generation.rst
	cp demos/using-generators.rst ../docs/demos/generating-trial-lists/using-generators.rst

demos: demos-run demos-convert demos-add

docs-build:
	cd docs && $(MAKE) html

docs-push:
	cd ../labtools-docs/html && \
	git add --all && \
	git commit -m "Updates to docs" && \
	git push origin gh-pages

docs: docs-build docs-push
