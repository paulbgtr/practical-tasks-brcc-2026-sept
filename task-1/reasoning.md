# Reasoning and Assessment

## Theoretical background

aFRR (automatic Frequency Restoration Reserve) is an automatically activated reserve that responds to system imbalances within minutes, correcting the gap between scheduled and actual generation/consumption before it affects frequency stability for too long. It sits between the very fast FCR (seconds-level, no operator/automatic dispatch decision) and the slower manual mFRR/RR reserves. Because it's automatic, its activation should track the sign and rough magnitude of the imbalance closely and with minimal delay.

## Metrics used

- `coverage_pct`: total aFRR activation (`|net_afrr|`) as a % of the imbalance that would have occurred without balancing (`|value|`).
- `direction_accuracy`: % of intervals where aFRR activation direction (Downward for surplus, Upward for deficit) matched the imbalance sign.
- `no_reaction_pct`: % of imbalanced intervals with zero aFRR activation.
- `avg_residual_ratio`: average of `|residual|/|value|`, showing typical leftover imbalance as a fraction of the counterfactual imbalance, per-interval rather than aggregated.

**Important**: `imbalance_volumes_v2` is explicitly defined as the counterfactual area control error "as it would have been if power balancing was not performed", not the actual residual imbalance after TSOs acted. So `coverage_pct` here doesn't mean "% of the real imbalance that was fixed", it means "how large aFRR activation was relative to the imbalance that would have existed with no balancing at all."
A low `coverage_pct` doesn't necessarily mean poor performance, it can also mean other reserves (FCR, mFRR, cross-border exchange) absorbed part of that counterfactual imbalance instead of aFRR alone.

## Findings (22.09.2025)

| Area      | Total Imbalance | Total Activation | Coverage | Direction accuracy | No-reaction | Avg residual ratio | Median residual ratio |
| --------- | --------------- | ---------------- | -------- | ------------------ | ----------- | ------------------ | --------------------- |
| Estonia   | 1766.07         | 267.39           | 15.1%    | 55.2%              | 0.0%        | 1.59               | 0.97                  |
| Latvia    | 594.96          | 320.78           | 53.9%    | 80.2%              | 0.0%        | 2.38               | 0.96                  |
| Lithuania | 1614.80         | 241.89           | 15.0%    | 56.2%              | 3.1%        | 1.60               | 1.00                  |

## Assessment

Latvia's total counterfactual imbalance (594.96) is roughly a third of Estonia's and Lithuania's (~1700 each) - the Latvian system needed far less correcting on this day to begin with. This matters for interpreting the rest of Latvia's numbers: its higher `coverage_pct` (53.9% vs ~15%) is computed against a much smaller base, so a comparable absolute activation volume naturally produces a larger percentage.

### Direction accuracy

Latvia's 80.2% is meaningfully higher than Estonia's and Lithuania's ~55-56%. Even accounting for the smaller-imbalance caveat, this gap suggests Latvia's aFRR activations were more consistently aligned with the direction of the (counterfactual) imbalance on this day. That said, since value is a "no balancing" counterfactual and not the actual post-balancing residual, a mismatch in sign doesn't necessarily mean aFRR reacted incorrectly - the real system imbalance can differ in sign from what value reports, so ~55% direction accuracy for Estonia/Lithuania should be read as "not clearly interpretable as pure over/under-correction" rather than as a definitive fault.

### Residual ratio

The `avg_residual_ratio` exceeding 1 in all three areas (1.59–2.38) reflects the same structural point: the gap between counterfactual imbalance and aFRR activation is, per interval, typically larger than the imbalance itself - expected given aFRR is only one of several balancing mechanisms and isn't meant to close 100% of a "no balancing" counterfactual alone. Latvia's higher ratio (2.38) despite its higher coverage and direction accuracy is a bit counterintuitive and likely reflects a few intervals with small value and comparatively large net_afrr, which inflate the ratio disproportionately, worth flagging rather than treating as a contradiction.

This divergence between the mean (1.59–2.38) and median (0.96–1.00) is itself informative: the median close to 1.0 across all three areas shows that in the *typical* interval, net aFRR activation is close to zero relative to the imbalance. The mean is pulled well above the median by a minority of intervals with small `value` and oppositely-signed `net_afrr`, which inflate the ratio disproportionately (a known weakness of ratio-based metrics with a small denominator). The two statistics answer different questions: the median describes typical/baseline behavior, while the mean captures the tail of mismatched-direction intervals - arguably the more relevant signal for judging reliability, since those are the moments activation actively works against the imbalance rather than simply being absent.

### No reaction

Lithuania's 3.1% no-reaction rate (non-zero imbalance, zero aFRR activation) is small but the only non-zero occurrence among the three areas - worth noting but not significant on a single day.

### Visual confirmations from the plots

The residual plots support the numbers above. For Estonia and Lithuania, the largest residual spikes coincide almost exactly with the largest imbalance excursions - e.g. Lithuania's imbalance drops to roughly -60 around 09:00, and residual tracks it nearly one-to-one at the same moment, implying close to zero effective aFRR response exactly when the imbalance was most extreme. The same pattern appears in Estonia around 12:00 and 18:00. This suggests the shortfall in both areas isn't spread evenly across the day but concentrated at the moments that matter most.

Latvia's `net_afrr` visibly tracks the shape of its imbalance curve more closely throughout the day, consistent with its higher `direction_accuracy` - the two curves move together rather than one being flat while the other swings. It still shows one sharp residual spike (~06:00), which is the likely driver of its higher mean residual ratio despite the otherwise closer tracking.

![graph](https://github.com/paulbgtr/practical-tasks-brcc-2026-sept/blob/main/task-1/aFRR_vs_imbalance_20250922.png?raw=true)

## Limitations

This is a single-day snapshot (22.09.2025), the imbalance metric is a counterfactual rather than the actual post-balancing residual, and Latvia's much smaller imbalance base makes its volume-based metrics (coverage_pct, avg_residual_ratio) less directly comparable to Estonia's and Lithuania's. A more robust assessment would use several days of data and, ideally, the actual net regulation state rather than the counterfactual imbalance series.
