# Measurement Protocol

- **Created on**: 2026-07-19
- **Status**: Draft
- **Related spec**: [spec.md](./spec.md)

## Objective

Provide a repeatable measurement method for success criteria SC-001 through SC-004 so the deterministic setup feature can be evaluated with evidence instead of assumptions.

## Measurement Model

| Success criterion | Measurement | Method | Expected threshold |
|-------------------|-------------|--------|--------------------|
| SC-001 | First attempt onboarding success | Run the canonical setup flow for a sample of contributors or dry runs and record whether the first attempt reaches a ready state without assistance. | At least 95 percent success on first attempt. |
| SC-002 | Dependency identity match | Repeat the same setup flow twice and compare the resulting dependency identity or lock evidence. | 100 percent of validation checks match. |
| SC-003 | Policy coverage | Count the core tools and dependency groups that are covered by explicit pin or constraint rules. | 100 percent coverage. |
| SC-004 | Time to readiness | Measure the elapsed time from the start of the documented flow to a ready state on a clean supported machine. | 20 minutes or less, excluding external download variability. |

## Data Collection Procedure

1. Prepare a validation worksheet with contributor name, platform, date, and run ID.
2. Record the start time immediately before the first canonical setup command.
3. Record the end time when the environment is reported ready by the canonical validate flow.
4. Save the outputs from setup, validate, and run commands for each run.
5. Compare repeated runs for dependency identity consistency.

## Metrics and Calculation Notes

- First attempt success rate is calculated as successful first attempt runs divided by total runs.
- Identity match is confirmed when the lock identity or dependency manifest output is unchanged across repeated runs for the same declared inputs.
- Policy coverage is confirmed when every core dependency group listed by the feature policy is assigned either a pin or an explicit constraint rule.
- Readiness time should be measured from the documented command sequence and should exclude external service interruptions that are outside the repository control.

## Evidence Pack

Each measured run should include:

- the command transcript
- the environment identity output
- the resulting lock or manifest artifact
- a short note describing any manual intervention or unexpected friction

A run is considered successful when all required evidence is captured and the threshold for the targeted metric is met.
