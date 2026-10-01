# BKP-500 Model Runs

Exact run configuration and leaderboard for BKP-500 (Bharat Knowledge Probe), a benchmark of whether language models know India-specific locale conventions.

[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-56BF4F?style=flat-square&labelColor=1E281F)](LICENSE)
[![Hugging Face dataset](https://img.shields.io/badge/%F0%9F%A4%97%20dataset-BKP--500-FFD21E?style=flat-square&labelColor=1E281F)](https://huggingface.co/datasets/sthanika-ai/Bharat-Knowledge-Probe-Benchmark)
[![Report](https://img.shields.io/badge/report-sthanika.ai-56BF4F?style=flat-square&labelColor=1E281F&logo=firefox&logoColor=white)](https://sthanika.ai/research/bkp500-2026)

## What it measures

BKP-500 tests knowledge of Indian numeral magnitudes, state-specific land units, traditional mass units, the Indian fiscal year, agricultural crop seasons, government schemes and structural identifiers. This repo holds the configuration behind a completed campaign: 19 models, the full 552-item corpus, 2 prompt regimes and 3 samples each (3,312 scored rows per model), graded deterministically with no LLM judge. Benchmark page: [sthanika.ai/benchmarks/bkp-500](https://sthanika.ai/benchmarks/bkp-500)

## Quickstart

Every model is self-hosted, so no API keys are needed. Python 3.12 is required for the pinned vLLM wheels, and the harness itself needs 3.10 or newer. The published runs used 80 GB GPUs.

The corpus is auto-gated on Hugging Face: accept its terms on the dataset page, then log in once.

```bash
git clone https://github.com/sthanika-ai/BKP-500-model-runs.git
cd BKP-500-model-runs
python3.12 -m venv ../.venv-vllm
source ../.venv-vllm/bin/activate
pip install huggingface_hub
huggingface-cli login

# Clones the harness from GitHub, downloads the corpus from Hugging Face into the layout the
# harness expects, and installs run_eval.py plus the vLLM helpers into the harness checkout
scripts/setup_harness.sh ../Bharat-Knowledge-Probe-Benchmark
cd ../Bharat-Knowledge-Probe-Benchmark

# Harness plus inference backends (vllm / torch / transformers), all in the same venv
pip install -e ".[dev]"
pip install -r ../BKP-500-model-runs/requirements.txt

# Smoke test, then a full run (3 samples, both regimes)
python scripts/run_eval.py --model qwen3.6-27b --mode smoke
python scripts/run_eval.py --model qwen3.6-27b --mode full

# Score the run
python -m bkp_eval.score results/qwen3.6-27b/full.jsonl
```

Notes:

- `--model` must be a key in `MODELS` inside `run_eval.py` (the same set as `configs/model_registry.json` and `configs/models/*.yaml`).
- For vLLM models, start that model's `vllm serve ...` command first. The exact command is under `vllm_launch` in `configs/models/<model_id>.yaml`. `run_eval.py` only calls an already-running server. HF-backend models load in-process.
- `sarvam-m` and `sarvam-30b` need `python scripts/vllm_infra/hotpatch_vllm.py` run against `.venv-vllm` before `vllm serve` will start.
- Gated model checkpoints need the same `huggingface-cli login`, or `export HF_TOKEN=...`.
- Run `pytest` in the harness checkout first to confirm the install is sound.
- `gpu_memory_utilization` in the YAML configs is a fraction of total VRAM, so expect a different budget (and possible OOM) on smaller GPUs.
- Config schema and known reproducibility gaps: [`configs/README.md`](configs/README.md).

## Results

Full report: [sthanika.ai/research/bkp500-2026](https://sthanika.ai/research/bkp500-2026) · Model runs: [`configs/`](configs/) in this repo. Ranked by Bharat Score (macro-mean accuracy across all 7 categories), tiered by chained bootstrap-CI overlap.

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

OOM error rate is the share of numeric answers off by 10× or more (a lakh/crore-scale slip). Unit discipline is the share of `numeric_with_unit` answers that included an explicit, correct unit. CIs use n_resamples=2,000 (the harness default for a publication-grade run is 10,000).

Per-category accuracy (%), all 19 models × 7 categories:

| model | numerals | weights/vol | land units | seasons | fiscal yr | schemes | identifiers |
|---|---|---|---|---|---|---|---|
| Qwen3.6 27B | 77.9 | 61.1 | 39.4 | 48.9 | 52.9 | 41.9 | 50.0 |
| gpt-oss-20b | 78.7 | 57.6 | 34.9 | 41.2 | 46.9 | 25.4 | 43.3 |
| Sarvam-M 24B | 46.6 | 55.8 | 21.5 | 54.6 | 49.0 | 36.5 | 52.2 |
| Gemma 3 27B | 54.0 | 54.9 | 26.4 | 38.5 | 50.6 | 36.0 | 32.2 |
| Qwen3-VL 8B | 55.4 | 39.4 | 31.2 | 42.1 | 39.8 | 29.7 | 36.7 |
| Mistral Small 3.1 24B | 50.6 | 59.0 | 26.1 | 42.9 | 32.2 | 31.1 | 30.0 |
| Krutrim-2 12B | 49.2 | 39.6 | 24.5 | 44.7 | 42.9 | 39.9 | 30.0 |
| Phi-4 14B | 46.1 | 53.5 | 24.2 | 42.1 | 46.1 | 32.2 | 26.7 |
| Sarvam 30B | 40.7 | 51.2 | 28.8 | 51.1 | 33.1 | 27.9 | 26.7 |
| Gemma 3 12B | 48.8 | 40.7 | 20.8 | 41.9 | 37.8 | 29.0 | 26.7 |
| Llama 3.1 8B Instruct | 32.0 | 25.7 | 17.3 | 39.6 | 38.2 | 35.1 | 40.0 |
| Qwen2.5 7B | 44.6 | 37.7 | 17.5 | 32.4 | 34.5 | 16.0 | 33.3 |
| Gemma 3 4B | 32.9 | 24.3 | 12.5 | 34.6 | 31.2 | 18.2 | 23.3 |
| Navarasa 2.0 7B | 26.1 | 21.5 | 10.3 | 25.1 | 30.4 | 17.6 | 13.3 |
| Param-1 2.9B | 15.2 | 11.1 | 3.5 | 25.8 | 15.3 | 15.5 | 13.3 |
| Sarvam-1 2B | 16.2 | 2.8 | 2.4 | 18.5 | 12.8 | 14.9 | 13.3 |
| OpenHathi 7B | 13.1 | 4.9 | 2.2 | 15.4 | 16.7 | 8.8 | 17.8 |
| Airavata 7B | 6.9 | 4.9 | 1.4 | 12.6 | 11.8 | 4.0 | 13.3 |
| Gemma 3 12B INT4 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 12.2 | 20.0 |

Qwen3.6 27B, a global open-weight model, leads the roster. Sarvam-M 24B is the strongest India-built model at rank 3. Land units by state is the weakest category for 14 of the 19 models.

Full report and data: `reports/bkp500_report.html`, `reports/report_data.json`, `reports/model_results.csv` (regenerated by the pipeline above) · Report page: [sthanika.ai](https://sthanika.ai/research/bkp500-2026) · Model runs: this repo.

## Citation

Cite this leaderboard and these configurations as in [`CITATION.cff`](CITATION.cff). To cite the benchmark itself, cite the harness repository.

```bibtex
@misc{bkp500_model_runs2026,
  title  = {BKP-500 Model Runs},
  author = {{sthanika-ai}},
  year   = {2026},
  url    = {https://github.com/sthanika-ai/BKP-500-model-runs}
}
```

## License

Apache-2.0, see [LICENSE](LICENSE); the benchmark dataset is licensed separately.

## Related

- [BKP-500 dataset](https://huggingface.co/datasets/sthanika-ai/Bharat-Knowledge-Probe-Benchmark): the corpus, on Hugging Face
- [Bharat-Knowledge-Probe-Benchmark](https://github.com/sthanika-ai/Bharat-Knowledge-Probe-Benchmark): the evaluation harness (adapters, graders, scoring, statistics)
- [`configs/README.md`](configs/README.md): config schema, naming conventions and known reproducibility gaps
- Site: [sthanika.ai](https://sthanika.ai)
