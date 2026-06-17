# Releasing & versioning

This project uses [Conventional Commits](https://www.conventionalcommits.org/)
and [python-semantic-release](https://python-semantic-release.readthedocs.io/)
(configured in `pyproject.toml` under `[tool.semantic_release]`).

**The version is derived from the commit history — never edit `__version__`
by hand.** `setup.py:__version__`, the git tag and the PyPI release are kept in
sync automatically by the release process.

## How commits map to versions

The project stays in the `0.x` range (`major_on_zero = false`), so:

| Commit type                         | Example                                  | Bump            |
| ----------------------------------- | ---------------------------------------- | --------------- |
| `fix:`                              | `fix(actions): correct filter encoding`  | patch (0.7.5 → 0.7.6) |
| `feat:`                             | `feat(events): add subscribe_now()`      | minor (0.7.5 → 0.8.0) |
| `BREAKING CHANGE:` / `feat!:`       | footer or `!` after the type             | minor while 0.x |
| `chore:`, `docs:`, `refactor:`, `test:`, `ci:`, `style:` | — | no release |

## Test ↔ release coordination

CI publishes nothing — it only runs the tests. Release credentials are never
stored in CI; the release is always published locally by whoever cuts it. The
ordering "tests first, then release" is enforced as follows:

```
.github/workflows/tests.yml   (push / pull_request)   → test matrix 3.8–3.12
                              ▲
scripts/release.sh (run locally)
   1. on master, clean tree, in sync with origin
   2. GATE: the latest Tests run for HEAD must be "success" (checked via gh)
   3. semantic-release: version + CHANGELOG + tag + push + GitHub release
   4. twine upload dist/*   → PyPI, using your local credentials
```

If CI for the exact commit is not green, the script aborts before anything is
published.

## One-time local setup

```sh
python -m venv .venv && . .venv/bin/activate
pip install python-semantic-release twine build
gh auth login                 # used for the CI status check and GitHub release
# PyPI credentials in ~/.pypirc or the TWINE_USERNAME / TWINE_PASSWORD env vars
```

## Cutting a release

1. Land your changes on `master` using Conventional Commit messages and push.
2. Wait for the **Tests** workflow on GitHub to go green.
3. Run the release locally:

   ```sh
   ./scripts/release.sh
   # or: make release
   ```

That's it — `setup.py`, `CHANGELOG.md`, the `vX.Y.Z` git tag, the GitHub
release and PyPI all end up on the same version.

### Manual fallback

If you ever need to do it by hand (after confirming CI is green):

```sh
semantic-release version     # bump, changelog, build, commit, tag, push
semantic-release publish     # attach artifacts to the GitHub release
twine upload dist/*          # PyPI
```

To preview what the next version would be without changing anything:

```sh
semantic-release version --print
```
