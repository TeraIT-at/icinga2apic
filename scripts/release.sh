#!/usr/bin/env bash
#
# Release gate: refuses to cut a release unless the tree is clean, on the
# default branch, the test suite passes, and (if gh is available) the latest
# CI run on the branch is green. On success it runs semantic-release locally
# WITHOUT pushing and WITHOUT creating a GitHub release; the push and the PyPI
# upload remain explicit manual steps (see RELEASING.md).
set -euo pipefail

BRANCH="$(git rev-parse --abbrev-ref HEAD)"
DEFAULT_BRANCH="main"

if [ "$BRANCH" != "$DEFAULT_BRANCH" ]; then
    echo "ERROR: releases are cut from '$DEFAULT_BRANCH', current branch is '$BRANCH'." >&2
    exit 1
fi

if [ -n "$(git status --porcelain)" ]; then
    echo "ERROR: working tree is not clean. Commit or stash changes first." >&2
    exit 1
fi

echo ">> Running the test suite..."
pytest tests/ -q

# Optional: refuse if the latest CI run on the branch did not succeed.
if command -v gh >/dev/null 2>&1; then
    echo ">> Checking latest CI run on '$BRANCH'..."
    CONCLUSION="$(gh run list --branch "$BRANCH" --limit 1 --json conclusion --jq '.[0].conclusion' 2>/dev/null || true)"
    if [ -n "$CONCLUSION" ] && [ "$CONCLUSION" != "success" ]; then
        echo "ERROR: latest CI run on '$BRANCH' concluded '$CONCLUSION', not 'success'." >&2
        exit 1
    fi
fi

echo ">> Tests green. Bumping version locally (no push, no GitHub release)..."
semantic-release version --no-push --no-vcs-release

echo
echo "Done. Review the result, then finish the release manually:"
echo "  git push origin $DEFAULT_BRANCH --follow-tags"
echo "  twine upload dist/*"
echo "  # optional GitHub release: gh release create <tag> --generate-notes dist/*"
