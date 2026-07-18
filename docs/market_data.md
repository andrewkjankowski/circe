# STR Market Data — Target Markets

_Snapshot: July 2026. Sources: AirDNA MarketMinder, AirROI (TTM datasets), Rabbu,
StaySTRA, Airbtics. These are market averages across ALL active listings — including
part-time, poorly managed, and room-share listings — so a purpose-bought, full-time,
well-furnished, self-managed whole home should land between the median and the top
quartile. Scenario inputs below target roughly the 60–75th percentile._

## Why sources disagree

"Average annual revenue" differs wildly between providers ($43k–$84k for Carlsbad)
because each uses a different listing universe and availability filter. ADR × 365 ×
occupancy for a full-time listing is materially higher than "average listing revenue"
because the average listing is not available year-round. We model a dedicated full-time
rental, so we anchor to ADR and occupancy, sanity-checked against bedroom-level revenue.

## Market metrics (all-listing averages)

| Market | Source (period) | ADR | Occupancy | Avg annual revenue |
|---|---|---|---|---|
| **Encinitas** | AirDNA (TTM Jun 2026) | $476 | 66% | $50.5k |
| | AirROI (Jun 2025–May 2026) | $572 | 49% | $71.8k |
| **Carlsbad** | AirDNA (2026) | $414 | 62% | $43.4k |
| | StaySTRA (Apr 2026) | $299 ($321 entire-home) | 65% | ~$64k ($71.5k houses) |
| | Airbtics (Feb 2025–Jan 2026) | $332 | 68% | $84k (median) |
| | AirROI (Jul 2025–Jun 2026) | $448 | 46% | $58.1k |
| **Carpinteria** | Rabbu (Apr 2026) | $445 | 35% | $59.0k |
| | AirROI (Apr 2025–Mar 2026) | $483 | 43% | $62.9k |
| | AirDNA | $451 | 52% | $44.5k |
| | STR Profit Map ("middle earners") | — | 59% | $63.7k |
| **Santa Barbara city** | AirDNA | $521 | 62% | $57.5k |
| **Montecito** | AirROI | — | 49% | $121.4k |

## Bedroom-level benchmarks

- **San Diego market, 3BR** (AirROI 2026): $77.0k/yr revenue, $539 ADR, 54% occupancy.
- **San Diego market, 2BR**: $52.0k/yr, $355 ADR, 56% occupancy.
- **Carpinteria 2BR**: $383 ADR; **3BR**: $601 ADR; 4BR $952 ADR / $185.9k revenue.
- Encinitas top quartile: $10.9k+/mo (~$130k/yr) at 74%+ occupancy; median ~$6.3k/mo.
- Encinitas seasonal ADR: ~$581 summer peak, ~$512 winter (AirROI).

## Scenario input calibration (what we now use)

| Scenario | ADR | Occ | Implied stabilized gross | Anchor |
|---|---|---|---|---|
| Encinitas 3BR coastal | $525 | 55% | ~$105k | Between SD-3BR median ($77k) and Encinitas top quartile ($130k); west-of-I-5 premium |
| Carlsbad 3BR Coastal Zone | $425 | 58% | ~$90k | Entire-home ADR $321–448 range, upper half; houses avg $71.5k |
| Carlsbad Village 2BR condo | $320 | 60% | ~$70k | SD-2BR avg $52k + walkable-Village premium |
| Carpinteria 2BR beach zone | $385 | 50% | ~$70k | Rabbu 2BR ADR $383; occ between market 35–43% avg and 59% middle-earner |
| Solana Beach 3BR (fail demo) | $600 | 45% | ~$99k | 7-night-min market, weekly bookings |

Caveats:

- Market occupancy has real seasonality (July peak, Jan trough); annual averages hide
  ~2x monthly swings. Reserves must cover winter.
- Carpinteria has only ~117–361 active listings — thin comp set, wide error bars, and
  a hard cap of 218 vacation-rental licenses in the beach district.
- Carlsbad's Coastal-Zone-only permit rule caps supply — a structural tailwind for
  permit holders (StaySTRA notes this explicitly).
- Next fidelity step (Phase 2): property-level comps via AirDNA Rentalizer / AirROI
  estimate API / Rabbu address lookup for specific candidate addresses, using p50 and
  p75 revenue percentiles rather than market averages.
