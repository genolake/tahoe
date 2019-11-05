
define help

Supported targets: prepare, develop, clean, test, check_build_reqs.

endef
export help
help:
	@printf "$$help"

# This Makefile uses bash features like printf and <()
SHELL=bash
python=python
jupyter=jupyter
pip=pip
npm=npm
node=node
tahoe_version:=$(shell $(python) genolake/tahoe/pileup/_version.py)
sdist_name:=tahoe.pileup-$(tahoe_version).tar.gz
tests=genolake/tahoe/
extras=
current_commit:=$(shell git log --pretty=oneline -n 1 -- $(pwd) | cut -f1 -d " ")
dirty:=$(shell (git diff --exit-code && git diff --cached --exit-code) > /dev/null || printf -- --DIRTY)

green=\033[0;32m
normal=\033[0m\n
red=\033[0;31m

develop:
	rm -rf genolake/tahoe/pileup/static
	rm -rf genolake/tahoe/js/dist
	rm -rf genolake.tahoe.pileup.egg-info/
	- $(pip) install -v -e .$(extras)
	- $(jupyter) nbextension uninstall pileup
	- $(jupyter) nbextension enable --py widgetsnbextension
	- $(jupyter) nbextension install --py --symlink --user genolake.tahoe.pileup
	- $(jupyter) nbextension enable genolake.tahoe.pileup --py --user


sdist: dist/$(sdist_name)
dist/$(sdist_name):
	@test -f dist/$(sdist_name) && mv dist/$(sdist_name) dist/$(sdist_name).old || true
	$(python) setup.py sdist bdist_egg
	@test -f dist/$(sdist_name).old \
			&& ( cmp -s <(tar -xOzf dist/$(sdist_name)) <(tar -xOzf dist/$(sdist_name).old) \
					 && mv dist/$(sdist_name).old dist/$(sdist_name) \
					 && printf "$(green)No significant changes to sdist, reinstating backup.$(normal)" \
					 || rm dist/$(sdist_name).old ) \
			|| true
clean_sdist:
	- rm -rf dist


test: check_build_reqs
	pushd examples \
		&& jupyter nbconvert --to python pileup-tutorial.ipynb

	mkdir -p target
	$(python) -m pytest -vv --junitxml target/pytest-reports/tests.xml $(tests)
	# run lint and flow for js
	pushd genolake/tahoe/js \
		&& npm run lint


pypi: clean sdist
	set -x \
	&& $(python) setup.py egg_info sdist bdist_egg \
	&& twine check dist/* \
	&& twine upload dist/*
	
# clean
clean:
	rm -rf genolake/tahoe/js/dist
	rm -rf genolake.tahoe.pileup.egg-info/
	rm -rf genolake/tahoe/pileup/static/
	rm -rf dist/
	rm -rf genolake/tahoe/js/node_modules
	$(jupyter) nbextension uninstall pileup


# check for node, jupyter and npm
check_build_reqs:
	@$(python) -c 'import jupyter' \
		|| ( printf "$(red)Build requirements are missing. Run 'make prepare' to install them.$(normal)" ; false )

	@$(npm) --version > /dev/null \
		|| ( printf "$(red)npm is not installed. Please install npm: https://www.npmjs.com/get-npm" ; false)

	@$(node) --version > /dev/null \
		|| ( printf "$(red)node is not installed. Please install node: https://nodejs.org/en/download/package-manager/" ; false)


# installs necessary requirements
prepare:
	$(pip) install -r requirements.txt

	# install node_modules
	cd genolake/tahoe/js; \
		$(npm) install
