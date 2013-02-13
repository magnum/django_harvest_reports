


from django.db.models import Q
from django.shortcuts import redirect
from django.http import *

from django.views.generic import ListView,UpdateView,RedirectView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.cache import params

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib import messages
from django.core.urlresolvers import reverse

import os
import json
from datetime import datetime, timedelta
from harvest import Harvest


def worked_hours(request):
    h = Harvest( os.environ['HARVEST_URL'], os.environ['HARVEST_USERNAME'], os.environ['HARVEST_PASSWORD'] )
    users = (
        {'firstname': 'Luca', 'lastname': 'Bravo', 'hours': 0},
        {'firstname': 'Antonio', 'lastname': 'Molinari', 'hours': 0},
    )
    for u in users:
        user = h.find_user( u['firstname'], u['lastname'] )
    	if user:
            start = datetime.today()
            end = start + timedelta(7)
            total = 0
            for entry in user.entries( start, end ):
                    total += entry.hours
            u['hours'] = total


    #return HttpResponse('Reports')   
    return render_to_response('worked_hours.html', {
            'version': 1,
            'users': users,
        },
        RequestContext(request)
    )