# Copyright 2025 Quartile (https://www.quartile.co)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class MailReplyStage(models.Model):
    _name = "mail.reply.config"

    model_id = fields.Many2one(
        "ir.model", string="Model", required=True, ondelete="cascade"
    )
    parent_field_id = fields.Many2one(
        "ir.model.fields",
        string="Parent Field",
        domain="[('model_id', '=', model_id), ('ttype', '=', 'many2one')]",
        ondelete="cascade",
    )
    parent_model_name = fields.Char(
        related="parent_field_id.relation",
        string="Parent Model",
        store=True,
        help="Automatically stores the model name of the related parent entity.",
    )
    parent_stage_field_id = fields.Many2one(
        "ir.model.fields",
        string="Parent Stage Field",
        domain="[('model_id.model', '=', parent_model_name), ('ttype', '=', 'many2many')]",
        ondelete="cascade",
        help="A Many2Many field within the parent model that defines "
        "valid stages for this configuration.",
    )
    parent_field_value = fields.Char(
        help="The specific value of the parent field that this configuration applies to. "
        "For example, a project name."
    )
    reply_stage_field_id = fields.Many2one(
        "ir.model.fields",
        domain="[('model_id', '=', model_id), ('ttype', '=', 'many2one')]",
        required=True,
        ondelete="cascade",
    )
    reply_stage = fields.Char(
        required=True,
        help="This stage of record will be changed when a non-internal user "
        "replies to the record.",
    )
    remain_stage = fields.Char(
        string="No Reply Stage",
        required=True,
        help="Record in this stage will not update to the mail reply stage "
        "when a non-internal user replies to the record.",
    )

    @api.onchange("model_id")
    def _onchange_model_id(self):
        self.reply_stage_field_id = False

    @api.onchange("reply_stage_field_id")
    def _onchange_reply_stage_field_id(self):
        self.reply_stage = False
        self.remain_stage = False
