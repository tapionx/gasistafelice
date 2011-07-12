from django.db import models

from django.utils.translation import ugettext_lazy as _

from permissions.models import Role
from permissions import PermissionBase # mix-in class for permissions management

from gasistafelice.base.fields import CurrencyField
from gasistafelice.base.models import Resource, Person

from django.db import models
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

    #TODO: This is the basis of the economic part. To discuss and extend
    balance = CurrencyField(default=Decimal("0"))
    #COMMENT: DecimalField --> 84 table on MySQL FloatField --> 84 table
    #COMMENT fero: what does this mean?

    def __unicode__(self):
        #FIXME: Caught TypeError while rendering: coercing to Unicode: need string or buffer, Decimal found
        #return self.balance
        return _("%(balance)s") % {'balance' : self.balance}

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
    """
    #TODO: This is the basis of the economic part. To discuss and extend
    account = models.ForeignKey(Account)
    amount = CurrencyField()
    causal = models.CharField(max_length=512, help_text=_("causal of economic movement"))    

    def __unicode__(self):
        return _("%(amount)s (causal: %(causal)s)") % {'amount' : self.amount, 'causal' : self.causal}