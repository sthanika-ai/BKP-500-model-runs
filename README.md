# BKP-500 Model Runs

[![License](https://img.shields.io/badge/code-Apache--2.0-blue.svg)](LICENSE)
[![Harness](https://img.shields.io/badge/harness-sthanika--ai%2FBharat--Knowledge--Probe--Benchmark-blue.svg)](https://github.com/sthanika-ai/Bharat-Knowledge-Probe-Benchmark)
[![Dataset](https://img.shields.io/badge/🤗%20dataset-sthanika--ai%2FBharat--Knowledge--Probe--Benchmark-yellow.svg)](https://huggingface.co/datasets/sthanika-ai/Bharat-Knowledge-Probe-Benchmark)

Exact run configuration and the full leaderboard for every model evaluated on
[BKP-500 (Bharat Knowledge Probe)](https://github.com/sthanika-ai/Bharat-Knowledge-Probe-Benchmark) —
a benchmark measuring whether language models know India-specific locale conventions (Indian
numeral magnitudes, state-specific land units, traditional mass units, the Indian fiscal year,
agricultural crop seasons, government schemes, and structural identifiers), as distinct from
general arithmetic competence, via matched internationally-framed control-twin items.

This repo is the configuration companion to the benchmark itself — it documents *how* each of the
21 models on the leaderboard was actually run (backend, HF revision pin, decoding settings) so any
number below can be independently reproduced. Raw per-model responses aren't hosted here; rerun a
model against its config below to regenerate them.

**21 models evaluated · 1,086 items each (552 core + 534 control) · 2 prompt regimes × 3 samples
= 6,504 rows/model**

## What's here

```
configs/
  run_eval.py           the exact CLI entrypoint that produced every score below — includes the
                         per-model engineering notes (batch sizing, quantization choices, backend
                         workarounds) behind each configuration decision
  model_registry.json   a clean, structured extraction of the same configuration (backend,
                         HF repo + revision pin, decoding settings) for anyone who wants the
                         data without reading Python
```

## Leaderboard

Ranked by Bharat Score (macro-mean accuracy across all 7 categories), tiered by chained
bootstrap-CI overlap. Locale Gap Δ = control-item accuracy minus India-item accuracy on matched
pairs; positive means the international framing was easier for that model, negative means the
India-specific framing was.

| tier | model | bucket | bharat score (95% CI) | locale gap Δ | oom error rate | unit discipline | refusal rate | consistency |
|---|---|---|---|---|---|---|---|---|
| 1 | Qwen3.6 27B | global | 53.2% (48.9–57.3) | −14.2% | 23.0% | 69.8% | 0.7% | 100.0% |
| 1 | gpt-oss-20b | global | 46.8% (43.0–50.9) | −9.5% | 25.8% | 65.7% | 0.1% | 89.3% |
| 1 | Sarvam-M 24B | india | 45.1% (40.9–49.1) | −8.7% | 32.8% | 74.7% | 3.6% | 92.6% |
| 1 | Gemma 3 27B | global | 41.8% (38.3–45.8) | −5.9% | 27.8% | 68.6% | 0.1% | 99.6% |
| 1 | Qwen3-VL 8B | global | 39.2% (35.1–43.4) | −1.9% | 28.7% | 66.9% | 0.0% | 97.6% |
| 1 | Mistral Small 3.1 24B | global | 38.8% (35.0–42.9) | −3.6% | 26.7% | 61.0% | 0.4% | 98.2% |
| 1 | Krutrim-2 12B | india | 38.7% (34.6–43.3) | −6.0% | 32.5% | 66.4% | 0.2% | 99.6% |
| 1 | Phi-4 14B | global | 38.7% (34.8–43.0) | −4.0% | 29.2% | 68.1% | 3.7% | 99.0% |
| 1 | Sarvam 30B | india | 37.1% (33.5–40.9) | −6.4% | 40.0% | 75.4% | 2.3% | 87.6% |
| 1 | Gemma 3 12B | global | 35.1% (31.3–39.4) | −2.9% | 32.4% | 66.7% | 0.0% | 99.7% |
| 1 | Llama 3.1 8B Instruct | global | 32.5% (28.5–36.6) | −3.1% | 40.4% | 63.5% | 2.2% | 100.0% |
| 1 | Qwen2.5 7B | global | 30.9% (27.1–34.8) | +1.0% | 31.6% | 67.2% | 0.1% | 98.1% |
| 1 | Gemma 3 4B | global | 25.3% (22.1–28.8) | −2.1% | 41.3% | 60.9% | 0.1% | 100.0% |
| 1 | Navarasa 2.0 7B | india | 20.7% (17.8–23.7) | +3.5% | 46.6% | 60.0% | 0.4% | 94.0% |
| 2 | Krutrim-1 7B | india | 14.4% (11.6–17.5) | +0.9% | 55.7% | 71.1% | 0.0% | 99.9% |
| 2 | Param-1 2.9B | india | 14.3% (11.9–16.9) | +1.4% | 57.8% | 50.8% | 0.4% | 99.8% |
| 2 | Sarvam-1 2B | india | 11.6% (9.1–14.8) | −0.1% | 60.1% | 42.2% | 0.9% | 99.8% |
| 2 | OpenHathi 7B | india | 11.2% (8.7–14.2) | −0.4% | 57.8% | 58.7% | 0.1% | 96.3% |
| 2 | Airavata 7B | india | 7.9% (5.6–10.4) | +1.1% | 26.7% | 14.5% | 37.4% | 100.0% |
| 2 | Param-1 7B | india | 4.8% (3.2–6.6) | −0.3% | 33.2% | 19.4% | 31.6% | 99.5% |
| 2 | Gemma 3 12B INT4 | global | 4.6% (2.4–7.2) | +29.4% | 20.7% | 25.8% | 46.5% | 99.7% |

*OOM error rate = share of numeric answers off by ≥10× (a lakh/crore-scale slip). Unit discipline
= share of `numeric_with_unit` answers that included an explicit, correct unit. n_resamples=2,000
for every bootstrap CI above (the harness's own `scripts/build_leaderboard.py` defaults to 10,000
for a publication-grade run).*

### Per-category accuracy — all 21 models × 7 categories

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
| Krutrim-1 7B | 17.1 | 3.5 | 5.8 | 28.0 | 13.5 | 16.2 | 16.7 |
| Param-1 2.9B | 15.2 | 11.1 | 4.0 | 25.8 | 15.3 | 15.5 | 13.3 |
| Sarvam-1 2B | 16.2 | 2.8 | 2.4 | 18.5 | 12.8 | 14.9 | 13.3 |
| OpenHathi 7B | 13.1 | 4.9 | 2.2 | 15.4 | 16.7 | 8.8 | 17.8 |
| Airavata 7B | 6.9 | 4.9 | 1.4 | 12.6 | 11.8 | 4.0 | 13.3 |
| Param-1 7B | 7.4 | 0.7 | 0.0 | 6.0 | 4.1 | 5.4 | 10.0 |
| Gemma 3 12B INT4 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 12.2 | 20.0 |

*Land units by state is the single weakest category for 15 of these 21 models.*

Qwen3.6 27B leads the roster — a global open-weight model, not an India-built one. Sarvam-M 24B
is the strongest India-built/tuned model, holding rank 3 outright. **Land units by state** is the
single weakest category for 15 of the 21 models: state-by-state variation in land-unit
definitions (a *bigha* in Punjab isn't a *bigha* in Bihar) appears to be genuinely harder for
every model family tested than any other category in the corpus.

## How these numbers were produced

Every model was served locally — via [vLLM](https://github.com/vllm-project/vllm), a plain
`transformers` HF pipeline, or Ollama for one architecture vLLM doesn't yet support — never
through a paid third-party API. `configs/run_eval.py` is the exact script that drove every run;
`configs/model_registry.json` is a structured summary of the same configuration. Where a model's
upstream HF repo is gated, an ungated community mirror with identical weights was used instead
(noted per-model in the registry) — the model being evaluated is unchanged, only its hosting.

Four of the 21 models pin an explicit HF revision (commit SHA) rather than tracking a mutable
branch: every model that runs with `trust_remote_code=True` executes code from that repo directly,
so an unpinned reference would silently re-execute whatever the maintainer pushes next. The pinned
commit is exactly what "main" already resolved to at the time each model was first downloaded.

Every response is graded deterministically by the eval harness's own code — no LLM judge is
involved in scoring. See the harness repo's grader implementations for the exact per-answer-type
logic.

## Reproducing this

This repo holds configuration and the scored leaderboard, not raw run data — you need three
things side by side to regenerate a model's numbers: the harness (code), the corpus (data), and
this repo's run configuration.

### 1. Get the eval harness

```bash
git clone https://github.com/sthanika-ai/Bharat-Knowledge-Probe-Benchmark.git
cd Bharat-Knowledge-Probe-Benchmark
pip install -e ".[dev]"
```

Requires Python ≥3.10. Add the `hf-datasets` extra if you'll load the corpus straight from the
Hub in step 2 rather than a local checkout:

```bash
pip install -e ".[hf-datasets]"
```

### 2. Get the BKP-500 corpus from Hugging Face

Either clone it into `data/` inside the harness checkout (matches the on-disk layout
`load_corpus()` expects by default):

```bash
git clone https://huggingface.co/datasets/sthanika-ai/Bharat-Knowledge-Probe-Benchmark data
```

...or load it straight from the Hub in Python, no local checkout needed:

```python
from bkp_eval.items import load_corpus_from_hf

corpus = load_corpus_from_hf()   # sthanika-ai/Bharat-Knowledge-Probe-Benchmark, every category + controls
```

### 3. Drop this repo's run config into the harness checkout

`configs/run_eval.py` here is the exact script that produced every row of the leaderboard above —
it imports `bkp_eval` directly, so it needs to sit inside the harness checkout's own `scripts/`
directory (overwriting the harness's own copy of the same file is fine — this one already has
every model, port, and config value baked in):

```bash
cp /path/to/BKP-500-model-runs/configs/run_eval.py scripts/run_eval.py
```

`configs/model_registry.json` is the same configuration in plain data form (backend, HF repo,
revision pin, decoding settings) — read it if you just want to know what ran without opening
Python, or to drive your own tooling instead of `run_eval.py` directly.

### 4. Run a model

```bash
# self-hosted backends (vllm / hf / ollama) - no API key needed, matches every model in this repo
python scripts/run_eval.py --model qwen3.6-27b --mode smoke   # small sanity run first
python scripts/run_eval.py --model qwen3.6-27b --mode full    # every item + control, 3 samples, R1+R2
```

`--model` must be a key in `MODELS` inside `run_eval.py` (same set as `configs/model_registry.json`).
For a `vllm`-backend entry, start that model's `vllm serve ...` command first (the exact command —
repo id, port, quantization flags — is in the registry's `hf_repo`/`vllm_*` fields for that model);
for `hf`-backend entries, `run_eval.py` loads the model in-process via `transformers`, no server
needed. Output lands in `results/<model>/{smoke,full}.jsonl` plus a matching `*_report.txt` scored
by the harness's own grader — score it directly with `python -m bkp_eval.score results/<model>/full.jsonl`.

## Status of the underlying corpus

Every item in BKP-500 has been through a single-reviewer human QA pass (100% coverage) — not the
stricter ≥2-independent-annotator adjudication gate the benchmark's own execution plan specifies
for formal dev/test-split eligibility, which hasn't run yet. Treat every figure in this repo as
reviewed, not yet fully adjudicated.

## License

Apache-2.0 (see [`LICENSE`](LICENSE)) — matching the eval harness. The benchmark dataset itself is
licensed separately; see [its repository](https://huggingface.co/datasets/sthanika-ai/Bharat-Knowledge-Probe-Benchmark)
for terms.

## Related repositories

- [**Bharat-Knowledge-Probe-Benchmark**](https://github.com/sthanika-ai/Bharat-Knowledge-Probe-Benchmark) — the evaluation harness (adapters, graders, scoring, statistics)
- [**BKP-500 dataset**](https://huggingface.co/datasets/sthanika-ai/Bharat-Knowledge-Probe-Benchmark) — the corpus itself, on Hugging Face
