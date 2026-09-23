#!/usr/bin/env bash
#
# Publish the tutorial test report: always write it to the job summary and,
# when problems were found, open a new GitHub issue with the full details.
#
# Environment:
#   RESULT          pass | fail (required).
#   REPORT_FILE     Path to the agent's markdown report (required).
#   ENV_FILE        Path to the captured environment details (optional).
#   TUTORIAL_PATH   Path of the tutorial that was tested (required).
#   OPENCODE_MODEL  Model used (for the report metadata).
#   GH_TOKEN        Token used by `gh` to open the issue (required when failing).
#
set -euo pipefail

RESULT="${RESULT:?RESULT must be set (pass|fail)}"
REPORT_FILE="${REPORT_FILE:?REPORT_FILE must be set}"
TUTORIAL_PATH="${TUTORIAL_PATH:?TUTORIAL_PATH must be set}"
TUTORIAL_NAME="$(basename "${TUTORIAL_PATH}" .md)"
DATE_UTC="$(date -u '+%Y-%m-%d %H:%M UTC')"
RUN_URL="${GITHUB_SERVER_URL:-https://github.com}/${GITHUB_REPOSITORY:-}/actions/runs/${GITHUB_RUN_ID:-}"

# Always publish the report to the CI job summary (success and failure).
{
  echo "# Tutorial test report"
  echo
  echo "- **Tutorial:** \`${TUTORIAL_PATH}\`"
  echo "- **Result:** ${RESULT}"
  echo "- **Model:** ${OPENCODE_MODEL:-unknown}"
  echo "- **Date:** ${DATE_UTC}"
  echo "- **Run:** ${RUN_URL}"
  echo
  if [ -f "${ENV_FILE:-}" ]; then
    echo "## Environment"
    echo
    cat "${ENV_FILE}"
    echo
  fi
  echo "## Report"
  echo
  cat "${REPORT_FILE}"
} >> "${GITHUB_STEP_SUMMARY}"

# Only open an issue when the tutorial is broken.
if [ "${RESULT}" != "fail" ]; then
  echo "Tutorial test passed; no issue opened."
  exit 0
fi

ISSUE_TITLE="Tutorial test failing: ${TUTORIAL_NAME}"
ISSUE_BODY_FILE="$(mktemp)"
{
  echo "The automated tutorial test for **${TUTORIAL_NAME}** found problems."
  echo
  echo "- **Tutorial:** \`${TUTORIAL_PATH}\`"
  echo "- **Date:** ${DATE_UTC}"
  echo "- **Model:** ${OPENCODE_MODEL:-unknown}"
  echo "- **CI run:** ${RUN_URL}"
  echo
  if [ -f "${ENV_FILE:-}" ]; then
    echo "## Environment"
    echo
    cat "${ENV_FILE}"
    echo
  fi
  echo "## Report"
  echo
  cat "${REPORT_FILE}"
  echo
  echo "---"
  echo "_Filed automatically by the tutorial-test workflow. Known-acceptable"
  echo "behaviour can be recorded under \`.github/workflows/tutorial-test/.agents/\` so it is"
  echo "not reported again._"
} > "${ISSUE_BODY_FILE}"

# Best-effort: ensure the labels exist so the issue can be tagged; never fail.
for LABEL in tutorial-test documentation; do
  gh label create "${LABEL}" --force >/dev/null 2>&1 || true
done

gh issue create \
  --title "${ISSUE_TITLE}" \
  --label "tutorial-test" \
  --label "documentation" \
  --body-file "${ISSUE_BODY_FILE}"

rm -f "${ISSUE_BODY_FILE}"
