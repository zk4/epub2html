
rm:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -type d -iname '*egg-info' -exec rm -rdf {} +
	rm -f .coverage
	rm -rf htmlcov
	rm -rf dist
	rm -rf build
	rm -rf proxy.py.egg-info
	rm -rf .pytest_cache
	rm -rf .hypothesis
	rm -rdf assets


wtest:
	watchexec -rce py "source ~/.bash_profile && make test"


test: rm
	pytest -s -v  tests/

coverage-html:
	# --cov where you want to cover
	#  tests  where your test code is
	pytest --cov=epub2html/ --cov-report=html tests/
	open htmlcov/index.html

coverage:
	pytest --cov=epub2html/ tests/

maina:
	python3 -m epub2html "./a.epub"

mainb:
	python3 -m epub2html "./a.epub"

any:
	python3 -m epub2html "./$(t).epub"

install: uninstall auto_version
	sudo pip3 install .

uninstall: rm
	sudo pip3 uninstall -y epub2html

run:
	python3 -m epub2html "./llvmcookbook.epub" -o "./"

wrun:
	watchexec -rce py "source ~/.bash_profile && make run"
help:
	python3 -m epub2html --help
all: rm uninstall install run


pure-all: env-rm rm env install test run



upload-to-test: rm
	python3 setup.py bdist_wheel --universal
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*


upload-to-prod: rm auto_version
	python3 setup.py bdist_wheel --universal
	twine upload dist/*


freeze:
	# pipreqs will find the module the project really depneds
	pipreqs . --force

freeze-all:
	#  pip3 will find all the module not belong to standard  library
	pip3 freeze > requirements.txt



env-rm:
	rm -rdf env


env:
	python3 -m venv env
	. env/bin/activate

path:
	echo $$PATH

auto_version:
	python version.py
