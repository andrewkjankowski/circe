#!/usr/bin/env python3
"""STR second-home deal analyzer.

Evaluates whether a property breaks even AFTER tax savings from the STR
strategy (cost segregation + 100% bonus depreciation + material participation),
even if pre-tax cashflow is negative.

Usage:
    python3 analysis/deal_analyzer.py scenarios/encinitas_example.toml
    python3 analysis/deal_analyzer.py scenarios/*.toml   # comparison table

No third-party dependencies (Python 3.11+ for tomllib).
"""

from __future__ import annotations

import sys
import tomllib
from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Tax constants (2026 law; update as needed)
# ---------------------------------------------------------------------------
BONUS_DEPRECIATION_RATE = 1.00     # OBBBA: permanent 100% for property placed in
                                   # service after 2025-01-19
EXCESS_BUSINESS_LOSS_CAP_MFJ = 317_000  # §461(l), 2026 MFJ (indexed annually)
DEFAULT_BUILDING_RECOVERY_YEARS = 39    # conservative: avg stay <=7d -> nonresidential

# 2026 federal MFJ brackets (Rev. Proc. 2025-32): (upper bound, rate)
FEDERAL_BRACKETS_MFJ = [
    (24_800, 0.10), (100_800, 0.12), (211_400, 0.22), (403_550, 0.24),
    (512_450, 0.32), (768_700, 0.35), (float("inf"), 0.37),
]
# CA MFJ Schedule Y (2025 FTB schedules; 2026 indexation pending)
CA_BRACKETS_MFJ = [
    (22_158, 0.01), (52_528, 0.02), (82_904, 0.04), (115_084, 0.06),
    (145_448, 0.08), (742_958, 0.093), (891_542, 0.103),
    (1_485_906, 0.113), (float("inf"), 0.123),
]
# CA Mental Health Services Tax: +1% on taxable income over $1M (doesn't double MFJ)
CA_MHST_THRESHOLD = 1_000_000


def tax_from_brackets(taxable: float, brackets: list[tuple[float, float]]) -> float:
    taxable = max(taxable, 0.0)
    tax = 0.0
    lower = 0.0
    for upper, rate in brackets:
        if taxable <= lower:
            break
        tax += (min(taxable, upper) - lower) * rate
        lower = upper
    return tax


def federal_tax(taxable: float) -> float:
    return tax_from_brackets(taxable, FEDERAL_BRACKETS_MFJ)


def ca_tax(taxable: float) -> float:
    t = tax_from_brackets(taxable, CA_BRACKETS_MFJ)
    if taxable > CA_MHST_THRESHOLD:
        t += (taxable - CA_MHST_THRESHOLD) * 0.01
    return t


