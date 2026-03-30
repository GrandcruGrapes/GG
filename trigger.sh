#!/usr/bin/env bash
# Manually trigger the idealwine monitor workflow via the GitHub Actions API.
# Usage:
#   GITHUB_TOKEN=ghp_... bash trigger.sh
#   or export GITHUB_TOKEN first, then: bash trigger.sh

set -euo pipefail

OWNER="GrandcruGrapes"
REPO="GG"
WORKFLOW="monitor.yml"
BRANCH="main"
TOKEN="${GITHUB_TOKEN:?GITHUB_TOKEN is not set}"

curl -s -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "https://api.github.com/repos/${OWNER}/${REPO}/actions/workflows/${WORKFLOW}/dispatches" \
  -d "{\"ref\":\"${BRANCH}\"}" \
  && echo "Workflow dispatched — check the Actions tab on GitHub."
