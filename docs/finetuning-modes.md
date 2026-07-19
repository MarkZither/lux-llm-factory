# Fine-tuning modes

This project has three different training approaches that are easy to confuse. They are different in how much of the model is updated and how much memory they need.

## 1. Full fine-tuning

This updates the entire model.

- Pros: often gives the strongest adaptation
- Cons: needs much more memory and compute
- Best for: powerful GPUs and larger experiments

In plain English: you retrain the whole model, not just a small part of it.

## 2. LoRA

This updates only a small set of extra trainable parameters added to the model.

- Pros: much cheaper than full fine-tuning
- Cons: usually not as strong as full fine-tuning
- Best for: smaller hardware budgets and faster experiments

In plain English: you leave most of the model alone and teach it a small extra adapter.

## 3. QLoRA

This is LoRA with quantization, which means the model weights are stored in a lower-precision format to save memory.

- Pros: cheaper than LoRA on many GPUs and often workable on smaller hardware
- Cons: more setup complexity and some trade-offs in precision
- Best for: memory-constrained GPU workflows

In plain English: you use the LoRA idea, but also compress the model so it fits into less memory.

## Which one should you use?

- Use full fine-tuning if you have strong GPU hardware and want the most direct training path.
- Use LoRA if you want a lighter and simpler adaptation path.
- Use QLoRA if you want a memory-efficient GPU workflow.

## What this project uses by default

The default setup in this repository is intentionally simple and CPU-friendly. It is not a QLoRA-only path. QLoRA is an optional advanced path for contributors who want a more memory-efficient GPU workflow.