@dataclass
class Scenario:
    name: str
    market: str

    # --- purchase ---
    purchase_price: float
    land_pct: float                 # share of price allocated to land (assessor ratio)
    closing_costs_pct: float = 0.02
    furnishing_budget: float = 40_000.0
    cost_seg_study_cost: float = 5_000.0

    # --- financing ---
    down_payment_pct: float = 0.25
    interest_rate: float = 0.0675
    loan_term_years: int = 30
    # Trust line of credit (borrow against trust assets). Interest-only, variable.
    # Used as a BRIDGE: it funds cash-to-close beyond our own cash, then the Year-1
    # tax savings are swept against the balance, shrinking the Year-2+ carry.
    # Interest is deductible against the STR under interest-tracing rules (§163;
    # Reg. 1.163-8T) since proceeds are used for the rental activity.
    # NOTE: interest-only + variable at prime+1% is an ASSUMPTION — actual line
    # mechanics (amortization, rate reset) pending financial-advisor confirmation.
    trust_line_amount: float = 0.0
    trust_line_rate: float = 0.0775      # WSJ prime 6.75% (Jul 2026) + 1%
    owner_cash_at_close: float = 50_000.0  # our own cash contributed at closing

    # --- revenue ---
    adr: float = 500.0              # average daily rate, net of TOT (guest pays TOT)
    occupancy: float = 0.60         # share of the 365-night year that is guest-occupied
    avg_stay_nights: float = 3.5    # for the ≤7-day test
    revenue_ramp_year1: float = 0.75  # year 1 revenue as fraction of stabilized

    # --- operating expenses ---
    platform_fee_pct: float = 0.03      # host-side channel fee on gross rents
    mgmt_fee_pct: float = 0.0           # keep 0 if self-managing for material participation
    cleaning_net_cost_per_turn: float = 0.0  # cleaning cost not covered by guest fees
    property_tax_rate: float = 0.0115   # CA effective incl. bonds/Mello-Roos varies
    insurance_annual: float = 8_000.0
    utilities_annual: float = 9_600.0   # power, water, internet, trash
    maintenance_pct_of_rents: float = 0.05
    supplies_annual: float = 3_600.0
    hoa_annual: float = 0.0
    permits_licenses_annual: float = 1_000.0
    other_annual: float = 0.0

    # --- tax profile ---
    # Household taxable income BEFORE the STR loss (income minus deductions).
    # Savings are computed bracket-by-bracket: a big deduction reaches down into
    # lower brackets, so the effective rate is blended, not the top marginal rate.
    household_taxable_income: float = 568_000.0   # ~$600k income - $32.2k std ded
    cost_seg_reclass_pct: float = 0.28  # share of improvement basis moved to 5/7/15-yr
    building_recovery_years: float = DEFAULT_BUILDING_RECOVERY_YEARS
    months_in_service_year1: int = 6    # months from placed-in-service to Dec 31
    personal_use_days: int = 14
    filing_status_mfj: bool = True

    # --- goal ---
    # "Break even every year if we can; a slight loss is acceptable."
    stabilized_loss_tolerance: float = 12_000.0   # max acceptable after-tax loss, yr 2+

    notes: str = ""

    @classmethod
    def from_toml(cls, path: str) -> "Scenario":
        with open(path, "rb") as f:
            raw = tomllib.load(f)
        flat: dict = {}
        for key, value in raw.items():
            if isinstance(value, dict):
                flat.update(value)
            else:
                flat[key] = value
        valid = {f.name for f in cls.__dataclass_fields__.values()}  # type: ignore[attr-defined]
        unknown = set(flat) - valid
        if unknown:
            raise ValueError(f"{path}: unknown keys {sorted(unknown)}")
        return cls(**flat)


@dataclass
class Result:
    scenario: Scenario
    cash_to_close: float = 0.0
    loan_amount: float = 0.0
    trust_draw: float = 0.0
    trust_paydown_year1: float = 0.0
    trust_balance_stabilized: float = 0.0
    debt_service_year1: float = 0.0
    debt_service_stabilized: float = 0.0
    year1_interest: float = 0.0

    gross_rents_stabilized: float = 0.0
    gross_rents_year1: float = 0.0
    operating_expenses_year1: float = 0.0
    operating_expenses_stabilized: float = 0.0
    noi_year1: float = 0.0
    noi_stabilized: float = 0.0
    pretax_cashflow_year1: float = 0.0
    pretax_cashflow_stabilized: float = 0.0

    improvement_basis: float = 0.0
    bonus_depreciation: float = 0.0
    sl_depreciation_year1: float = 0.0
    sl_depreciation_full_year: float = 0.0
    taxable_loss_year1: float = 0.0
    loss_allowed_year1: float = 0.0
    ebl_carryforward: float = 0.0
    federal_tax_savings_year1: float = 0.0
    ca_tax_savings_year1: float = 0.0
    total_tax_savings_year1: float = 0.0
    tax_savings_stabilized: float = 0.0

    after_tax_cashflow_year1: float = 0.0
    after_tax_cashflow_stabilized: float = 0.0
    flags: list[str] = field(default_factory=list)

    @property
    def hard_fail(self) -> bool:
        return any(f.startswith("FAIL") for f in self.flags)

    @property
    def passes(self) -> bool:
        """Goal: break even after tax every year; slight stabilized loss OK."""
        return (not self.hard_fail
                and self.after_tax_cashflow_year1 >= 0
                and self.after_tax_cashflow_stabilized
                >= -self.scenario.stabilized_loss_tolerance)


def monthly_payment(principal: float, annual_rate: float, years: int) -> float:
    r = annual_rate / 12
    n = years * 12
    if r == 0:
        return principal / n
    return principal * r / (1 - (1 + r) ** -n)


def first_year_interest(principal: float, annual_rate: float, years: int) -> float:
    """Sum of interest portions over the first 12 payments."""
    r = annual_rate / 12
    pmt = monthly_payment(principal, annual_rate, years)
    balance = principal
    interest = 0.0
    for _ in range(12):
        i = balance * r
        interest += i
        balance -= pmt - i
    return interest


