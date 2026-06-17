#!/usr/bin/env bash
#
# Local release helper for icinga2apic.
#
# Releases are published locally so the PyPI token is never stored in CI (it
# lives in ~/.pypirc / keyring on the machine running the release). CI in
# GitHub only runs the tests; this script enforces that those tests are green
# for the exact commit being released before anything is published.
#
# Flow:
#   1. sanity checks (on master, clean tree, in sync with origin)
#   2. gate: the latest "Tests" CI run for HEAD must have succeeded
#   3. semantic-release: derive version from commits, update CHANGELOG, build,
#      commit, tag and push, and create the GitHub release
#   4. twine: upload the built artifacts to PyPI with the local credentials
#
# Requirements (install locally, e.g. in a venv):
#   pip install python-semantic-release twine build
#   gh auth login                 # for the CI status check + GitHub release
#   ~/.pypirc or TWINE_* env      # PyPI credentials
#
set -euo pipefail

WORKFLOW="tests.yml"
BRANCH="master"

info() { printf '\033[1;34m==>\033[0m %s\n' "$*"; }
die()  { printf '\033[1;31mError:\033[0m %s\n' "$*" >&2; exit 1; }

# --- 1. sanity checks ------------------------------------------------------
current_branch="$(git rev-parse --abbrev-ref HEAD)"
[ "$current_branch" = "$BRANCH" ] || die "not on $BRANCH (on '$current_branch')"
[ -z "$(git status --porcelain)" ] || die "working tree is not clean"

info "Fetching origin..."
git fetch --quiet origin "$BRANCH"
local_sha="$(git rev-parse HEAD)"
remote_sha="$(git rev-parse "origin/$BRANCH")"
[ "$local_sha" = "$remote_sha" ] || \
  die "local $BRANCH ($local_sha) is not in sync with origin ($remote_sha); push first"

# --- 2. CI gate ------------------------------------------------------------
info "Checking CI status for $local_sha ..."
conclusion="$(gh run list --workflow="$WORKFLOW" --branch="$BRANCH" \
  --json headSha,status,conclusion \
  --jq "[.[] | select(.headSha==\"$local_sha\")] | .[0].conclusion")"

case "$conclusion" in
  success) info "CI is green." ;;
  "")      die "no completed '$WORKFLOW' run found for $local_sha; wait for CI to finish" ;;
  *)       die "CI for $local_sha is '$conclusion', not 'success'; aborting" ;;
esac

# --- 3. semantic-release ---------------------------------------------------
# Determines the next version from the commit history, updates setup.py +
# CHANGELOG.md, builds the artifacts, commits, tags, pushes and creates the
# GitHub release. Use VCS token via gh / GH_TOKEN.
info "Running semantic-release (version + build + tag + GitHub release)..."
semantic-release version
semantic-release publish   # uploads built dists to the GitHub release

# --- 4. PyPI upload (local credentials) ------------------------------------
info "Uploading to PyPI with twine (local credentials)..."
twine upload dist/*

info "Release done."
