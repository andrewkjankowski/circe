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

> A deal passes if: `pre-tax cashflow + tax savings ≥ 0` in Year 1 **and** stabilized
> (Year 2+) after-tax cashflow is not deeply negative, **and** the parcel has a legal,
> durable path to STR permitting.

Year-1 bonus depreciation is a one-time boost. Years 2+ must stand closer to their own
feet, so the model shows both.

## Disclaimer

This is a decision-support tool, not tax or legal advice. The STR loophole has strict
requirements (average stay ≤ 7 days, material participation, personal-use limits) that we
must verify with our CPA before closing on anything.
