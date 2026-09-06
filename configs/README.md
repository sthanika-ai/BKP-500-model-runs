# Model configs

One YAML file per evaluated model in `configs/models/`, named `<model_id>.yaml` (same key
used in `configs/run_eval.py`'s `MODELS` dict and `configs/model_registry.json`). Each config
pins the checkpoint, serving backend, decoding settings, and concurrency knobs that produced
that model's row on the leaderboard, plus a `notes:` field carrying the real engineering
rationale (and any workaround) behind non-default settings — read it before copying a config
as a template for a new model.

This directory is a human-readable *derivative* of `configs/run_eval.py`, not a second source
of truth: `run_eval.py`'s `MODELS` dict is what the harness actually executes; these YAMLs
exist so the same information can be read, diffed, and reasoned about without running Python.
If the two ever disagree, `run_eval.py` is correct.

## Schema

- `model_id` — the run key, matches `run_eval.py`'s `MODELS` dict and `model_registry.json`.
- `rank_by_bharat_score` — this model's rank (1 = highest) on the published leaderboard, for
  browsing the directory in leaderboard order.
- `hf_checkpoint` — the exact Hugging Face repo string served, or (for `qwen3.6-27b`, the one
  Ollama-backed model) the Ollama tag — there is no HF checkpoint to pin in that case.
- `revision` — commit SHA, when pinned. **Only 2 of these 19 configs are actually
  commit-pinned** (`sarvam-m`, `param-1-2.9b`) — both `trust_remote_code=True` models pinned
  2026-08-27/28 as a security fix, since that flag executes the repo's own Python. Every other
  config tracks that repo's mutable default branch as it resolved at run time; no `access_date`
  was recorded for any model, so an unpinned config here cannot be traced back to an exact
  checkpoint state the way a pinned one can — treat that as a known gap, not an oversight.
- `serving_backend` — `hf` (in-process `transformers`, no server), `vllm` (local `vllm serve`,
  hit via `LocalAPIAdapter`), or `ollama` (Ollama's OpenAI-compatible endpoint — used only for
  `qwen3.6-27b`, whose hybrid attention+SSM+vision architecture vLLM doesn't support yet).
- `apply_chat_template` — whether the request is formatted with the model's own chat template.
  Marked `false` only where a run_eval.py comment **confirms** the repo ships no real
  chat_template (`airavata-7b`, `openhathi-7b`, `navarasa-2.0-7b` — all older/base-derived
  checkpoints); `true` elsewhere. Where no comment either way exists, `true` reflects
  `hf_adapter.py`'s own runtime auto-detection default, not a fact independently confirmed for
  that specific repo — see that model's `notes:`.
- `dtype`, `quantization` — as actually loaded: `bfloat16` for unquantized `hf`-backend models,
  `auto` for `vllm`-backend models (no `--dtype` flag was ever passed, so this is vLLM's own
  default, not an assumption), and the real quantization scheme for the 3 prequantized models
  (`airavata-7b`: bitsandbytes 8-bit; `gemma3-12b-int4`: bitsandbytes int4 QAT; `gpt-oss-20b`:
  native MXFP4, auto-detected from `config.json`).
- `batch_size` — the real client-side batch for `hf`-backend models (no continuous batching
  there — see `hf_adapter.py`'s module docstring); `auto` for `vllm`/`ollama`, where the server
  handles concurrent sequences and `max_workers` is the real concurrency lever instead.
- `max_workers` — client-side concurrent request count, calibrated per-model against server
  metrics (KV-cache %, Running/Waiting queue depth) where a `notes:` field says so.
- `vllm_launch` (vLLM-backend only) — `port`, `gpu_memory_utilization`, `max_model_len`, and any
  `extra_args` the harness expects `vllm serve` to have been started with *before* running
  `run_eval.py` (see the root README's "How these numbers were produced"). **Read
  `gpu_memory_utilization` as a fraction of that GPU's *total* VRAM, not of the model's size** —
  vLLM enforces it as a hard startup requirement independent of how large the model actually is,
  so the same value means a different real memory budget on a different GPU.
- `generation_config.temperature` — always `0.0` (the harness's `RunConfig` default; every
  model in this roster ran at temperature 0, so this is never overridden per-model).
- `generation_config.max_gen_toks` — `max_tokens` in `run_eval.py`, defaulting to 512 when not
  explicitly overridden; several models override it up (reasoning models that need headroom
  past their chain-of-thought) or down (`param-1-2.9b`, where uncached generation is
  quadratic in this value).
- `mode: full`, `regimes: [R1, R2]`, `n_samples: 3` — constant across every model in this
  roster: the full 552-item corpus, both prompt regimes, 3 samples each
  = 3,312 rows/model. Not a per-model choice, included here only so each file is
  self-describing without cross-referencing the root README.
- `notes` — condensed from that model's comment block in `run_eval.py`. Where a config setting
  reflects a confirmed, reproduced finding (a real bug, a calibration measurement), the notes
  say so explicitly; where it's a default with no specific investigation behind it, the notes
  say that too, rather than implying more confidence than the original comment had.

## Adding a new model

1. Copy the config for the model here closest to yours in backend and architecture.
2. If it needs `trust_remote_code=True`, pin an exact revision (commit SHA) before running
   anything at scale — see `param-1-2.9b.yaml`'s notes for why an unpinned "main" is a real risk
   for that flag specifically.
3. Run `python scripts/run_eval.py --model <model_id> --mode smoke` first — a small sanity run
   before committing to a multi-hour full run.
4. Record what you found in `notes:` as you go, including settings that *didn't* work and why —
   that history is what makes the next model's config faster to write correctly.
