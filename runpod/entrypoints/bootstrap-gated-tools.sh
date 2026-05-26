#!/usr/bin/env bash
set -euo pipefail

echo "license-gated tool bootstrap is intentionally fail-closed in the public repo." >&2
echo "Use operator-owned scripts outside git after current license, credential, and budget review." >&2
exit 2
