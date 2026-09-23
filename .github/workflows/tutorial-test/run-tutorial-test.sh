#!/usr/bin/env bash
#
# Run an AI agent over a documentation tutorial and capture its report.
#
# The script installs opencode from the snap, prepares the environment the
# tutorial expects (snapd/snapcraft/LXD backend + container networking), and
# drives a non-interactive `opencode run` session that follows the tutorial and
# emits a markdown report.
#
# Environment:
#   OPENROUTER_API_KEY   OpenRouter API key (required).
#   OPENCODE_MODEL       Model in provider/model form (default: openrouter/moonshotai/kimi-k3).
#   TUTORIAL_PATH        Path to the tutorial file to test (required).
#   REPORT_FILE          Where to write the agent's markdown report.
#   ENV_FILE             Where to write captured environment facts.
#
set -euo pipefail

TUTORIAL_PATH="${TUTORIAL_PATH:?TUTORIAL_PATH must point to the tutorial file to test}"
REPORT_FILE="${REPORT_FILE:?REPORT_FILE must be set}"
ENV_FILE="${ENV_FILE:-tutorial-env.txt}"
OPENCODE_MODEL="${OPENCODE_MODEL:-openrouter/moonshotai/kimi-k3}"

# Repo root (two levels above this script) and the agent's clean working dir.
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
WORK_DIR="${HOME}/tutorial-test"
mkdir -p "${WORK_DIR}"

export OPENCODE_CONFIG="${REPO_ROOT}/.github/workflows/tutorial-test/opencode.json"
# The tester config loads its instructions relative to its own directory; the
# agent itself runs from a clean HOME dir so artifacts (clones, builds) stay
# out of the repo and relative commands behave like a real user's shell.
cd "${WORK_DIR}"

# Make REPORT_FILE / ENV_FILE absolute so downstream steps find them regardless
# of their own working directory.
REPORT_FILE="${WORK_DIR}/$(basename "${REPORT_FILE}")"
ENV_FILE="${WORK_DIR}/$(basename "${ENV_FILE}")"
echo "REPORT_FILE=${REPORT_FILE}" >> "${GITHUB_OUTPUT}"
echo "ENV_FILE=${ENV_FILE}" >> "${GITHUB_OUTPUT}"

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
# Allow `runner` (and the agent) to talk to the LXD socket without sudo.
sudo usermod -aG lxd "${USER}" || true
# Snapcraft's default backend (multipass) is unavailable on hosted runners;
# use the LXD backend (a known, documented deviation for CI).
export SNAPCRAFT_BUILD_ENVIRONMENT=lxd
# Hosted runners ship with Docker, which sets the iptables FORWARD policy to
# DROP and breaks LXD container networking. Accept traffic on the LXD bridge.
if command -v iptables >/dev/null 2>&1 && sudo iptables -L DOCKER-USER -n >/dev/null 2>&1; then
  sudo iptables -I DOCKER-USER -i lxdbr0 -j ACCEPT || true
  sudo iptables -I DOCKER-USER -o lxdbr0 -j ACCEPT || true
fi
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
} | tee "${ENV_FILE}"
echo "::endgroup::"

echo "::group::Run tutorial test"
# Always start from an existing (empty) report so downstream steps never fail
# reading it even if the agent produces no output at all.
: > "${REPORT_FILE}"
TUTORIAL_ABS="${REPO_ROOT}/${TUTORIAL_PATH}"
PROMPT_FILE="$(mktemp)"
cat > "${PROMPT_FILE}" <<EOF
Follow the tutorial at "${TUTORIAL_ABS}" step by step, exactly as a reader
would, on this machine. Execute every command it contains in order, in your
shell, from your current working directory. Apply the tester behaviour and
known deviations described in your instructions, and finish with a report that
begins with a "## Result: PASS" or "## Result: FAIL" line and then the
"## Environment", "## Steps performed", "## Findings", and
"## Suggested changes" sections.
EOF

# `--pure` isolates the run from any external/global plugins; `--auto`
# auto-approves permission requests so a headless CI run never blocks waiting
# for approval (this machine is disposable).
if opencode run --pure --auto --model "${OPENCODE_MODEL}" "$(cat "${PROMPT_FILE}")" | tee "${REPORT_FILE}"; then
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
