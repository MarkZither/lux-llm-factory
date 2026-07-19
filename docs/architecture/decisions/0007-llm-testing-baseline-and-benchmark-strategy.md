# LLM Testing Baseline and Benchmark Strategy

**Status**: Proposed
**Date**: 2026-07-19

## Context

The project needs a repeatable testing baseline before fine tuning so model quality changes can be measured credibly after training iterations. The official Luxembourgish evaluation approach defines 630 multiple choice questions across Vocabulary, Grammar, Reading Comprehension, and Listening Comprehension, each mapped to CEFR levels A1 through C2, with scores reported as percentage correct by category and level. The current external suite focus includes LangBiTe for bias testing, with planned addition of langtest and selected Beyond Imitation Game tests.

Without an explicit testing strategy decision, baseline creation and post fine tuning comparison could drift across runs, reducing confidence in quality claims and making regressions difficult to detect.

## Priorities and Requirements (ordered)

1. **Before versus after comparability**: Baseline and post fine tuning evaluations must use a stable, versioned core protocol so deltas are attributable to model changes.
2. **Luxembourgish relevance and diagnostic depth**: The core baseline must reflect Luxembourgish language capability and expose breakdowns by CEFR level and linguistic category.
3. **Operational repeatability**: Test execution must be automatable and practical for routine iteration in this repository.
4. **Extensible benchmark coverage**: The strategy must support bias, robustness, and broader capability checks without destabilizing the core baseline.

## Options Considered

### Option 1: Official exam baseline as mandatory core plus phased external benchmark suites

Use the official 630 question CEFR and category methodology as the mandatory baseline gate. Keep LangBiTe in the active suite, then add langtest and selected Beyond Imitation Game tests in a controlled second phase while preserving the official baseline as the primary comparison axis.

**Evaluation against priorities**:
- **Before versus after comparability**: Meets. One mandatory core protocol creates stable run to run comparison and clear post fine tuning deltas.
- **Luxembourgish relevance and diagnostic depth**: Meets. CEFR and category slices provide targeted diagnostics aligned to project goals.
- **Operational repeatability**: Meets. Multiple choice scoring and percentage reporting are deterministic and easy to automate.
- **Extensible benchmark coverage**: Meets. Additional suites can be added as secondary tracks without changing the core baseline identity.

### Option 2: External benchmark suites only without official exam baseline

Use LangBiTe now and future langtest and Beyond Imitation Game subsets as the only testing surface.

**Evaluation against priorities**:
- **Before versus after comparability**: Partially meets. Comparability exists inside each suite but lacks one domain specific canonical baseline.
- **Luxembourgish relevance and diagnostic depth**: Partially meets. Coverage may be broad but does not guarantee CEFR and category alignment for Luxembourgish learning focus.
- **Operational repeatability**: Partially meets. Tooling exists but subset selection and configuration drift can reduce stable comparisons.
- **Extensible benchmark coverage**: Meets. This option is broad by design.

### Option 3: Ad hoc manual evaluation per fine tuning cycle

Evaluate each trained model with manually selected prompts and qualitative review, without a fixed benchmark contract.

**Evaluation against priorities**:
- **Before versus after comparability**: Fails. Prompt and reviewer variation makes deltas unreliable.
- **Luxembourgish relevance and diagnostic depth**: Partially meets. Domain prompts can be relevant but usually lack consistent CEFR and category structure.
- **Operational repeatability**: Fails. Manual scoring is expensive and inconsistent.
- **Extensible benchmark coverage**: Fails. Results are difficult to aggregate across additional suites.

## Decision

Choose Option 1.

The project will adopt the official 630 question CEFR and category methodology as the canonical baseline for model quality tracking. LangBiTe remains part of the active testing suite, and langtest plus selected Beyond Imitation Game tests will be introduced as phased secondary suites. Baseline and post fine tuning comparisons must always include the canonical official baseline report, with category and CEFR breakdown percentages, so quality deltas remain stable and interpretable.

## Implementation Notes (optional)

- Record a baseline run for the current unfine tuned reference model before additional training iterations.
- Version the test manifest that defines question set identity and external suite subsets used in each run.
- Treat external suite additions as additive tracks unless a future ADR changes the canonical baseline.
- Publish result artifacts with aggregate score plus per category and per CEFR breakdown.

## References

* [Official Luxembourgish exam methodology](https://llmluxapp-a7tpfn2c5tgk8pqzecquvh.streamlit.app/~/+/#how-does-it-work)
* [LangBiTe](https://github.com/SOM-Research/LangBiTe)
* [langtest](https://langtest.org/)
* [Beyond Imitation Game](https://github.com/google/BIG-bench)
* [Envisioning: Luxembourgish LLM Factory](../../envisioning/README.md)
* [Feature Spec: Deterministic Python and Environment Foundation](../../features/deterministic-python-foundation/spec.md)