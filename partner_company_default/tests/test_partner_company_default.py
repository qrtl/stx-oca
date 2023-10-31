# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import odoo.tests.common as common


class TestPartnerCompanyDefault(common.TransactionCase):
    def setUp(self):
        super(TestPartnerCompanyDefault, self).setUp()

    def test_partner_company_default(self):
        user = self.env["res.users"].create(
            {
                "name": "Test User",
                "login": "Test User",
                "email": "test@yourcompany.com",
                "groups_id": [
                    (
                        6,
                        0,
                        [
                            self.env.ref("base.group_system").id,
                            self.env.ref("base.group_partner_manager").id,
                        ],
                    )
                ],
            }
        )

        # Test created partner company
        partner = (
            self.env["res.partner"]
            .with_user(user.id)
            .create({"name": "Test Partner 1"})
        )
        self.assertEqual(partner.company_id, user.company_id)

        # Test partners of multi company
        company_fr = (
            self.env["res.company"]
            .with_user(user.id)
            .create(
                {
                    "name": "French company",
                    "currency_id": self.env.ref("base.EUR").id,
                    "country_id": self.env.ref("base.fr").id,
                }
            )
        )
        self.assertFalse(company_fr.partner_id.company_id)

        user.company_ids = [(4, company_fr.id)]
        user.company_id = company_fr.id
        partner = (
            self.env["res.partner"]
            .with_user(user.id)
            .create({"name": "Test Partner 2"})
        )

        self.assertEqual(partner.company_id, company_fr)
