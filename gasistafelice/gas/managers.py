from django.db import models
from django.contrib.auth.models import User

class GASMembersManager(models.Manager):

    def have_role(self, parametric_role):
        return self.get_query_set().filter(person__user_principal_param_role_set__in=[parametric_role], gas=parametric_role.gas)

    def have_roles(self, parametric_roles):
        qs = self.get_query_set().none()
        for p in parametric_roles:
            qs = qs | self.have_role(p)
        return qs

    def tech_referrers(self, **resource_kw):
        parametric_roles = ParamRole.objects.gas_tech_referrers(**resource_kw)
        return self.have_roles(parametric_roles)

    def cash_referrers(self):
        parametric_roles = ParamRole.objects.gas_cash_referrers(**resource_kw)
        return self.have_roles(parametric_roles)

    def supplier_referrers(self):
        parametric_roles = ParamRole.objects.gas_supplier_referrers(**resource_kw)
        return self.have_roles(parametric_roles)

    def delivery_referrers(self):
        parametric_roles = ParamRole.objects.gas_delivery_referrers(**resource_kw)
        return self.have_roles(parametric_roles)


