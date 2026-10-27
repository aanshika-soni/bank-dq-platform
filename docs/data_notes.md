# Data notes: profiling results

Source: PKDD'99 Financial (Berka) dataset, from the CTU Prague Relational Dataset Repository.
Profiled with src/profile_data.py, profile_trans.py, profile_followup.py, profile_bank.py, profile_transfers.py and profile_transfer_gap.py.

## Table sizes
- trans: 1,056,320 rows
- order: 6,471
- client: 5,369
- disp: 5,369
- account: 4,500
- card: 892
- loan: 682
- district: 77

## Dates
- trans dates run from 1993-01-01 to 1998-12-31, so this is historical data.
- Timeliness rules must use the dataset's own end date (1998-12-31), not today's date.
- All date columns load as text and must be cast to DATE in staging.

## Duplicates
- No duplicate rows in any table and no duplicate trans_id.
- Any duplicates found later were injected by me on purpose.

## Transaction types and operations (trans)
- type: VYDAJ 634,571 / PRIJEM 405,083 / VYBER 16,666 (sums to the full row count).
- operation: VYBER 434,918 / PREVOD NA UCET 208,283 / null 183,114 / VKLAD 156,743 / PREVOD Z UCTU 65,226 / VYBER KARTOU 8,036.
- Withdrawals use two type codes: VYDAJ with operation VYBER (418,252 rows) and VYBER with operation VYBER (16,666 rows). Both are treated as debits. Original code kept for the consistency rule.

## Missing values in trans
- k_symbol: 481,881 nulls plus 53,433 blank-text values, about 50.7% with no payment purpose. The same "missing" is stored two ways. Blank text is converted to null in staging.
- operation: 183,114 nulls (17.3%). Confirmed: every null operation is an interest credit (k_symbol = UROK, type PRIJEM) and every UROK row has a null operation. Nulls are expected here, so no completeness rule on operation.
- bank: 782,812 nulls (74.1%). account: 760,931 nulls (72.0%). These describe the other party and are expected to be empty for non-transfers.
- bank is never filled for non-transfers (0 rows).
- All 21,881 rows with an account but no bank are withdrawals: VYBER (13,845) and VYBER KARTOU (8,036). The 8,036 equals every card withdrawal in the table. This looks like how withdrawals are recorded, not a defect.
- Some of those withdrawals carry a payment purpose (SIPO 2,811; POJISTNE 23), which is unusual for a withdrawal. To review later.
- Transfers with an account (273,508) plus withdrawals with an account (21,881) equals 295,389, which matches the overall count of rows with an account.
- bank has 13 distinct two-letter codes (AB to YZ), all well formed.

## Real defect found in the source data
- Among 273,509 transfers, exactly 1 has a null bank and a null account: trans_id 236564 (account 808, 1996-04-12, outgoing transfer of 4,500, k_symbol UVER loan payment). Every other transfer has both fields.
- Cause unknown. Comparison with other loan payments on account 808 not done yet (optional follow-up).

## Distributions
- amount: median 2,100, mean 5,924, max 87,400 (skewed, a few large values pull the mean up). 162 zero-amount transactions (0.015%).
- balance: ranges from -41,126 to 209,637. 2,999 negative balances (0.28%); review as warnings, not automatic failures.

## Other tables
- district: columns A2 to A16 need readable names. A12 and A15 have 1 null each.
- order: k_symbol has 1,379 nulls (21.3%) and no blank-text values.
- account.frequency, loan.status and the trans codes are Czech or single letters and need translating in staging.

## Implications for my data quality rules
- Bank/account completeness applies to transfers only (PREVOD NA UCET, PREVOD Z UCTU). Expected to fail on exactly 1 row (trans_id 236564).
- Treat blank text in k_symbol as null before validating.
- Use IQR or per-account comparison for amount outliers, not a plain z-score.
- Define timeliness against 1998-12-31.
- Zero amounts and negative balances are warnings with low severity.
- Add a consistency rule for the two withdrawal type codes.

## Open items (do later)
- Compare trans_id 236564 with other loan payments on account 808 and with the loan table.
- Review withdrawals that carry a payment purpose.