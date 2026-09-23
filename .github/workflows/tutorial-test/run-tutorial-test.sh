#!/usr/bin/env bash
#
# Run an AI agent over a documentation tutorial and capture its report.
#
# The script installs opencode from the snap, prepares the environment the
# tutorial expects (snapd/snapcraft/LXD backend), and drives a non-interactive
# `opencode run` session that follows the tutorial and emits a markdown report.
#
# Environment:
#   OPENROUTER_API_KEY   OpenRouter API key (required).
#   OPENCODE_MODEL       Model in provider/model form (default: openrouter/moonshotai/kimi-k3).
#   TUTORIAL_PATH        Path to the tutorial file to test (required).
#   REPORT_FILE          Where to write the agent's markdown report.
#
set -euo pipefail

TUTORIAL_PATH="${TUTORIAL_PATH:?TUTORIAL_PATH must point to the tutorial file to test}"
REPORT_FILE="${REPORT_FILE:?REPORT_FILE must be set}"
OPENCODE_MODEL="${OPENCODE_MODEL:-openrouter/moonshotai/kimi-k3}"
WORKFLOWS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

export OPENCODE_CONFIG="${WORKFLOWS_DIR}/tutorial-test/opencode.json"
# The tester config loads instructions relative to its own directory, so run
# opencode from the tutorial-test directory where the isolated .agents/ lives.
cd "${WORKFLOWS_DIR}/tutorial-test"

echo "::group::Install opencode (snap)"
sudo snap install opencode --classic
opencode --version
echo "::endgroup::"

echo "::group::Prepare tutorial environment"
sudo apt-get update
sudo apt-get install -y snapd
sudo snap install snapcraft --classic
sudo snap install lxd
sudo lxd init --auto
# Snapcraft's default backend (multipass) is unavailable on hosted runners;
# use the LXD backend (a known, documented deviation for CI).
export SNAPCRAFT_BUILD_ENVIRONMENT=lxd
echo "::endgroup::"

echo "::group::Capture environment for the report"
{
  echo "- Date: $(date -u '+%Y-%m-%d %H:%M UTC')"
  echo "- Runner image: ${RUNNER_IMAGE:-${ImageOS:-unknown}}"
  echo "- opencode: $(opencode --version 2>/dev/null || echo unknown)"
  echo "- Model: ${OPENCODE_MODEL}"
  echo "- snapd: $(snap version 2>/dev/null | tr '\n' '; ' || echo unknown)"
  echo "- snapcraft: $(snapcraft --version 2>/dev/null || echo unknown)"
  echo "- lxd: $(lxd --version 2>/dev/null || echo unknown)"
} | tee "${ENV_FILE:-/tmp/tutorial-env.txt}"
echo "::endgroup::"

echo "::group::Run tutorial test"
PROMPT_FILE="$(mktemp)"
cat > "${PROMPT_FILE}" <<EOF
Follow the tutorial at "${TUTORIAL_PATH}" step by step, exactly as a reader
would, on this machine. Execute every command it contains in order, in your
shell. Apply the tester behaviour and known deviations described in your
instructions, and finish with a report that begins with a "## Result: PASS" or
"## Result: FAIL" line and then the "## Environment", "## Steps performed",
"## Findings", and "## Suggested changes" sections.
EOF

# `--pure` isolates the run from any external/global plugins.
if opencode run --pure --model "${OPENCODE_MODEL}" "$(cat "${PROMPT_FILE}")" | tee "${REPORT_FILE}"; then
  echo "opencode run completed."
else
  echo "::warning::opencode run exited non-zero; continuing so we can report it."
fi
rm -f "${PROMPT_FILE}"
echo "::endgroup::"

# Surface the result to the workflow regardless of the agent's exit code.
if grep -qE '^## Result: *FAIL' "${REPORT_FILE}"; then
  echo "RESULT=fail" >> "${GITHUB_OUTPUT}"
elif grep -qE '^## Result: *PASS' "${REPORT_FILE}"; then
  echo "RESULT=pass" >> "${GITHUB_OUTPUT}"
else
  echo "::warning::No '## Result:' line found in the report; treating as failure."
  echo "RESULT=fail" >> "${GITHUB_OUTPUT}"
fi
