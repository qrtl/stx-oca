# © 2011 Akretion Sébastien BEAU <sebastien.beau@akretion.com>
# © 2013 Camptocamp SA (author: Guewen Baconnier)
# © 2016 Sodexis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    workflow_process_id = fields.Many2one(
        comodel_name="sale.workflow.process",
        string="Sale Workflow Process",
        copy=False,
    )
