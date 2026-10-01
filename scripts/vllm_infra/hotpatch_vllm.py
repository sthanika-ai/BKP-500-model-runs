#!/usr/bin/env python3
from __future__ import annotations

import sys
import subprocess
from pathlib import Path
from urllib.request import urlopen, Request


HF_BLOB_URL = "https://huggingface.co/sarvamai/sarvam-30b/blob/main/sarvam.py"

NEW_LINES = [
    '    "SarvamMoEForCausalLM": ("sarvam", "SarvamMoEForCausalLM"),\n',
    '    "SarvamMLAForCausalLM": ("sarvam", "SarvamMLAForCausalLM"),\n',
]


def run(cmd: list[str]) -> None:
    print(f"+ {' '.join(cmd)}")
    subprocess.check_call(cmd)


def pip_install_vllm() -> None:
    run([sys.executable, "-m", "pip", "install", "vllm==0.15.0"])


def find_vllm_dir() -> Path:
    import vllm  # type: ignore

    vllm_dir = Path(vllm.__file__).resolve().parent
    print(f"Detected vLLM package dir: {vllm_dir}")
    return vllm_dir


def patch_text_generation_models(registry_path: Path) -> None:
    if not registry_path.exists():
        raise FileNotFoundError(f"registry.py not found at: {registry_path}")

    text = registry_path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)

    # Idempotency: if both keys already present, do nothing
    if (
        any('"SarvamMoEForCausalLM"' in l for l in lines)
        and any('"SarvamMLAForCausalLM"' in l for l in lines)
    ):
        print("registry.py already contains Sarvam entries. Skipping patch.")
        return

    # Find the start of the _TEXT_GENERATION_MODELS dict
    start_idx = None
    for i, line in enumerate(lines):
        if line.strip() == "_TEXT_GENERATION_MODELS = {":
            start_idx = i
            break

    if start_idx is None:
        raise RuntimeError(
            "Could not find '_TEXT_GENERATION_MODELS = {' in registry.py. "
            "vLLM version/layout may differ."
        )

    # Find the matching closing brace for that dict using brace depth
    depth = 0
    end_idx = None
    for j in range(start_idx, len(lines)):
        depth += lines[j].count("{")
        depth -= lines[j].count("}")
        if j > start_idx and depth == 0:
            end_idx = j
            break

    if end_idx is None:
        raise RuntimeError("Failed to find end of _TEXT_GENERATION_MODELS dict (brace matching).")

    # Insert new entries just before the closing brace line
    insert_at = end_idx
    lines[insert_at:insert_at] = NEW_LINES

    registry_path.write_text("".join(lines), encoding="utf-8")
    print(f"Patched _TEXT_GENERATION_MODELS in: {registry_path}")


def download_sarvam_py(dst: Path) -> None:
    # Use /raw/ to download file contents, not HTML
    raw_url = HF_BLOB_URL.replace("/blob/", "/raw/")
    print(f"Downloading sarvam.py from: {raw_url}")

    req = Request(raw_url, headers={"User-Agent": "vllm-hotpatch-script"})
    with urlopen(req) as resp:
        data = resp.read()

    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(data)
    print(f"Wrote: {dst}")


def main() -> None:
    pip_install_vllm()

    vllm_dir = find_vllm_dir()
    registry_path = vllm_dir / "model_executor" / "models" / "registry.py"
    sarvam_path = vllm_dir / "model_executor" / "models" / "sarvam.py"

    patch_text_generation_models(registry_path)
    download_sarvam_py(sarvam_path)

    print("\nDone.")
    print(f"- Registry patched: {registry_path}")
    print(f"- Sarvam module installed: {sarvam_path}")


if __name__ == "__main__":
    main()