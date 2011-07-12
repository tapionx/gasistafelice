from django.utils.translation import ugettext, ugettext_lazy as _

# FIXME: strong application coupling !
ACCOUNT_TYPES = [
    ('ROOT', _('Root account')),
    ('INCOME', _('Incomes')),
    ('EXPENSE', _('Expenses')),
    ('ASSET', _('Asset')),
    ('LIABILITY', _('Liability')),
    ('INVOICES', _('Invoices')),
]

TRANSACTION_TYPES = [
    ('SUPPLIER_ORDER_PAYMENT', _('Payment of an order to a supplier')),
    ('RECHARGE', _('Recharge of a GAS member account')),
    ('GASMEMBER_ORDER_PAYMENT', _('Payment of an order from a GAS member')),
    ('MEMBERSHIP_FEE_PAYMENT', _('Payment of a membership fee')),   
]