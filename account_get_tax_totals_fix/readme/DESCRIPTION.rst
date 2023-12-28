This module fixes some corner-case issues of the _get_tax_toltals() method of
account.move.

Corner-case issue example:
--------------------------

Rounding Method configuration: Round Globally

Create an invoice with following conditions:

- Currency: JPY
- A line with price 12,345 and 10% tax (exclusive)

Result on totals:

- Untaxed Amount: 12,345
- Taxes: 1,234
- Total: 13,580

Total is incorrect. It should show as 13,579.