def analyze(s: Scenario) -> Result:
    r = Result(scenario=s)

    # --- acquisition & financing ---
    down = s.purchase_price * s.down_payment_pct
    closing = s.purchase_price * s.closing_costs_pct
    total_cash_needed = down + closing + s.furnishing_budget + s.cost_seg_study_cost
    r.trust_draw = min(s.trust_line_amount,
                       max(total_cash_needed - s.owner_cash_at_close, 0.0))
    r.cash_to_close = total_cash_needed - r.trust_draw
    r.loan_amount = s.purchase_price - down
    mortgage_payment_annual = monthly_payment(r.loan_amount, s.interest_rate,
                                              s.loan_term_years) * 12
    trust_interest_y1 = r.trust_draw * s.trust_line_rate  # interest-only carry
    r.debt_service_year1 = mortgage_payment_annual + trust_interest_y1
    r.year1_interest = (first_year_interest(r.loan_amount, s.interest_rate,
                                            s.loan_term_years)
                        + trust_interest_y1)

    # --- revenue ---
    occupied_nights = 365 * s.occupancy
    r.gross_rents_stabilized = s.adr * occupied_nights
    r.gross_rents_year1 = r.gross_rents_stabilized * s.revenue_ramp_year1
    turns_stabilized = occupied_nights / max(s.avg_stay_nights, 1)

    def opex(rents: float, turns: float) -> float:
        return (
            rents * (s.platform_fee_pct + s.mgmt_fee_pct + s.maintenance_pct_of_rents)
            + turns * s.cleaning_net_cost_per_turn
            + s.purchase_price * s.property_tax_rate
            + s.insurance_annual + s.utilities_annual + s.supplies_annual
            + s.hoa_annual + s.permits_licenses_annual + s.other_annual
        )

    r.operating_expenses_stabilized = opex(r.gross_rents_stabilized, turns_stabilized)
    r.operating_expenses_year1 = opex(r.gross_rents_year1,
                                      turns_stabilized * s.revenue_ramp_year1)
    r.noi_stabilized = r.gross_rents_stabilized - r.operating_expenses_stabilized
    r.noi_year1 = r.gross_rents_year1 - r.operating_expenses_year1
    r.pretax_cashflow_year1 = r.noi_year1 - r.debt_service_year1

    # --- depreciation ---
    basis = s.purchase_price + closing            # closing costs capitalize into basis
    r.improvement_basis = basis * (1 - s.land_pct)
    reclassified = r.improvement_basis * s.cost_seg_reclass_pct
    r.bonus_depreciation = (reclassified + s.furnishing_budget) * BONUS_DEPRECIATION_RATE
    building_basis = r.improvement_basis - reclassified
    r.sl_depreciation_full_year = building_basis / s.building_recovery_years
    # approximate mid-month convention with months in service
    r.sl_depreciation_year1 = (r.sl_depreciation_full_year
                               * max(s.months_in_service_year1 - 0.5, 0.5) / 12)

    # --- year-1 taxable income (federal) ---
    # taxable = NOI - interest - depreciation - cost-seg study (deductible)
    taxable_year1 = (r.noi_year1 - r.year1_interest - r.bonus_depreciation
                     - r.sl_depreciation_year1 - s.cost_seg_study_cost)
    r.taxable_loss_year1 = -taxable_year1 if taxable_year1 < 0 else 0.0

    cap = EXCESS_BUSINESS_LOSS_CAP_MFJ if s.filing_status_mfj else \
        EXCESS_BUSINESS_LOSS_CAP_MFJ / 2
    r.loss_allowed_year1 = min(r.taxable_loss_year1, cap)
    r.ebl_carryforward = max(r.taxable_loss_year1 - cap, 0.0)
    income = s.household_taxable_income
    r.federal_tax_savings_year1 = (federal_tax(income)
                                   - federal_tax(income - r.loss_allowed_year1))

    # --- California: no bonus depreciation; straight-line only ---
    ca_depreciation_year1 = ((r.improvement_basis / s.building_recovery_years)
                             * max(s.months_in_service_year1 - 0.5, 0.5) / 12
                             + s.furnishing_budget / 7
                             * s.months_in_service_year1 / 12)
    ca_taxable_year1 = (r.noi_year1 - r.year1_interest - ca_depreciation_year1
                        - s.cost_seg_study_cost)
    ca_loss = -ca_taxable_year1 if ca_taxable_year1 < 0 else 0.0
    r.ca_tax_savings_year1 = ca_tax(income) - ca_tax(income - ca_loss)
    r.total_tax_savings_year1 = r.federal_tax_savings_year1 + r.ca_tax_savings_year1

    # --- compliance flags (hard fails suspend the loss -> no tax savings) ---
    if s.avg_stay_nights > 7:
        r.flags.append("FAIL: average stay > 7 nights — losses are passive "
                       "(§469 rental); tax savings zeroed (loss suspended)")
    rented_days = occupied_nights * s.revenue_ramp_year1
    personal_cap = max(14, 0.10 * rented_days)
    if s.personal_use_days > personal_cap:
        r.flags.append(f"FAIL: personal use {s.personal_use_days}d exceeds §280A cap "
                       f"({personal_cap:.0f}d) — losses disallowed; tax savings zeroed")
    hard_fail = any(f.startswith("FAIL") for f in r.flags)
    if hard_fail:
        r.federal_tax_savings_year1 = 0.0
        r.ca_tax_savings_year1 = 0.0
        r.total_tax_savings_year1 = 0.0

    # --- bridge paydown: sweep Year-1 tax savings against the trust line ---
    r.trust_paydown_year1 = min(r.total_tax_savings_year1, r.trust_draw)
    r.trust_balance_stabilized = r.trust_draw - r.trust_paydown_year1
    trust_interest_stab = r.trust_balance_stabilized * s.trust_line_rate
    r.debt_service_stabilized = mortgage_payment_annual + trust_interest_stab
    r.pretax_cashflow_stabilized = r.noi_stabilized - r.debt_service_stabilized

    # --- stabilized (year 2+): federal bonus is gone (building SL only);
    # CA keeps depreciating everything straight-line, so CA depreciation is larger.
    # Year-1 mortgage interest approximates early-year interest.
    mortgage_interest_stab = first_year_interest(r.loan_amount, s.interest_rate,
                                                 s.loan_term_years)
    interest_stab = mortgage_interest_stab + trust_interest_stab
    fed_taxable_stab = (r.noi_stabilized - interest_stab
                        - r.sl_depreciation_full_year)
    ca_depr_stab = r.improvement_basis / s.building_recovery_years \
        + s.furnishing_budget / 7
    ca_taxable_stab = r.noi_stabilized - interest_stab - ca_depr_stab
    # positive savings if taxable loss; negative (tax owed) if taxable income
    r.tax_savings_stabilized = (
        federal_tax(income) - federal_tax(income + fed_taxable_stab)
        + ca_tax(income) - ca_tax(income + ca_taxable_stab))

    if hard_fail:
        r.tax_savings_stabilized = min(r.tax_savings_stabilized, 0.0)

    r.after_tax_cashflow_year1 = r.pretax_cashflow_year1 + r.total_tax_savings_year1
    r.after_tax_cashflow_stabilized = (r.pretax_cashflow_stabilized
                                       + r.tax_savings_stabilized)

    if r.ebl_carryforward > 0 and not hard_fail:
        r.flags.append(f"WARN: §461(l) excess business loss — "
                       f"${r.ebl_carryforward:,.0f} deferred to NOL carryforward")
    if s.mgmt_fee_pct > 0:
        r.flags.append("WARN: property manager engaged — material participation "
                       "(100-hr / more-than-anyone test) is at risk")
    if s.land_pct >= 0.5:
        r.flags.append(f"WARN: land allocation {s.land_pct:.0%} — cost-seg benefit "
                       "is significantly diluted")
    return r


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------
def money(x: float) -> str:
    return f"-${abs(x):,.0f}" if x < 0 else f"${x:,.0f}"


