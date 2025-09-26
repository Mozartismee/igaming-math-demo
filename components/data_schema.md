# Data Schema Component (`spins_log`)

## Table: `spins_log`
Columns (minimal for demo):
- `ts` (timestamp, UTC or with tz)
- `game_id` (string)
- `session_id_hash` (string/hashed)
- `bet_amount` (float; here = 1)
- `outcome_id` (int in \([0,k]\) matching the index of \(r\))
- `payout` (float in \(\{r_i\}\))
- `jurisdiction_id` (string or enum)

## Aggregates
Daily or batch aggregates may include: mean RTP, variance, hit-rate, counts per outcome, and jurisdiction splits.

## Data quality checks
- Range checks: payouts in \(\{r_i\}\), probs sum to 1 (model side).
- Missingness: no nulls in key columns; define policy for drops/backfills.
- Time sanity: non-decreasing timestamps per session; optional dedup by `(ts, session_id_hash)`.
- Leakage: ensure training splits do not leak future days.

## Inputs / Outputs / Tests
- **Inputs:** generated or real logs.
- **Outputs:** clean aggregates; flags for anomalies.
- **Tests:** schema validation; histogram of `outcome_id` matches \(p\) within tolerance for sample size.
