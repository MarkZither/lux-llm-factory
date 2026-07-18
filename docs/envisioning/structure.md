# Structure (Cache)

> Source of truth: Board. Check board for current state.
> Platform configured in: .memory/board-config.md

| ID | Type | Name | Parent | Priority |
|----|------|------|--------|----------|
| #1 | Epic | Luxembourgish LLM Factory MVP | - | - |
| #2 | Feature | Deterministic Python and Environment Foundation | #1 | P1 |
| #3 | Feature | Luxembourgish Dataset Ingestion and Normalization | #1 | P1 |
| #4 | Feature | First Finetuning Tracer Bullet | #1 | P1 |
| #5 | Feature | Luxembourgish Evaluation Baseline for CEFR A1 and A2 | #1 | P1 |
| #6 | Feature | Dual Export Pipeline ONNX and GGUF | #1 | P2 |
| #7 | Feature | Scale-up Training Tracks for Gemma and QLoRA Toolchains | #1 | P3 |

## Dependencies

- #3 depends on #2
- #4 depends on #2 and #3
- #5 depends on #3 and #4
- #6 depends on #4
- #7 depends on #4, #5, and #6
