#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="${CRYOCORE_REPO_ROOT:-/workspace/biosymphony-cryocore-public}"
REPO_URL="${CRYOCORE_REPO_URL:-}"
GIT_REF="${CRYOCORE_GIT_REF:-main}"

if [[ -z "${REPO_URL}" ]]; then
  echo "bootstrap-repo blocked: CRYOCORE_REPO_URL is required and must point to a public or operator-authorized repo." >&2
  exit 2
fi

mkdir -p "$(dirname "${REPO_ROOT}")"
if [[ -d "${REPO_ROOT}/.git" ]]; then
  git -C "${REPO_ROOT}" fetch --depth=1 origin "${GIT_REF}"
else
  rm -rf "${REPO_ROOT}"
  git init -q "${REPO_ROOT}"
  git -C "${REPO_ROOT}" remote add origin "${REPO_URL}"
  git -C "${REPO_ROOT}" fetch --depth=1 origin "${GIT_REF}"
fi
git -C "${REPO_ROOT}" checkout --detach FETCH_HEAD
echo "bootstrapped CryoCore repo at ${REPO_ROOT}"
