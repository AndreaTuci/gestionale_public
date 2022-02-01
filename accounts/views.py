
from django.contrib.auth.models import User
from anagrafica.models import Staff
from django.db.models import Q
from django.contrib.postgres.search import SearchVector
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404


@login_required
def user_profile_view(request, pk):
    context = {}
    user = get_object_or_404(User, pk=pk)
    #spec = user.profile.specialization.all()
    if request.user.pk == user.pk:
        context["profile"] = user
        #context['specialization'] = spec

    else:
        context["profile"] = "invalid_profile"
    return render(request, "accounts/user_profile.html", context)
