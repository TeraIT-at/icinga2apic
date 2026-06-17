# Releasing

Releases are cut locally with [python-semantic-release]; the version bump,
commit, tag, build and PyPI upload all run locally, so no token is stored in CI.
GitHub Actions (`.github/workflows/tests.yml`) only runs the test matrix.

No GitHub *Release* objects are created and nothing is pushed automatically: the
release command runs with `--no-vcs-release` (so no `GH_TOKEN` is required) and
`--no-push` (the push is a separate, manual step after reviewing the result).

## Versioning

The version is computed automatically from the commit messages since the last
`vX.Y.Z` tag, following [Conventional Commits]:

| Commit prefix                  | Bump          |
| ------------------------------ | ------------- |
| `fix:` / `perf:`               | patch (0.7.5 → 0.7.6) |
| `feat:`                        | minor (0.7.5 → 0.8.0) |
| `feat!:` / `BREAKING CHANGE:`  | minor while in 0.x (see note) |
| `chore:`/`ci:`/`docs:`/`build:`/`refactor:`/`style:`/`test:` | no release |

The single source of truth for the version is `icinga2apic/__init__.py`;
`setup.cfg` derives it via `attr:`. Semantic-release bumps `__init__.py`,
updates `CHANGELOG.md` (above the `<!-- version list -->` marker), commits and
tags.

> Note: this project stays in the `0.x` series (`allow_zero_version = true`,
> `major_on_zero = false`), so breaking changes bump the minor, not to `1.0.0`.
> To deliberately release `1.0.0`, set `major_on_zero = true` in
> `pyproject.toml` for that release.

## One-time setup

Install the release tools into a virtual environment (do not install globally):

```bash
python -m venv .venv
.venv/bin/pip install python-semantic-release build twine
```

Activate it (`source .venv/bin/activate`) before running the release commands
below, or call the tools via `.venv/bin/...`. Alternatively, install the CLIs in
isolation with `pipx install python-semantic-release` and `pipx install twine`.

PyPI credentials are read from `~/.pypirc` (or a configured keyring).

## Cutting a release

From a clean, up-to-date `main`. The helper script enforces the gate (clean
tree, default branch, tests green, latest CI run green) before bumping:

```bash
./scripts/release.sh                 # gate + `semantic-release version` (no push)
git push origin main --follow-tags   # push the release commit and tag
twine upload dist/*                   # upload the built artifacts to PyPI
```

Equivalent manual flow without the script:

```bash
semantic-release version --no-push --no-vcs-release
git push origin main --follow-tags
twine upload dist/*
```

Preview the next release without changing anything:

```bash
semantic-release version --print            # print the next version only
semantic-release version --noop -v          # full dry run, no writes
```

Optionally attach the built artifacts to a GitHub Release as well (requires a
`GH_TOKEN` in the environment, e.g. `GH_TOKEN=$(gh auth token)`):

```bash
gh release create <tag> --generate-notes dist/*
```

[python-semantic-release]: https://python-semantic-release.readthedocs.io/
[Conventional Commits]: https://www.conventionalcommits.org/
