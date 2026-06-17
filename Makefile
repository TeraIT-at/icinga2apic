.PHONY: install test lint release

# Install the package together with the test/lint tooling.
install:
	pip install -e . pytest flake8

# Run the test suite.
test:
	pytest -q

# Lint: fail on real errors, report style issues without failing.
lint:
	flake8 icinga2apic tests --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 icinga2apic tests --count --max-line-length=100 --exit-zero --statistics

# Cut a release locally (gates on green CI, then publishes). See RELEASING.md.
release:
	./scripts/release.sh