def print_report(r: Result) -> None:
    s = r.scenario
    w = 78
    print("=" * w)
    print(f"{s.name}  [{s.market}]")
    if s.notes:
        print(f"  {s.notes}")
    print("=" * w)
    print(f"""
ACQUISITION
  Purchase price                 {money(s.purchase_price):>14}
  Land allocation                {s.land_pct:>13.0%}   (improvement basis {money(r.improvement_basis)})
  Our cash at close                            {money(r.cash_to_close):>14}
  Trust line draw @ {s.trust_line_rate:.2%} (interest-only bridge)  {money(r.trust_draw):>12}
    swept with Y1 tax savings: -{money(r.trust_paydown_year1)} -> Y2+ balance {money(r.trust_balance_stabilized)}
  Mortgage {money(r.loan_amount)} @ {s.interest_rate:.3%}, {s.loan_term_years}y

OPERATIONS                          Year 1        Stabilized
  Gross rents                 {money(r.gross_rents_year1):>14} {money(r.gross_rents_stabilized):>14}
  Operating expenses          {money(-r.operating_expenses_year1):>14} {money(-r.operating_expenses_stabilized):>14}
  NOI                         {money(r.noi_year1):>14} {money(r.noi_stabilized):>14}
  Debt service                {money(-r.debt_service_year1):>14} {money(-r.debt_service_stabilized):>14}
  PRE-TAX CASHFLOW            {money(r.pretax_cashflow_year1):>14} {money(r.pretax_cashflow_stabilized):>14}

YEAR-1 TAX (vs household taxable income {money(s.household_taxable_income)}, MFJ brackets)
  Bonus depreciation (cost-seg + furnishings)  {money(r.bonus_depreciation):>14}
  Straight-line depreciation (yr 1)            {money(r.sl_depreciation_year1):>14}
  Year-1 taxable loss                          {money(r.taxable_loss_year1):>14}
  Loss usable this year (§461(l) cap)          {money(r.loss_allowed_year1):>14}
  Federal tax savings (blended {r.federal_tax_savings_year1 / r.loss_allowed_year1 if r.loss_allowed_year1 else 0:.1%})        {money(r.federal_tax_savings_year1):>14}
  CA tax savings (no bonus conformity)         {money(r.ca_tax_savings_year1):>14}
  TOTAL YEAR-1 TAX SAVINGS                     {money(r.total_tax_savings_year1):>14}

VERDICT
  After-tax cashflow, Year 1        {money(r.after_tax_cashflow_year1):>14}   {'meets Y1 break-even' if r.after_tax_cashflow_year1 >= 0 else 'misses Y1 break-even'}
  After-tax cashflow, stabilized    {money(r.after_tax_cashflow_stabilized):>14}   {'within tolerance (-' + money(s.stabilized_loss_tolerance)[1:] + ')' if r.after_tax_cashflow_stabilized >= -s.stabilized_loss_tolerance else 'exceeds loss tolerance (-' + money(s.stabilized_loss_tolerance)[1:] + ')'}
  Overall: {'PASS' if r.passes else ('FAIL (compliance)' if r.hard_fail else 'MISS (economics)')}""")
    if r.flags:
        print("\nFLAGS")
        for f in r.flags:
            print(f"  ! {f}")
    print()


