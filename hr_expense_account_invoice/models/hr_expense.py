# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _


class HrExpenseSheet(models.Model):
    _inherit = 'hr.expense.sheet'

    account_invoice_ids = fields.Many2many("account.voucher", string="Included invoices")
    total_invoiced_amount = fields.Float(string='Total Invoced Amount', store=True, compute='_compute_invoiced_amount', digits=dp.get_precision('Account'))

    @api.one
    @api.depends('account_invoice_ids')
    def _compute_invoiced_amount(self):
        total_amount = 0.0
        for inv in self.account_invoice_ids:
            total_amount += inv.currency_id.with_context(
                date=inv.date,
                company_id=inv.company_id.id
            ).compute(inv.amount, inv.currency_id)
        self.total_invoiced_amount = total_amount


class AccountVoucher(models.Model):
    _inherit = 'account.voucher'

    employee_id = fields.Many2one('hr.employee', string="Employee", required=True, readonly=True, states={'submit': [('readonly', False)]}, default=lambda self: self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1))
