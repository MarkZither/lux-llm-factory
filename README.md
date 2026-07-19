# Lux LLM Factory

## Overview
This repository contains a reproducible finetuning and evaluation pipeline for
Luxembourgish language models targeting the LIST leaderboard. The goal is to
produce strong locally-hostable models first, then scale to larger variants.

The project emphasizes:
- Deterministic, reproducible training
- Clean separation of data, training, evaluation, and packaging
- ONNX export for personal inference environments
- GGUF export for broad community adoption (Ollama, llama.cpp, LM Studio)
- Automated Luxembourgish-specific evaluation

## Current Scope
- First milestone: beginner-safe first finetune run on a standard CPU laptop
- Initial focus: Luxembourgish n-rule examples, then inversion rule (V2 word order)
- Model path: start with tiny smoke model, then Gemma 2B and Gemma 4B
- Future path: QLoRA, Axolotl, Unsloth, and MoE experiments once hardware and runtime are ready

## First Run Quickstart

### Canonical setup flow

Use the deterministic setup flow documented in [docs/features/deterministic-python-foundation/setup.md](docs/features/deterministic-python-foundation/setup.md) and the canonical command reference in [docs/features/deterministic-python-foundation/commands.md](docs/features/deterministic-python-foundation/commands.md) as the single supported onboarding path.

```powershell
uv python install 3.14
uv venv --python 3.14
uv sync
uv run python scripts/envctl.py setup --profile local-cpu
uv run python scripts/envctl.py validate --profile local-cpu
uv run python scripts/envctl.py run --profile local-cpu
```

### 1) Install uv and create environment

On Windows PowerShell:

```powershell
irm https://astral.sh/uv/install.ps1 | iex
uv python install 3.14
uv venv --python 3.14
uv sync
```

### 2) Verify your training data format

Your file should be JSONL with one object per line and a text field:

```json
{"category":"n_rule","instruction":"Mark N-rule candidates.","input":"Ech hunn en Apel.","output":{"corrected":"Ech hunn en Apel.","n_rule":{"candidates":["en"],"lemma":"een","applies":true,"reason":"Before vowel-initial noun."}}}
{"category":"n_rule","instruction":"Mark N-rule candidates.","input":"Ech gesinn de Mann.","output":{"corrected":"Ech gesinn de Mann.","n_rule":{"candidates":["de"],"lemma":"den","applies":false,"reason":"Consonant-initial noun."}}}
```

Starter files are already present in this repository:
- data/processed/nrule_train.jsonl
- data/processed/nrule_eval.jsonl

### 3) Run the first CPU training

```powershell
uv run python scripts/train_first_sft.py --config training/configs/first-run-cpu.yaml
```

Expected output artifacts:
- models/first-run-cpu/final

### 4) Replace starter data with your own n-rule dataset

Update these files with your real examples while preserving JSONL format:
- data/processed/nrule_train.jsonl
- data/processed/nrule_eval.jsonl

### 5) Move from smoke test to Gemma

Edit training/configs/first-run-cpu.yaml and replace model.name with your target model.

Important practical note:
- CPU-only Gemma finetuning is useful for tiny sanity checks but can be very slow.
- QLoRA usually requires Linux and CUDA for practical speed.
- On Windows, use WSL2 with NVIDIA CUDA when you are ready for QLoRA toolchains.

## Tooling Strategy

This repository uses uv and pyproject.toml for explicit dependency management.

Default install includes:
- PyTorch
- Transformers
- TRL SFTTrainer
- PEFT
- Datasets
- Accelerate

Optional dependency groups are defined for:
- qlora (bitsandbytes)
- axolotl
- unsloth

Examples:

```powershell
uv sync --group qlora
uv sync --group axolotl
uv sync --group unsloth
```

Some optional groups are intentionally restricted to non-Windows environments.

## Features
- Data ingestion and preprocessing (supports large corpora such as BnL newspapers)
- Plain-English guide to full fine-tuning, LoRA, and QLoRA in [docs/finetuning-modes.md](docs/finetuning-modes.md)
- Tokenization and vocabulary extension options
- LoRA and full finetuning pipelines
- Training configs for multiple model sizes
- Evaluation suite tailored to Luxembourgish morphology, syntax, and NER
- Export pipeline:
  - ONNX (for custom runtimes)
  - GGUF (for community tools)
- Model card generator
- Makefile targets for reproducible workflows

## Directory Structure
data/
raw/
processed/
scripts/

training/
configs/
lora/
full/
logs/
wandb/

evaluation/
lux-tests/
perplexity/
leaderboard-format/

export/
onnx/
gguf/

models/
checkpoints/
final/
model-card.md

docs/
dataset-prep.md
training-notes.md
evaluation-methodology.md

## Roadmap
- [ ] Gemma 2B baseline finetune
- [ ] Gemma 4B baseline finetune
- [ ] V2 inversion rule training set and eval set
- [ ] Luxembourgish grammar evaluation suite
- [ ] ONNX runtime optimizations
- [ ] GGUF quantization presets
- [ ] MoE expert specialization experiments
- [ ] LIST leaderboard submission automation