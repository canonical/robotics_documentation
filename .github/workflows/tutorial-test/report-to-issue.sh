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

# Print the report file, or a placeholder when it is missing/empty. Never
# abort (this script runs with `set -e`) just because the agent produced no
# output.
print_report() {
  if [ -f "${REPORT_FILE}" ] && [ -s "${REPORT_FILE}" ]; then
    # The agent's streamed reply may include live commentary / task lists before
    # the final report. Print only the report: from the first `## Result:` line
    # onward (falls back to the whole file if no result line is present).
    if grep -qE '^## Result:' "${REPORT_FILE}"; then
      awk '/^## Result:/{found=1} found' "${REPORT_FILE}"
    else
      cat "${REPORT_FILE}"
    fi
  else
    echo "_No report was produced. The AI tester may have failed before running"
    echo "the tutorial (see the 'Run the tutorial with an AI agent' step log in"
    echo "the CI run for the underlying error)._"
  fi
}

# Print the captured environment facts as a nested metadata list (indented so
# it does not add its own `##` heading that would collide with the agent's
# report sections).
print_env() {
  if [ -f "${ENV_FILE:-}" ]; then
    sed 's/^/  /' "${ENV_FILE}"
  fi
}

# Always publish the report to the CI job summary (success and failure). The
# agent's report already contains its own `##` sections, so the wrapper only
# adds metadata bullets and never emits a competing heading.
{
  echo "# Tutorial test report"
  echo
  echo "- **Tutorial:** \`${TUTORIAL_PATH}\`"
  echo "- **Result:** ${RESULT}"
  echo "- **Model:** ${OPENCODE_MODEL:-unknown}"
  echo "- **Date:** ${DATE_UTC}"
  echo "- **Run:** ${RUN_URL}"
  echo "- **Environment:**"
  print_env
  echo
  print_report
} >> "${GITHUB_STEP_SUMMARY}"

# Open an issue when the tutorial is broken (FAIL) or when it works but has
# findings/suggestions worth acting on (WARN). PASS opens no issue.
echo "RESULT=${RESULT}"
if [ "${RESULT}" != "fail" ] && [ "${RESULT}" != "warn" ]; then
  echo "Tutorial test result is '${RESULT}'; not opening an issue."
  exit 0
fi

if [ "${RESULT}" = "fail" ]; then
  ISSUE_TITLE="Tutorial test failing: ${TUTORIAL_NAME}"
  ISSUE_INTRO="The automated tutorial test for **${TUTORIAL_NAME}** found problems."
else
  ISSUE_TITLE="Tutorial test feedback: ${TUTORIAL_NAME}"
  ISSUE_INTRO="The automated tutorial test for **${TUTORIAL_NAME}** completed, but found things worth changing."
fi
echo "Result is '${RESULT}'; opening a GitHub issue."

ISSUE_BODY_FILE="$(mktemp)"
{
  echo "${ISSUE_INTRO}"
  echo
  echo "- **Tutorial:** \`${TUTORIAL_PATH}\`"
  echo "- **Date:** ${DATE_UTC}"
  echo "- **Model:** ${OPENCODE_MODEL:-unknown}"
  echo "- **CI run:** ${RUN_URL}"
  echo "- **Environment:**"
  print_env
  echo
  print_report
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

# Create the issue. If this fails, surface the error and fail the step loudly
# rather than silently skipping the report the run was meant to produce.
if ISSUE_URL="$(gh issue create \
    --title "${ISSUE_TITLE}" \
    --label "tutorial-test" \
    --label "documentation" \
    --body-file "${ISSUE_BODY_FILE}")"; then
  echo "Opened issue: ${ISSUE_URL}"
else
  echo "::error::Failed to open the GitHub issue for the failing tutorial test." >&2
  rm -f "${ISSUE_BODY_FILE}"
  exit 1
fi

rm -f "${ISSUE_BODY_FILE}"
