# <a id="about-icinga2"></a> About icinga2apic

icinga2apic is a [Python](http://www.python.org) module to interact with the [Icinga 2 RESTful API](https://www.icinga.com/docs/icinga2/latest/doc/12-icinga2-api/).

# Features

1. [basic and certificate auth](doc/2-authentication.md)
1. [config file support](doc/2-authentication.md#-config-file)
1. [objects (zone support)](doc/3-objects.md)
1. [actions](doc/4-actions.md)
1. [events](doc/5-events.md)
1. [status](doc/6-status.md)

# Developing

```sh
python -m venv .venv && . .venv/bin/activate
make install   # editable install + pytest/flake8
make test      # run the test suite
make lint      # run flake8
```

Tests run automatically on every push and pull request via GitHub Actions
across Python 3.8–3.12 (`.github/workflows/tests.yml`).

# Releasing

Commits follow [Conventional Commits](https://www.conventionalcommits.org/)
and the version is derived automatically from the commit history. See
[RELEASING.md](RELEASING.md) for the versioning rules and the release process.

# Usage

See the [doc](doc) directory.
