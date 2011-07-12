from django.db import models

from django.utils.translation import ugettext_lazy as _

from permissions.models import Role
from permissions import PermissionBase # mix-in class for permissions management

from gasistafelice.base.fields import CurrencyField
from gasistafelice.base.models import Subject

from consts import ACCOUNT_TYPES, TRANSACTION_TYPES

from datetime import datetime
from decimal import Decimal

class Account(models.Model):
    """
    An account within a double-entry accounting system.
    
    From an abstract point of view, there are two general kind of accounts:
    1) those which are stocks of money, either positive (assets) or negative (liabilities)
    2) those which represent entry-points in the system (e.g incomes) or exit-points (e.g. expenses) from it   
    
    As a data stucture, an account is just a collection of transactions
    between either two accounts in the system  or an account in the system
    and one outside it. 
    
    Accounts are hierarchically organized in a tree-like structure, 
    and are owned by somebody.  
    
    An account can be merely a placeholder (just a container of subaccounts, no transactions).  
    """
    
    parent = models.ForeignKey('Account')
    name = models.CharField(max_length=128)
    type = models.CharField(max_length=128, choices=ACCOUNT_TYPES)
    placeholder = models.BooleanField(default=False)
    owner = models.ForeignKey(Subject)
    
    @property
    def balance(self):
        """The balance of this account (as a signed Decimal number)."""
        raise NotImplementedError 
    
    @property
    def path(self):
        """
        The tree path needed to reach this account from the root of the account system,
        in the form 'root:account:subaccount:...' .
        """
        raise NotImplementedError 
    
    
    @property
    def root(self):
        """The root account for the account system this account belongs to."""
        raise NotImplementedError 
    
    
    def __unicode__(self):
        return _("Account %(path)s of the system owned by %(subject)s") % {'path':self.path, 'subject':self.root.owner}

class Transaction(models.Model):
    """
    A transaction within a double-entry accounting system.
    
    From an abstract point of view, a transaction is a just a money flow between two accounts, 
    of which at least one is internal to the system.     
    
    A transaction can etiher increase/decrease the amount of money globally contained within the system,
    or just represent a transfer between system stocks. 
    
    A transaction is characterized at least by:
    * a source account
    * a destination/target account
    * the amount of money transferred from/to both directions
    * the date when it happened
    * a reason for the transfer
    * who autorized the transaction 
    """

    # source account for the transaction
    source = models.ForeignKey(Account, related_name='outgoing_transaction_set')
    # target account for the transaction
    destination = models.ForeignKey(Account, related_name='incoming_transaction_set')
    # A transaction can have a plus- and minus- part, or both
    plus_amount = CurrencyField(blank=True, null=True)
    minus_amount = CurrencyField(blank=True, null=True)
    # given the transaction type, some fields can be auto-set (e.g. source/destination account)
    type = models.CharField(max_length=128, choices=TRANSACTION_TYPES)
    # when the transaction happened
    date = models.DateTimeField(default=datetime.now)
    # what the transaction represents
    description = models.CharField(max_length=512, help_text=_("Reason of the transaction"))
    # who triggered the transaction
    issuer = models.ForeignKey(Subject)     

    def __unicode__(self):
        return _("%(type)s issued by %(issuer)s at %(date)s") % {'type' : self.type, 'issuer' : self.issuer, 'date' : self.date}