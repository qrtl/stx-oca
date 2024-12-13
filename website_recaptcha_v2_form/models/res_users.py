# Copyright 2024 Quartile Limited

"""
When using this module together with the OCA module auth_signup_verify_email,
an error occurs in the _signup_create_user method stating
that g-recaptcha-response does not exist in res.users.
Additionally, it is not possible to create a g-recaptcha-response field in res.users
because Python cannot use a hyphen (-) in field names.
Therefore, this method is necessary.
Task:4999
"""

from odoo import api, models


class ResUsers(models.Model):
    _inherit = "res.users"

    @api.model
    def _signup_create_user(self, values):
        if "g-recaptcha-response" in values:
            values.pop("g-recaptcha-response")
        return super(ResUsers, self)._signup_create_user(values)
