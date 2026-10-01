#!/usr/bin/env bash
# Prepares a harness checkout so that every step in the README works: fetches the corpus from
# Hugging Face into the layout the harness expects (data/items/*.jsonl + data/items/schema.json),
# installs this repo's run script and vLLM helpers into it.
#
# Usage: scripts/setup_harness.sh [HARNESS_DIR]
set -euo pipefail

RUNS="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HARNESS="$RUNS/../Bharat-Knowledge-Probe-Benchmark"
[ $# -ge 1 ] && HARNESS="$1"

if [ ! -d "$HARNESS/.git" ]; then
  git clone https://github.com/sthanika-ai/Bharat-Knowledge-Probe-Benchmark.git "$HARNESS"
fi
HARNESS="$(cd "$HARNESS" && pwd)"

# Corpus: the HF dataset is auto-gated, so a plain `git clone` fails. Accept the terms on the
# dataset page once, then authenticate (`huggingface-cli login` or `export HF_TOKEN=...`).
# Set BKP_DATASET_DIR to an already-downloaded copy to skip the download.
# The HF repo stores items under data/items and the schema at data/schema.json, whereas the
# harness reads data/items/*.jsonl and data/items/schema.json.
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
if [ -n "${BKP_DATASET_DIR:-}" ]; then
  HF="$BKP_DATASET_DIR"
else
  HF="$(python - <<'PY'
from huggingface_hub import snapshot_download
print(snapshot_download("sthanika-ai/Bharat-Knowledge-Probe-Benchmark", repo_type="dataset"))
PY
)"
fi
mkdir -p "$HARNESS/data/items" "$HARNESS/scripts/vllm_infra"
cp "$HF"/data/items/*.jsonl "$HARNESS/data/items/"
cp "$HF/data/schema.json" "$HARNESS/data/items/schema.json"

cp "$RUNS/configs/run_eval.py"              "$HARNESS/scripts/run_eval.py"
cp "$RUNS"/scripts/vllm_infra/*             "$HARNESS/scripts/vllm_infra/"

echo "Harness ready at $HARNESS"
