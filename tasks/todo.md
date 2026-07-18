# Working Plan

## Phase 0 — Repo initialization (this PR)
- [x] Research current law: OBBBA made 100% bonus depreciation permanent (placed in
      service after Jan 19, 2025); confirmed STR-loophole mechanics.
- [x] Research STR regulations in all three target markets (July 2026 snapshot).
- [x] `docs/strategy.md` — how the strategy works, requirements, pitfalls, CA
      non-conformity.
- [x] `docs/regulations.md` — jurisdiction-by-jurisdiction legality + strategy fit.
- [x] `analysis/deal_analyzer.py` — after-tax break-even model with compliance flags.
- [x] Example scenarios: Encinitas, Carlsbad, Carpinteria (pass), Solana Beach
      (intentional fail: 7-night minimum).
- [x] `QUESTIONS.md` — open questions for the owners.

## Phase 1 — Calibrate (blocked on answers to QUESTIONS.md)
- [ ] Set real tax profile (marginal rates, income level vs §461(l) cap).
- [ ] Set real budget/financing terms (quote from lender).
- [ ] Decide market scope (likely: drop Monterey for STR purposes).
- [ ] Replace placeholder ADR/occupancy with AirDNA/Rabbu comps per zip.
- [ ] Get insurance quotes for representative coastal properties.

## Phase 2 — Property pipeline
- [ ] Build a candidate-property intake process (one TOML per listing).
- [ ] Per-property diligence checklist automation (zone lookup, permit availability,
      HOA CC&Rs) — see checklist at bottom of docs/regulations.md.
- [ ] Sensitivity analysis (ADR ±15%, occupancy ±10pts, rate ±1%).

## Phase 3 — Decision
- [ ] Shortlist 2–3 properties, run full model + CPA review.
- [ ] Verify placed-in-service timing vs target tax year.

## Review — Phase 0
Repo initialized with strategy docs, regulation research, a working break-even model,
and four example scenarios. Key findings baked into the docs:

1. **The law is favorable**: 100% bonus depreciation is permanent (OBBBA). The strategy
   works mechanically.
2. **Regulations are the binding constraint**: Monterey Peninsula is effectively closed;
   Del Mar is closed; Solana Beach's 7-night minimum breaks the 7-day test. Best fits:
   Encinitas, Carlsbad Coastal Zone, SD Tier 3 coastal, Carpinteria beach zone.
3. **The math works in Year 1 but not Year 2+** at placeholder assumptions: example
   deals show +$30–57k after-tax in Year 1 (thanks to ~$125k tax savings) but
   ‑$20–35k/yr after-tax stabilized. The stated goal ("break even after tax savings")
   is met in Year 1 only — owners should decide if that's the intended bar.
4. **§461(l) cap binds at these price points** (~$317k MFJ) — a cheaper property
   captures nearly the same Year-1 tax savings; price ceiling is a real optimization
   variable, not just a budget constraint.
5. **CA doesn't conform to bonus depreciation** — only the federal side gets the big
   Year-1 savings.

## Lessons
(none yet)
