from anagrafica.models import Staff
from django.shortcuts import redirect
from django.urls import reverse
from urllib.parse import urlencode


from django.shortcuts import redirect
from django.core.mail import send_mail
from django.template.loader import render_to_string
from anagrafica.models import Staff

def first_access(backend, user, response, *args, **kwargs):
    for person in Staff.objects.all():
        profile = person.user.email
        if profile == response['email']:
            return
    base_url = reverse('first-access')
    query_string = urlencode({'user_bound': kwargs['username']})
    url = '{}?{}'.format(base_url, query_string)
    return redirect(url)



def send_bug_mail(request):
    sender = request.user
    host_text = request.get_full_path()

    send_mail(
        subject='Utente ' + str(sender) + " - Segnalazione bug",
        from_email='a.tuci@cfpdonfacibeni.org',
        recipient_list=['tuci.registrazioni@gmail.com'],
        message=str(sender) + ' segnala un bug alla pagina ' + host_text,
        html_message=render_to_string('bug_mail.html', {'profile':sender, 'host': host_text})
    )

def send_activation_mail(request, profile):
    sender = Staff.objects.get(user=profile)
    host_text="https://" + str(request.get_host()) + str(redirect('staff-activate', sender.pk).url)

    send_mail(
        subject='Utente ' + str(sender) + " - Richiesta di attivazione",
        from_email='a.tuci@cfpdonfacibeni.org',
        recipient_list=['tuci.registrazioni@gmail.com'],
        message=str(sender) + ' vuole attivare il suo profilo',
        html_message=render_to_string('mail.html', {'profile':sender, 'host': host_text})
    )