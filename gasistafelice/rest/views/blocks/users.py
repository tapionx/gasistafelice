from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.core import urlresolvers

from gasistafelice.rest.views.blocks.base import BlockSSDataTables, ResourceBlockAction
from gasistafelice.consts import EDIT, CONFIRM, EDIT_MULTIPLE, VIEW

from gasistafelice.lib.shortcuts import render_to_response, render_to_xml_response, render_to_context_response

from django.contrib.auth.models import User
from gasistafelice.gas.forms.base import SingleUserForm
from django.forms.formsets import formset_factory
from gasistafelice.lib.formsets import BaseFormSetWithRequest

from flexi_auth.models import ObjectWithContext

#------------------------------------------------------------------------------#
#                                                                              #
#------------------------------------------------------------------------------#

class Block(BlockSSDataTables):

    BLOCK_NAME = "users"
    BLOCK_DESCRIPTION = _("Users")
    BLOCK_VALID_RESOURCE_TYPES = ["gas"] 

    COLUMN_INDEX_NAME_MAP = { 
        0: 'pk',
        1: 'first_name',
        2: 'last_name',
        3: 'is_active'
    }

    def _get_user_actions(self, request):

        user_actions = []

        if request.user.has_perm(EDIT, obj=ObjectWithContext(request.resource)):
            user_actions += [
                ResourceBlockAction( 
                    block_name = self.BLOCK_NAME,
                    resource = request.resource,
                    name=VIEW, verbose_name=_("Show"), 
                    popup_form=False,
                    method="get",
                ),
                ResourceBlockAction( 
                    block_name = self.BLOCK_NAME,
                    resource = request.resource,
                    name=EDIT_MULTIPLE, verbose_name=_("Edit"), 
                    popup_form=False,
                    method="get",
                ),
#                ResourceBlockAction( 
#                    block_name = self.BLOCK_NAME,
#                    resource = request.resource,
#                    name=CONFIRM, verbose_name=_("Active"), 
#                    popup_form=False,
#                ),
            ]

        return user_actions
        
    def _get_resource_list(self, request):
        # User list
        return request.resource.users

    def _get_edit_multiple_form_class(self):
        qs = self._get_resource_list(self.request)
        return formset_factory(
                    form=SingleUserForm,
                    formset=BaseFormSetWithRequest, 
                    extra=qs.count()   #0
        )

    def _get_records(self, request, querySet):
        """Return records of rendered table fields."""

        data = {}
        i = 0
        c = querySet.count()
        map_info = { }
        av = True

        for i,el in enumerate(querySet):

            key_prefix = 'form-%d' % i
            data.update({
               '%s-id' % key_prefix : el.pk, 
               '%s-pk' % key_prefix : el.pk,
               '%s-is_active' % key_prefix : bool(el.is_active),
            })

            map_info[el.pk] = {'formset_index' : i}

        data['form-TOTAL_FORMS'] = c #i 
        data['form-INITIAL_FORMS'] = c #0
        data['form-MAX_NUM_FORMS'] = 0

        formset = self._get_edit_multiple_form_class()(request, data)

        records = []
        for i, el in enumerate(querySet):

            form = formset[map_info[el.pk]['formset_index']]

            records.append({
               'id' : "%s %s" % (form['pk'], form['id']),
                'first_name' : el.first_name,
                'last_name' : el.last_name,
                'is_active' : form['is_active'],
            })

        return formset, records, {}
