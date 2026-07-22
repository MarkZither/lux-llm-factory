import argparse
import inspect
import os
import random
from pathlib import Path

import numpy as np
import torch
import yaml
from datasets import load_dataset
from peft import LoraConfig
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, set_seed
from trl import SFTTrainer


def _read_config(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _set_determinism(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    set_seed(seed)


def _ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def resolve_hf_token() -> str | None:
    for key in ("HF_TOKEN", "HUGGINGFACE_HUB_TOKEN"):
        value = os.environ.get(key)
        if value:
            return value
    return None


def build_sft_trainer_kwargs(
    *,
    model: object,
    args: object,
    train_dataset: object,
    eval_dataset: object | None,
    tokenizer: object,
    dataset_text_field: str,
    max_seq_length: int,
    peft_config: object | None,
) -> dict:
    kwargs = {
        "model": model,
        "args": args,
        "train_dataset": train_dataset,
        "eval_dataset": eval_dataset,
        "peft_config": peft_config,
    }

    signature = inspect.signature(SFTTrainer.__init__)
    if "processing_class" in signature.parameters:
        kwargs["processing_class"] = tokenizer
    else:
        kwargs["tokenizer"] = tokenizer

    if "dataset_text_field" in signature.parameters:
        kwargs["dataset_text_field"] = dataset_text_field
    else:
        kwargs["formatting_func"] = lambda sample: sample.get(dataset_text_field, "")

    if "max_seq_length" in signature.parameters:
        kwargs["max_seq_length"] = max_seq_length

    return kwargs


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a first deterministic SFT training job.")
    parser.add_argument("--config", required=True, help="Path to YAML config.")
    args = parser.parse_args()

    config = _read_config(Path(args.config))

    hf_token = resolve_hf_token()
    if hf_token:
        os.environ["HF_TOKEN"] = hf_token
        os.environ["HUGGINGFACE_HUB_TOKEN"] = hf_token
        print("Using Hugging Face token from environment.")

    seed = int(config.get("seed", 42))
    _set_determinism(seed)

    model_name = config["model"]["name"]
    configured_output_dir = config["output"]["dir"]
    output_dir = Path(os.environ.get("TRAIN_OUTPUT_DIR", configured_output_dir))
    if not output_dir.is_absolute():
        output_dir = (Path.cwd() / output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    _ensure_parent(output_dir / "checkpoint-placeholder")

    train_path = config["data"]["train_file"]
    eval_path = config["data"].get("eval_file")
    text_field = config["data"].get("text_field", "text")

    data_files = {"train": train_path}
    if eval_path:
        data_files["validation"] = eval_path

    ds = load_dataset("json", data_files=data_files)

    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    lora_cfg = config.get("lora")

    model = AutoModelForCausalLM.from_pretrained(model_name)

    peft_config = None
    if lora_cfg and bool(lora_cfg.get("enabled", False)):
        peft_config = LoraConfig(
            r=int(lora_cfg.get("r", 8)),
            lora_alpha=int(lora_cfg.get("alpha", 16)),
            lora_dropout=float(lora_cfg.get("dropout", 0.05)),
            bias="none",
            task_type="CAUSAL_LM",
            target_modules=lora_cfg.get("target_modules", ["c_attn"]),
        )

    train_args = TrainingArguments(
        output_dir=str(output_dir),
        per_device_train_batch_size=int(config["training"].get("batch_size", 1)),
        gradient_accumulation_steps=int(config["training"].get("grad_accum", 1)),
        learning_rate=float(config["training"].get("learning_rate", 2e-5)),
        max_steps=int(config["training"].get("max_steps", 20)),
        logging_steps=int(config["training"].get("logging_steps", 1)),
        save_steps=int(config["training"].get("save_steps", 20)),
        seed=seed,
        dataloader_num_workers=0,
        report_to=[],
        fp16=False,
        bf16=False,
    )

    trainer = SFTTrainer(
        **build_sft_trainer_kwargs(
            model=model,
            args=train_args,
            train_dataset=ds["train"],
            eval_dataset=ds.get("validation"),
            tokenizer=tokenizer,
            dataset_text_field=text_field,
            max_seq_length=int(config["training"].get("max_seq_length", 512)),
            peft_config=peft_config,
        )
    )

    trainer.train()
    trainer.save_model(str(output_dir / "final"))
    tokenizer.save_pretrained(str(output_dir / "final"))

    print("Training finished.")
    print(f"Model artifacts saved to: {output_dir / 'final'}")


if __name__ == "__main__":
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
    main()
