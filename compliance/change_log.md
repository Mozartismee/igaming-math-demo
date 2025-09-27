# Change Log — Paytable Tuning (KL-Bounded)

- **Run ID:** (e.g., run_20250927_1130)
- **Date:** YYYY-MM-DD
- **Owner:** <name>
- **Config hash:** <sha256 of config yaml>
- **Seed:** <int>

## Guardrails
- RTP band: [L, U]
- Hit band: [L, U]
- Trust region (max KL per step): <value>

## Baseline KPIs
- RTP: <value>
- Hit: <value>
- Variance: <value>

## Final KPIs
- RTP: <Analytic / MC (95% CI)>
- Hit: <Analytic / MC (95% CI)>
- Variance: <Analytic / MC (95% CI)>

## Diffs
- ΔRTP: <value> (in band? Y/N)
- ΔHit: <value> (in band? Y/N)
- ΔVar: <value> (↑ expected)

## Rollout Policy
- Shadow: <scope / duration>
- Canary: <scope / abort thresholds>
- Full: <criteria>

## Revert Plan
- Revert-to: <Run ID / commit>
- Trigger: <metric / incident>
