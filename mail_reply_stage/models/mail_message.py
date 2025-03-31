# Copyright 2025 Quartile (https://www.quartile.co)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import api, models


class MailMessage(models.Model):
    _inherit = "mail.message"

    @api.model_create_multi
    def create(self, values_list):
        messages = super().create(values_list)
        for message in messages:
            user = message.author_id.user_ids[:1]
            if user and user.has_group("base.group_user"):
                continue
            if message.subtype_id and message.subtype_id.internal:
                continue
            res_model = (
                self.env["ir.model"]
                .sudo()
                .search([("model", "=", message.model)], limit=1)
            )
            if not res_model:
                continue
            resource = self.env[message.model].browse(message.res_id)
            config_records = self.env["mail.reply.config"].search(
                [("model_id", "=", res_model.id)]
            )
            matched_config = None
            parent_field_rec = None
            for config in config_records:
                if config.parent_field_id:
                    parent_field_rec = getattr(
                        resource, config.parent_field_id.name, None
                    )
                    if (
                        parent_field_rec
                        and getattr(parent_field_rec, "name", None)
                        == config.parent_field_value
                    ):
                        matched_config = config
                        break
                else:
                    matched_config = config
            if not matched_config:
                continue
            current_stage = getattr(
                resource, matched_config.reply_stage_field_id.name, None
            )
            if current_stage == matched_config.remain_stage:
                continue
            reply_stage_rec = self.env[
                matched_config.reply_stage_field_id.relation
            ].search([("name", "=", matched_config.reply_stage)])
            if matched_config.parent_stage_field_id:
                allowed_stages = getattr(
                    parent_field_rec,
                    matched_config.parent_stage_field_id.name,
                    self.env[matched_config.parent_stage_field_id.relation],
                )
                reply_stage_rec = reply_stage_rec.filtered(
                    lambda stage: stage in allowed_stages
                )
            if reply_stage_rec:
                resource.sudo().write(
                    {matched_config.reply_stage_field_id.name: reply_stage_rec.id}
                )
        return messages
