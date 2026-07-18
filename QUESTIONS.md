# Open Questions

Answers to these will materially change the analysis. Grouped by how much they move the
numbers. Where useful, the current model default is noted so you can just confirm or
correct it.

## Answered so far (July 2026)

- **Goal (was Q7):** aim for after-tax break-even **every year**; a slight stabilized
  loss is acceptable. Encoded as `stabilized_loss_tolerance` (default $12k/yr) in the
  model — confirm or change that number.
- **Price philosophy (was part of Q5):** cheaper is optimal — agreed, since the §461(l)
  cap binds. Still need the actual budget ceiling.
- **Financing (was Q6):** trust line of credit (>$1M available) at prime + 1% (7.75%
  currently), assumed interest-only, funding cash-to-close; investment mortgage for the
  rest. Encoded as `trust_line_amount` / `trust_line_rate` per scenario.

## A. Tax profile (drives the entire break-even math)

1. **What is your combined marginal tax rate?** Federal bracket (model assumes 37%) and
   California bracket (model assumes 10.3%). Also: filing MFJ? Any AMT exposure?
2. **How much W-2/active income are you sheltering?** The §461(l) excess-business-loss
   cap (~$317k MFJ in 2026) already binds in every example scenario at these price
   points. If your income is such that a $317k deduction saves less than modeled, or you
   want to stay under the cap, that changes the optimal purchase price — a *cheaper*
   property can capture nearly the same Year-1 savings.
3. **Does either spouse have (or want) Real Estate Professional Status?** Not required
   for this strategy, but it changes the fallback options if the 7-day test ever fails.
4. **Who is your CPA and have they run STR-loophole returns before?** Their positions
   (27.5 vs 39-year building life, land allocation method) should be baked into the model.

## B. Budget and financing

5. **Purchase price ceiling?** Examples now span $1.2–2.6M. Given "cheaper is optimal,"
   what's the realistic band — and is a condo acceptable, or single-family only?
   (Condos have much lower land allocations, which helps the tax math, but most condo
   HOAs prohibit STRs.)
6. **Trust line details.** Is the prime+1% line interest-only or amortizing? Is there a
   draw limit you want to respect (e.g., only fund the down payment, not 100% of cash
   needs)? Full 100% financing adds ~$28–44k/yr of carry and currently pushes every
   example past the $12k/yr stabilized-loss tolerance — putting ~$200–300k cash equity
   in (or a smaller draw) is the main fix.
7. **What counts as a "slight loss"?** Model default is $12k/yr (~$1k/mo) after tax.
   Confirm or set your number.

## C. How you'll actually use and run the property

8. **How many personal-use nights do you want per year?** The §280A cap is the greater
   of 14 nights or 10% of rented nights. If you want 30+ nights of personal use, the
   loss-harvesting strategy fails in that year. Is ~14 nights/yr acceptable, at least
   for Year 1?
9. **Who self-manages?** Material participation effectively requires self-management
   (100+ hours and more than any other person) in Year 1. Given day jobs, is that
   realistic? This is also the strongest argument for **North County San Diego over
   Monterey/Santa Barbara** if you live in or near San Diego — where are you based?
10. **Timeline?** To take the deduction for tax year 2026, the property must be
    purchased, furnished, permitted, and *listed* by Dec 31, 2026. That is tight.
    Is 2026 the target year or 2027?

## D. Market selection

11. **Monterey reality check:** Carmel-by-the-Sea, the City of Monterey, Pacific Grove,
    and (as of the Jan 2026 county vote) Pebble Beach/Carmel Valley residential zones
    all prohibit or effectively block non-hosted STRs, and the Pebble Beach Company
    blocks permits in Del Monte Forest. **Do you want to drop Monterey from the STR
    analysis** (keep it as a pure second-home option), or should we hunt for the rare
    commercial-zoned exceptions?
12. **Del Mar is capped/waitlisted and primary-residence-only; Solana Beach's 7-night
    minimum breaks the tax test.** Within North County that leaves Encinitas, Carlsbad
    (Coastal Zone), and City of San Diego (Torrey Pines/La Jolla, Tier 3 license). OK to
    focus there?
13. **Santa Barbara is mid-rulemaking** (new ordinance targeted Sept 2026 + Coastal
    Commission into 2027). Buying there now carries regulatory-change risk both ways
    (grandfathering vs. tightening). What's your risk appetite for that?

## E. Revenue assumptions (to replace my placeholders)

14. Do you have access to **AirDNA / Rabbu / PriceLabs comps** for the target zips, or
    should we pull comp data another way? Model placeholders: ADR $500–650, 60–62%
    occupancy, which are rough mid-range values, not researched comps.
15. **Property profile:** bedrooms/sleeps target, pool/hot-tub, pet-friendly? These move
    ADR 20–40% in these markets.

## F. The Instagram reel

16. Instagram blocks scraping, so the reel's specific claims couldn't be reviewed. The
    strategy doc (`docs/strategy.md`) covers the standard version of this play. If the
    reel made specific claims or used specific numbers you want validated, paste a
    transcript or screenshots and we'll reconcile them.
