from django.utils.translation import ugettext as _, ugettext_lazy
from django.contrib.auth.views import login as django_auth_login
from django.core.exceptions import PermissionDenied
from django.shortcuts import render_to_response
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django.conf import settings
from django.contrib import messages
from django.core import urlresolvers
from django.http import HttpResponseRedirect, HttpResponse
from gasistafelice.des.forms import DESRegistrationForm, DESStaffRegistrationForm
from gasistafelice.des.models import Siteattr

from registration.models import RegistrationProfile
import re

@never_cache
def login(request, *args, **kw):

    kw['extra_context'] = {
        'VERSION': settings.VERSION,
        'THEME' : settings.THEME,
        'MEDIA_URL' : settings.MEDIA_URL,
        'ADMIN_MEDIA_PREFIX' : settings.ADMIN_MEDIA_PREFIX,
        'MAINTENANCE_MODE' : settings.MAINTENANCE_MODE
    }
    if settings.MAINTENANCE_MODE: 
        if request.method == "POST" and \
            request.POST.get('username') != settings.INIT_OPTIONS['su_username']:
            return HttpResponse(_("Maintenance in progress, please retry later..."))

    return django_auth_login(request, *args, **kw)

@csrf_protect
@never_cache
def registration(request, *args, **kw):

    form_class = DESRegistrationForm
    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, "Ti sei registrato con successo, \
                attendi l'abilitazione del GAS e poi potrai accedere al sistema"
            )
            return HttpResponseRedirect(settings.LOGIN_URL)
    else:
        form = form_class()

    context = {
        'registration_form' : form,
        'VERSION': settings.VERSION,
        'THEME' : settings.THEME,
        'MEDIA_URL' : settings.MEDIA_URL,
        'ADMIN_MEDIA_PREFIX' : settings.ADMIN_MEDIA_PREFIX
    }

    return render_to_response("registration/register.html", context,
                              context_instance=RequestContext(request)
    )

@csrf_protect
@never_cache
def staff_registration(request, *args, **kw):
    """This view is used by staff that wants to register new users
    without using the email confirmation procedure.

    """
    des = Siteattr.get_site()

    if request.user in des.admins | des.gas_tech_referrers:

        form_class = DESStaffRegistrationForm
        if request.method == "POST":
            form = form_class(request.POST)
            if form.is_valid():
                form.save()
                messages.info(request, "Complimenti o tecnico! Hai registrato un nuovo utente :)")
                return HttpResponseRedirect(settings.LOGIN_URL)
        else:
            form = form_class()

        context = {
            'registration_form' : form,
            'VERSION': settings.VERSION,
            'THEME' : settings.THEME,
            'MEDIA_URL' : settings.MEDIA_URL,
            'ADMIN_MEDIA_PREFIX' : settings.ADMIN_MEDIA_PREFIX
        }

        return render_to_response("registration/staff_register.html", context,
                                  context_instance=RequestContext(request)
        )

    else:
        return django_auth_login(request, *args, **kw)

# Activate user function which update RegistrationProfile activation key, 
# but doesn't activate the user

SHA1_RE = re.compile('^[a-f0-9]{40}$')
def activate_user(activation_key):

    model = RegistrationProfile

    if SHA1_RE.search(activation_key):
        try:
            profile = model.objects.get(activation_key=activation_key)
        except model.DoesNotExist:
            return False
        if not profile.activation_key_expired():
            profile.activation_key = model.ACTIVATED
            profile.save()
            return profile.user
    return False
    
    
# Function copied from registration.views app
# Use custom function to update activation key for a user
# but does not activate it

def activate(request, activation_key,
             template_name='registration/activate.html',
             extra_context=None):

    activation_key = activation_key.lower() # Normalize before trying anything with it.
    account = activate_user(activation_key)

    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    return render_to_response(template_name,
        { 'account': account,
          'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS },
        context_instance=context
    )
