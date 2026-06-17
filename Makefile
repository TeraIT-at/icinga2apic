.PHONY: install test lint dist release clean

# Install the package together with the test/lint tooling.
install:
	pip install -e . pytest flake8

# Run the test suite.
test:
	pytest tests/ -q

# Lint: fail on real errors, report style issues without failing.
lint:
	flake8 icinga2apic tests --select=E9,F63,F7,F82 --show-source --statistics
	flake8 icinga2apic tests --exit-zero --max-line-length=127 --statistics

# Build sdist + wheel into dist/.
dist: clean
	python -m build
	ls -l dist

# Releases are cut locally with python-semantic-release. See RELEASING.md.
release:
	@echo "Releases are cut with python-semantic-release. Run ./scripts/release.sh (see RELEASING.md)."

clean:
	rm -fr build/ dist/ *.egg-info
