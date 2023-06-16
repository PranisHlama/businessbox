# Copyright 2016 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from dateutil.relativedelta import relativedelta
from dateutil.rrule import MONTHLY, YEARLY
from psycopg2 import IntegrityError

from odoo import fields
from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase
from odoo.tools import mute_logger


class DateRangeTypeTest(TransactionCase):
    def setUp(self):
        super(DateRangeTypeTest, self).setUp()
        self.type = self.env["date.range.type"]
        self.company = self.env["res.company"].create({"name": "Test company"})
        self.company_2 = self.env["res.company"].create(
            {"name": "Test company 2", "parent_id": self.company.id}
        )

    def test_default_company(self):
        drt = self.type.create({"name": "Fiscal year", "allow_overlap": False})
        self.assertTrue(drt.company_id)
        # you can specify company_id to False
        drt = self.type.create(
            {"name": "Fiscal year", "company_id": False, "allow_overlap": False}
        )
        self.assertFalse(drt.company_id)

    def test_unlink(self):
        date_range = self.env["date.range"]
        drt = self.env["date.range.type"].create(
            {"name": "Fiscal year", "allow_overlap": False}
        )
        date_range.create(
            {
                "name": "FS2016",
                "date_start": "2015-01-01",
                "date_end": "2016-12-31",
                "type_id": drt.id,
            }
        )
        with self.assertRaises(IntegrityError), mute_logger("odoo.sql_db"):
            drt.unlink()

    def test_type_multicompany(self):
        drt = self.type.create(
            {"name": "Fiscal year", "company_id": False, "allow_overlap": False}
        )
        dr = self.env["date.range"].create(
            {
                "name": "FS2016",
                "date_start": "2015-01-01",
                "date_end": "2016-12-31",
                "type_id": drt.id,
                "company_id": self.company.id,
            }
        )
        drt.company_id = self.company.id
        with self.assertRaises(ValidationError):
            dr.company_id = self.company_2

    def test_autogeneration(self):
        """Ranges are autogenerated for types configured for that"""
        today = fields.Date.context_today(self.env.user)
        year_start = today.replace(day=1, month=1)
        dr_type = self.env["date.range.type"].create(
            {
                "name": __name__,
                "name_expr": "'>%s<' % date_start.strftime('%d%m%Y')",
                "unit_of_time": str(MONTHLY),
                "duration_count": 1,
                "autogeneration_count": 1,
                "autogeneration_unit": str(YEARLY),
            }
        )
        self.assertEqual(
            dr_type.range_name_preview, ">%s<" % year_start.strftime("%d%m%Y")
        )

        self.env["date.range.type"].autogenerate_ranges()
        ranges = self.env["date.range"].search(
            [("type_id", "=", dr_type.id)], order="date_start asc"
        )
        # For new types, ranges are autogenerated from the start of the year
        year_start = today.replace(day=1, month=1)
        self.assertEqual(ranges[0].date_start, year_start)
        # Ranges are autogenerated upto the range in which the computed end
        # date falls, c.q. the first of the month a year from now.
        next_year_month_start = today.replace(day=1) + relativedelta(years=1)
        self.assertEqual(ranges[-1].date_start, next_year_month_start)
        self.assertEqual(
            ranges[-1].name, ">%s<" % next_year_month_start.strftime("%d%m%Y")
        )

        # No new ranges get generated anymore this month
        self.env["date.range.type"].autogenerate_ranges()
        self.assertEqual(
            len(ranges),
            len(
                self.env["date.range"].search(
                    [("type_id", "=", dr_type.id)], order="date_start asc"
                )
            ),
        )

    def test_autogeneration_with_start_date(self):
        today = fields.Date.context_today(self.env.user)
        start_date = today.replace(year=2019, day=6, month=1)
        dr_type = self.env["date.range.type"].create(
            {
                "name": __name__,
                "name_expr": "'>%s<' % date_start.strftime('%d%m%Y')",
                "unit_of_time": str(MONTHLY),
                "duration_count": 1,
                "autogeneration_date_start": start_date,
                "autogeneration_count": 1,
                "autogeneration_unit": str(YEARLY),
            }
        )
        self.assertFalse(dr_type.date_ranges_exist)
        self.env["date.range.type"].autogenerate_ranges()
        self.assertTrue(dr_type.date_ranges_exist)
        ranges = self.env["date.range"].search(
            [("type_id", "=", dr_type.id)], order="date_start asc"
        )
        self.assertEqual(ranges[0].date_start, start_date)
        # No new ranges get generated anymore this month
        self.env["date.range.type"].autogenerate_ranges()
        self.assertEqual(
            len(ranges),
            len(
                self.env["date.range"].search(
                    [("type_id", "=", dr_type.id)], order="date_start asc"
                )
            ),
        )

    def test_autogeneration_invalid_config(self):
        """The cron method does not raise when an invalid config exists"""
        today = fields.Date.context_today(self.env.user)
        start_date = today.replace(year=2019, day=6, month=1)
        dr_type = self.env["date.range.type"].create(
            {
                "name": __name__,
                "name_expr": "index",
                "unit_of_time": str(MONTHLY),
                "duration_count": 1,
                "autogeneration_date_start": start_date,
                "autogeneration_count": 1,
                "autogeneration_unit": str(YEARLY),
            }
        )
        # Inject invalid value
        self.env.cr.execute("UPDATE date_range_type SET name_expr = 'invalid'")
        dr_type.refresh()
        with mute_logger("odoo.addons.date_range.models.date_range_type"):
            self.env["date.range.type"].autogenerate_ranges()
        self.assertFalse(dr_type.date_ranges_exist)
