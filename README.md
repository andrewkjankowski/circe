# Second Home + STR Tax Strategy Analysis

This repo helps us analyze and select a second home in coastal California that:

1. Works as a **second home** we actually enjoy using,
2. Operates as a **short-term rental (STR)** when we're not there, and
3. Generates enough **tax savings** (via the STR loophole: cost segregation + 100% bonus
   depreciation + material participation) that the property **breaks even after-tax**, even
   if it doesn't fully cover its debt service on cashflow alone.

## Target markets

| Market | Areas of interest |
|---|---|
| North County San Diego | Carlsbad, Encinitas/Leucadia, Cardiff, Solana Beach, Del Mar, Torrey Pines/La Jolla edge |
| Monterey Peninsula | Carmel, Carmel Valley, Pebble Beach, Pacific Grove, Monterey |
| Santa Barbara area | Santa Barbara city, Montecito, Summerland, Carpinteria, Goleta |

**Read `docs/regulations.md` first.** STR legality varies wildly by parcel in these markets,
and several areas (Carmel-by-the-Sea, Del Mar, unincorporated Monterey County residential
zones) effectively prohibit the strategy. Regulations are the #1 screen — before price,
before ADR, before anything else.

## Repo layout

```
README.md                 <- you are here
QUESTIONS.md              <- open questions we need to answer to sharpen the analysis
docs/
  strategy.md             <- how the STR tax strategy works, requirements, and pitfalls
  regulations.md          <- STR rules by city/jurisdiction (snapshot, July 2026)
analysis/
  deal_analyzer.py        <- the break-even model (pre-tax and after-tax)
scenarios/
  *.toml                  <- one file per candidate property / market scenario
tasks/
  todo.md                 <- working plan and progress
```

## Quick start

No dependencies beyond Python 3.11+ (uses stdlib `tomllib`).

```bash
# Analyze one scenario
python3 analysis/deal_analyzer.py scenarios/encinitas_example.toml

# Analyze all scenarios and print a comparison table
python3 analysis/deal_analyzer.py scenarios/*.toml
```

The analyzer reports, for each scenario:

- Cash required to close (down payment + closing costs + furnishing)
- Year-1 and stabilized pre-tax cashflow (NOI minus debt service)
- Year-1 depreciation (bonus on cost-seg components + furnishings, straight-line on the rest)
- Federal and California tax savings (CA does **not** conform to bonus depreciation)
- **After-tax cashflow** and the break-even verdict against our stated goal
- Compliance flags: 7-day average-stay test, §280A personal-use test, excess business loss cap

## The core decision rule

> A deal **passes** if: (1) the parcel has a legal, durable path to STR permitting,
> (2) Year-1 after-tax cashflow (pre-tax cashflow + tax savings) ≥ 0, **and**
> (3) stabilized (Year 2+) after-tax cashflow is break-even or a slight loss —
> within the configurable `stabilized_loss_tolerance` (default $12k/yr, i.e. ~$1k/mo).

Year-1 bonus depreciation is a one-time boost, so the every-year goal is governed by
the stabilized number. Owner guidance: aim for break-even every year; a slight loss is
acceptable; cheaper properties are preferred (the §461(l) cap means a ~$1.2M property
captures nearly the same Year-1 tax savings as a $2.4M one).

## Financing assumption

Baseline financing stack per scenario:

- Investment mortgage at ~7% / 30yr on 75% of price, plus
- **Trust line of credit** (borrowing against trust assets, >$1M available) at
  **prime + 1% = 7.75%** (WSJ prime 6.75%, July 2026), interest-only, funding the
  down payment / closing / furnishing — so cash out of pocket is ~$0.

Trust-line interest is deductible against the STR under interest-tracing rules since
the proceeds fund the rental activity. Note the trade-off: 100% financing adds
~$28–44k/yr of interest carry, which makes the stabilized every-year goal materially
harder — the model shows this directly, and putting some cash equity in (or drawing
less of the line) is the main lever to fix it.

## Disclaimer

This is a decision-support tool, not tax or legal advice. The STR loophole has strict
requirements (average stay ≤ 7 days, material participation, personal-use limits) that we
must verify with our CPA before closing on anything.
