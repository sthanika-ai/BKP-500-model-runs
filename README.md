# BKP-500 Model Runs

[![License](https://img.shields.io/badge/code-Apache--2.0-blue.svg)](LICENSE)
[![Harness](https://img.shields.io/badge/harness-sthanika--ai%2FBharat--Knowledge--Probe--Benchmark-blue.svg)](https://github.com/sthanika-ai/Bharat-Knowledge-Probe-Benchmark)
[![Dataset](https://img.shields.io/badge/🤗%20dataset-sthanika--ai%2FBharat--Knowledge--Probe--Benchmark-yellow.svg)](https://huggingface.co/datasets/sthanika-ai/Bharat-Knowledge-Probe-Benchmark)

Exact run configuration and the full leaderboard for [BKP-500 (Bharat Knowledge Probe)](https://github.com/sthanika-ai/Bharat-Knowledge-Probe-Benchmark)
— a benchmark measuring whether language models know India-specific locale conventions (Indian
numeral magnitudes, state-specific land units, traditional mass units, the Indian fiscal year,
agricultural crop seasons, government schemes, and structural identifiers).

This repository presents a completed evaluation campaign: **19 models, the full 552-item
corpus, 2 prompt regimes, 3 samples each = 3,312 scored rows per model.** Every reported figure traces back to a raw model response
through this pipeline (`configs/run_eval.py` → `results/<model>/full.jsonl` →
`scripts/build_report_data.py` → `reports/report_data.json`/`reports/bkp500_report.html`), so
results can be independently reproduced or audited rather than taken on faith.

BKP-500 is this project's own benchmark, not an adopted third-party one — this repo is the
configuration-and-results companion to [the harness](https://github.com/sthanika-ai/Bharat-Knowledge-Probe-Benchmark)
itself, documenting *how* each model on the leaderboard was actually run so any number below
can be independently reproduced. Raw per-model responses aren't hosted here; rerun a model
against its config below to regenerate them.

## 1. Results

Ranked by Bharat Score (macro-mean accuracy across all 7 categories), tiered by chained
bootstrap-CI overlap.

| tier | model | bucket | bharat score (95% CI) | oom error rate | unit discipline | refusal rate | consistency |
|---|---|---|---|---|---|---|---|
| 1 | Qwen3.6 27B | global | 53.2% (48.9–57.3) | 10.6% | 84.9% | 0.7% | 100.0% |
| 1 | gpt-oss-20b | global | 46.9% (43.0–50.9) | 16.5% | 84.6% | 0.1% | 87.6% |
| 1 | Sarvam-M 24B | india | 45.2% (40.9–49.2) | 22.2% | 89.1% | 3.1% | 90.7% |
| 1 | Gemma 3 27B | global | 41.8% (38.3–45.8) | 18.4% | 85.3% | 0.0% | 99.6% |
| 1 | Qwen3-VL 8B | global | 39.2% (35.1–43.4) | 20.5% | 80.8% | 0.0% | 97.1% |
| 1 | Mistral Small 3.1 24B | global | 38.8% (35.0–42.9) | 17.1% | 68.8% | 0.6% | 97.7% |
| 1 | Krutrim-2 12B | india | 38.7% (34.6–43.3) | 24.1% | 82.3% | 0.2% | 99.5% |
| 1 | Phi-4 14B | global | 38.7% (34.8–43.0) | 21.2% | 81.6% | 2.1% | 99.0% |
| 1 | Sarvam 30B | india | 37.1% (33.5–40.9) | 33.7% | 90.5% | 1.3% | 86.7% |
| 1 | Gemma 3 12B | global | 35.1% (31.3–39.4) | 25.6% | 83.2% | 0.0% | 99.6% |
| 1 | Llama 3.1 8B Instruct | global | 32.6% (28.5–36.7) | 32.9% | 77.9% | 2.9% | 100.0% |
| 1 | Qwen2.5 7B | global | 30.9% (27.1–34.8) | 23.1% | 82.9% | 0.1% | 97.9% |
| 1 | Gemma 3 4B | global | 25.3% (22.1–28.8) | 33.7% | 75.9% | 0.0% | 100.0% |
| 1 | Navarasa 2.0 7B | india | 20.6% (17.8–23.6) | 44.3% | 74.7% | 0.6% | 93.1% |
| 2 | Param-1 2.9B | india | 14.3% (11.8–16.9) | 54.2% | 60.4% | 0.6% | 99.7% |
| 2 | Sarvam-1 2B | india | 11.6% (9.1–14.8) | 56.7% | 47.5% | 1.5% | 99.7% |
| 2 | OpenHathi 7B | india | 11.2% (8.7–14.2) | 52.3% | 65.8% | 0.1% | 96.1% |
| 2 | Airavata 7B | india | 7.9% (5.6–10.4) | 22.7% | 14.5% | 38.5% | 99.9% |
| 2 | Gemma 3 12B INT4 | global | 4.6% (2.4–7.2) | 1.4% | 2.0% | 91.3% | 100.0% |

*OOM error rate = share of numeric answers off by ≥10× (a lakh/crore-scale slip). Unit discipline
= share of `numeric_with_unit` answers that included an explicit, correct unit. n_resamples=2,000
for every bootstrap CI above (the harness's own `scripts/build_leaderboard.py` defaults to 10,000
for a publication-grade run).*

### Per-category accuracy — all 19 models × 7 categories

| model | numerals | weights/vol | land units | seasons | fiscal yr | schemes | identifiers |
|---|---|---|---|---|---|---|---|
| Qwen3.6 27B | 77.9 | 61.1 | 39.4 | 48.9 | 52.9 | 41.9 | 50.0 |
| gpt-oss-20b | 78.7 | 57.6 | 34.9 | 41.2 | 46.7 | 25.4 | 43.3 |
| Sarvam-M 24B | 46.4 | 55.8 | 21.5 | 54.6 | 49.0 | 36.5 | 52.2 |
| Gemma 3 27B | 54.0 | 54.9 | 26.4 | 38.5 | 50.6 | 36.0 | 32.2 |
| Qwen3-VL 8B | 55.4 | 39.4 | 31.2 | 42.1 | 39.8 | 29.7 | 36.7 |
| Mistral Small 3.1 24B | 50.6 | 59.0 | 26.1 | 42.9 | 32.2 | 31.1 | 30.0 |
| Krutrim-2 12B | 49.2 | 39.6 | 24.5 | 44.7 | 42.9 | 39.9 | 30.0 |
| Phi-4 14B | 46.1 | 53.5 | 24.2 | 42.1 | 46.1 | 32.2 | 26.7 |
| Sarvam 30B | 40.7 | 51.2 | 28.8 | 51.1 | 33.1 | 27.9 | 26.7 |
| Gemma 3 12B | 48.8 | 40.7 | 20.8 | 41.9 | 37.8 | 29.0 | 26.7 |
| Llama 3.1 8B Instruct | 32.0 | 25.7 | 16.8 | 39.6 | 38.2 | 35.1 | 40.0 |
| Qwen2.5 7B | 44.6 | 37.7 | 17.5 | 32.4 | 34.5 | 16.0 | 33.3 |
| Gemma 3 4B | 32.9 | 24.3 | 12.5 | 34.6 | 31.2 | 18.2 | 23.3 |
| Navarasa 2.0 7B | 26.1 | 21.5 | 10.6 | 25.1 | 30.4 | 17.6 | 13.3 |
| Param-1 2.9B | 15.2 | 11.1 | 4.0 | 25.8 | 15.3 | 15.5 | 13.3 |
| Sarvam-1 2B | 16.2 | 2.8 | 2.4 | 18.5 | 12.8 | 14.9 | 13.3 |
| OpenHathi 7B | 13.1 | 4.9 | 2.2 | 15.4 | 16.7 | 8.8 | 17.8 |
| Airavata 7B | 6.9 | 4.9 | 1.4 | 12.6 | 11.8 | 4.0 | 13.3 |
| Gemma 3 12B INT4 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 12.2 | 20.0 |

*Land units by state is the single weakest category for 14 of these 19 models.*

Qwen3.6 27B leads the roster — a global open-weight model, not an India-built one. Sarvam-M 24B
is the strongest India-built/tuned model, holding rank 3 outright. **Land units by state** is the
single weakest category for 14 of the 19 models: state-by-state variation in land-unit
definitions (a *bigha* in Punjab isn't a *bigha* in Bihar) appears to be genuinely harder for
every model family tested than any other category in the corpus.

## 2. Models evaluated

**19 curated configs in `configs/models/`** — one YAML per model with a row in the table above,
named `<model_id>.yaml` (same key as `configs/run_eval.py`'s `MODELS` dict and
`configs/model_registry.json`). Spanning local open-weight models served via vLLM, a plain
`transformers` HF pipeline, or Ollama — every model here is self-hosted, never a paid third-party
API. See `configs/README.md` for the schema and naming conventions.

## 3. Repository structure

```
configs/
  run_eval.py           the exact CLI entrypoint that produced every score above — includes the
                         per-model engineering notes (batch sizing, quantization choices, backend
                         workarounds) behind each configuration decision
  model_registry.json   a clean, structured extraction of the same configuration (backend,
                         HF repo + revision pin, decoding settings) for anyone who wants the
                         data without reading Python
  models/*.yaml          one human-readable config per model, derived from run_eval.py's MODELS
                         dict — see configs/README.md for the schema and, importantly, what
                         these configs do *not* capture (§10 below)
  README.md             config schema, naming conventions, and known reproducibility gaps
requirements.txt         pinned versions for the harness's local-inference backends (hf/vllm/
                          ollama-via-openai-client) — install into the harness checkout, see §4
CITATION.cff, LICENSE    citation metadata and the Apache-2.0 license this repo's own content
                          is released under
```

The harness itself (adapters, graders, scoring, statistics, `bkp_eval`/`bharat_units` packages)
lives in a separate repository — see Related repositories at the bottom.

## 4. Installation

```bash
git clone https://github.com/sthanika-ai/Bharat-Knowledge-Probe-Benchmark.git
cd Bharat-Knowledge-Probe-Benchmark
pip install -e ".[dev]"                    # harness code + dev tooling (pytest, mypy, ruff)

python3.12 -m venv .venv-vllm
source .venv-vllm/bin/activate
pip install -r /path/to/BKP-500-model-runs/requirements.txt   # vllm/torch/transformers/etc.
```

Requires Python ≥3.10 for the harness itself; `requirements.txt`'s pinned `vllm`/`torch` wheels
require Python 3.12 specifically (see that file's header comment). `pip install -e ".[dev]"`
alone does **not** install anything needed to actually serve a model — `requirements.txt` is a
separate, additional install step, not covered by the harness's own `pyproject.toml`.

Add the `hf-datasets` extra to the harness install if you'll load the corpus straight from the
Hub in the next step rather than a local checkout:

```bash
pip install -e ".[hf-datasets]"
```

## 5. Configuration

No API keys are needed — every model here is self-hosted. What you do need:

- **Hugging Face access** for any gated checkpoint or its ungated mirror's parent repo — most
  models in this roster use an explicitly-chosen ungated mirror for exactly this reason (noted
  per-model in `configs/models/*.yaml`). Authenticate with `huggingface-cli login` or
  `export HF_TOKEN=...`.
- **The BKP-500 corpus itself**, from Hugging Face (see step 2 below) — not gated, but not
  bundled in this repo either.
- **A `vllm serve` process already running** for any `serving_backend: vllm` config, before
  invoking `run_eval.py` — see §6.

### Get the BKP-500 corpus

Either clone it into `data/` inside the harness checkout (matches the on-disk layout
`load_corpus()` expects by default):

```bash
git clone https://huggingface.co/datasets/sthanika-ai/Bharat-Knowledge-Probe-Benchmark data
```

...or load it straight from the Hub in Python, no local checkout needed:

```python
from bkp_eval.items import load_corpus_from_hf

corpus = load_corpus_from_hf()   # sthanika-ai/Bharat-Knowledge-Probe-Benchmark, every category
```

## 6. Running an evaluation

Drop this repo's run config into the harness checkout first — `configs/run_eval.py` here is the
exact script that produced every row of the leaderboard above; it imports `bkp_eval` directly,
so it needs to sit inside the harness checkout's own `scripts/` directory (overwriting the
harness's own copy of the same file is fine — this one already has every model, port, and
config value baked in):

```bash
cp /path/to/BKP-500-model-runs/configs/run_eval.py scripts/run_eval.py
```

```bash
# self-hosted backends (vllm / hf / ollama) - no API key needed, matches every model in this repo
python scripts/run_eval.py --model qwen3.6-27b --mode smoke   # small sanity run first
python scripts/run_eval.py --model qwen3.6-27b --mode full    # every item, 3 samples, R1+R2
```

`--model` must be a key in `MODELS` inside `run_eval.py` (same set as `configs/model_registry.json`
and `configs/models/*.yaml`). For a `vllm`-backend entry, **start that model's `vllm serve ...`
command yourself first** — `run_eval.py` only calls an already-running server, it never launches
one; the exact command (repo id, port, `gpu_memory_utilization`, `max_model_len`, any extra
flags) is in that model's `configs/models/<model_id>.yaml` under `vllm_launch`. For `hf`-backend
entries, `run_eval.py` loads the model in-process via `transformers`, no server needed. Output
lands in `results/<model>/{smoke,full}.jsonl` plus a matching `*_report.txt` scored by the
harness's own grader — score it directly with `python -m bkp_eval.score results/<model>/full.jsonl`.

**`sarvam-m` and `sarvam-30b` need one extra step**: run
`python scripts/vllm_infra/hotpatch_vllm.py` against your `.venv-vllm` install before their
`vllm serve` command will start at all (registers their custom MoE/MLA architecture classes —
native support is still an open upstream vLLM PR).

## 7. Reproducing results

1. Complete §4 (Installation) and §5 (Configuration).
2. Run the harness's own test suite (`pytest`) to confirm the install is sound before spending
   GPU-hours on anything.
3. For a `vllm`-backend model, start its server per that model's `configs/models/<model_id>.yaml`
   (`vllm_launch` fields), applying the hotpatch first if it's `sarvam-m`/`sarvam-30b`.
4. `python scripts/run_eval.py --model <model_id> --mode smoke` — confirms the adapter, prompt,
   and grading pipeline work end-to-end before a multi-hour full run.
5. `python scripts/run_eval.py --model <model_id> --mode full` — the real run: every item,
   R1+R2, 3 samples.
6. `PYTHONPATH=src python scripts/build_report_data.py` (from the harness checkout, with this
   repo's `results/` populated) regenerates `reports/report_data.json` — every number in this
   README's leaderboard traces back to that file.

## 8. Results and analysis

Running the pipeline yourself (§6/§7), or reading the versions of these files already in this
repo/the harness checkout, gives you:

- `reports/report_data.json` — every number in this README's tables, plus per-regime (R1/R2)
  breakdowns, the India-built-vs-global bucket comparison, a cross-model hardest-items ranking,
  and a human-review coverage summary. Computed by `scripts/build_report_data.py`, which reads
  every `results/<model>/full.jsonl` (the model roster is discovered by globbing, never
  hardcoded) and calls straight into the harness's own `bkp_eval.score`/`bkp_eval.stats`.
- `reports/bkp500_report.html` — a fully auto-generated narrative report (`reports/build_showcase_report.py`);
  every number and callout in it is pulled live from `report_data.json`, nothing hand-typed.
- `reports/model_results.csv` — the leaderboard table in flat CSV form.

## 9. Known limitations
- **All 552 rows have passed the required two-reviewer check** (`adjudicated: true`, `split:
  test`) — see the dataset card for details. A contamination-resistant public-dev/gated-test
  split is still planned but not yet built.
- **Hardware**: this project ran on GPUs with 80GB VRAM each. `gpu_memory_utilization` in
  `configs/models/*.yaml` is a fraction of a GPU's *total* VRAM, not of model size — expect a
  different real memory budget, and possibly OOM, on a smaller GPU.
- **No LLM judge is involved in scoring anywhere** — every response is graded deterministically
  by the harness's own per-answer-type grader code.

## 10. Citation

If you use this leaderboard or these model configurations, please cite as in
[`CITATION.cff`](CITATION.cff). If you use the BKP-500 benchmark itself, cite
[the harness repository](https://github.com/sthanika-ai/Bharat-Knowledge-Probe-Benchmark).

## License

Apache-2.0 (see [`LICENSE`](LICENSE)) — matching the eval harness. The benchmark dataset itself is
licensed separately; see [its repository](https://huggingface.co/datasets/sthanika-ai/Bharat-Knowledge-Probe-Benchmark)
for terms.

## Related repositories

- [**Bharat-Knowledge-Probe-Benchmark**](https://github.com/sthanika-ai/Bharat-Knowledge-Probe-Benchmark) — the evaluation harness (adapters, graders, scoring, statistics)
- [**BKP-500 dataset**](https://huggingface.co/datasets/sthanika-ai/Bharat-Knowledge-Probe-Benchmark) — the corpus itself, on Hugging Face