def print_comparison(results: list[Result]) -> None:
    w = 118
    print("=" * w)
    print(f"{'Scenario':<28}{'Price':>12}{'Cash in':>12}{'PreTax CF Y1':>14}"
          f"{'Tax Save Y1':>13}{'AfterTax Y1':>13}{'AfterTax Y2+':>14}{'Verdict':>12}")
    print("-" * w)
    for r in sorted(results, key=lambda x: -x.after_tax_cashflow_stabilized):
        s = r.scenario
        verdict = "PASS" if r.passes else ("FAIL" if r.hard_fail else "MISS")
        print(f"{s.name[:27]:<28}{money(s.purchase_price):>12}"
              f"{money(r.cash_to_close):>12}{money(r.pretax_cashflow_year1):>14}"
              f"{money(r.total_tax_savings_year1):>13}"
              f"{money(r.after_tax_cashflow_year1):>13}"
              f"{money(r.after_tax_cashflow_stabilized):>14}{verdict:>12}")
    print("=" * w)
    print("PASS = Y1 after-tax break-even AND stabilized after-tax loss within")
    print("       tolerance, with no compliance failures.")
    print("MISS = compliant but misses the economic goal (see per-scenario detail).")
    print("FAIL = a strategy requirement is violated (see per-scenario flags).")


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 1
    results = [analyze(Scenario.from_toml(p)) for p in argv[1:]]
    for r in results:
        print_report(r)
    if len(results) > 1:
        print_comparison(results)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
