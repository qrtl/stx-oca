from collections import defaultdict

from odoo import _
from odoo.tools.misc import formatLang

from odoo.addons.account.models.account_move import AccountMove


def _new_get_tax_totals(
    self, partner, tax_lines_data, amount_total, amount_untaxed, currency
):  # noqa
    account_tax = self.env["account.tax"]

    grouped_taxes = defaultdict(
        lambda: defaultdict(
            lambda: {"base_amount": 0.0, "tax_amount": 0.0, "base_line_keys": set()}
        )
    )  # noqa
    subtotal_priorities = {}
    for line_data in tax_lines_data:
        tax_group = line_data["tax"].tax_group_id

        # Update subtotals priorities
        if tax_group.preceding_subtotal:
            subtotal_title = tax_group.preceding_subtotal
            new_priority = tax_group.sequence
        else:
            # When needed, the default subtotal is always the most prioritary
            subtotal_title = _("Untaxed Amount")
            new_priority = 0

        if (
            subtotal_title not in subtotal_priorities
            or new_priority < subtotal_priorities[subtotal_title]
        ):  # noqa
            subtotal_priorities[subtotal_title] = new_priority

        # Update tax data
        tax_group_vals = grouped_taxes[subtotal_title][tax_group]

        if "base_amount" in line_data:
            # Base line
            if (
                tax_group
                == line_data.get("tax_affecting_base", account_tax).tax_group_id
            ):  # noqa
                # In case the base has a tax_line_id belonging to the same group as the base tax,  # noqa
                # the base for the group will be computed by the base tax's original line (the one with tax_ids and no tax_line_id)  # noqa
                continue

            if line_data["line_key"] not in tax_group_vals["base_line_keys"]:
                # If the base line hasn't been taken into account yet, at its amount to the base total.  # noqa
                tax_group_vals["base_line_keys"].add(line_data["line_key"])
                tax_group_vals["base_amount"] += line_data["base_amount"]

        else:
            # Tax line
            tax_group_vals["tax_amount"] += line_data["tax_amount"]

    # Compute groups_by_subtotal
    groups_by_subtotal = {}
    tax_amount_total = 0.0  # QRTL
    for subtotal_title, groups in grouped_taxes.items():

        # QRTL: Following several lines are replaced by the subsequent lines.
        # groups_vals = [{
        #     'tax_group_name': group.name,
        #     'tax_group_amount': amounts['tax_amount'],
        #     'tax_group_base_amount': amounts['base_amount'],
        #     'formatted_tax_group_amount': formatLang(self.env, amounts['tax_amount'], currency_obj=currency),  # noqa: B950
        #     'formatted_tax_group_base_amount': formatLang(self.env, amounts['base_amount'], currency_obj=currency),  # noqa: B950
        #     'tax_group_id': group.id,
        #     'group_key': '%s-%s' %(subtotal_title, group.id),
        # } for group, amounts in sorted(groups.items(), key=lambda l: l[0].sequence)]
        # QRTL >>>
        groups_vals = []
        for group, amounts in sorted(groups.items(), key=lambda l: l[0].sequence):
            tax_group_amount = currency.round(amounts["tax_amount"])
            tax_amount_total += tax_group_amount
            groups_vals.append(
                {
                    "tax_group_name": group.name,
                    "tax_group_amount": tax_group_amount,  # QRTL
                    "tax_group_base_amount": amounts["base_amount"],
                    "formatted_tax_group_amount": formatLang(
                        self.env, tax_group_amount, currency_obj=currency
                    ),  # QRTL
                    "formatted_tax_group_base_amount": formatLang(
                        self.env, amounts["base_amount"], currency_obj=currency
                    ),
                    "tax_group_id": group.id,
                    "group_key": "%s-%s" % (subtotal_title, group.id),
                }
            )
        # <<< QRTL

        groups_by_subtotal[subtotal_title] = groups_vals

    # QRTL: Adjust amount_total based on tax_amount_total, in case of inconsistency.
    amount_total = amount_untaxed + tax_amount_total

    # Compute subtotals
    subtotals_list = []  # List, so that we preserve their order
    previous_subtotals_tax_amount = 0
    for subtotal_title in sorted(
        (sub for sub in subtotal_priorities), key=lambda x: subtotal_priorities[x]
    ):
        subtotal_value = amount_untaxed + previous_subtotals_tax_amount
        subtotals_list.append(
            {
                "name": subtotal_title,
                "amount": subtotal_value,
                "formatted_amount": formatLang(
                    self.env, subtotal_value, currency_obj=currency
                ),
            }
        )

        subtotal_tax_amount = sum(
            group_val["tax_group_amount"]
            for group_val in groups_by_subtotal[subtotal_title]
        )
        previous_subtotals_tax_amount += subtotal_tax_amount

    # Assign json-formatted result to the field
    return {
        "amount_total": amount_total,
        "amount_untaxed": amount_untaxed,
        "formatted_amount_total": formatLang(
            self.env, amount_total, currency_obj=currency
        ),
        "formatted_amount_untaxed": formatLang(
            self.env, amount_untaxed, currency_obj=currency
        ),
        "groups_by_subtotal": groups_by_subtotal,
        "subtotals": subtotals_list,
        "allow_tax_edition": False,
    }


def post_load_hook():
    AccountMove._get_tax_totals = _new_get_tax_totals
