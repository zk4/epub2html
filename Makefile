
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


coverage:
	pytest --cov=epub2html/ tests/

dev:
	python3 -m epub2html "./SuperMemo.epub"

dd:
	python3 -m epub2html "./dd.epub"

a:
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
	echo "use a fresh env first"
	pip3 freeze > requirements.txt



env-rm:
	rm -rdf env


env:
	python3 -m venv env
	. env/bin/activate

path:
	echo $$PATH

auto_version:
	python3 version.py
