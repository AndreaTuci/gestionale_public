from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, Group
from django.core.management import call_command
from django.test import TestCase, RequestFactory
from django.test.client import Client
from django.urls import reverse
from anagrafica.views import TeacherListView
from anagrafica.models import Staff
import environ

# Lancia i test con python -W ignore::RuntimeWarning manage.py test
# Per evitare warning sulla data di Wharehouse.last_movement

# Esempio di fixture
# python manage.py dumpdata anagrafica --indent=4 --output=anagrafica_dump.json

env = environ.Env()
environ.Env.read_env()


def load_data_commands():
    call_command('loaddata', 'groups.json', verbosity=0)
    call_command('loaddata', 'users.json', verbosity=0)
    call_command('loaddata', 'anagrafica_dump.json', verbosity=0)


class LogInTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.client.login(username=env('SUPERADMIN_NAME'), password=env('SUPERADMIN_PW'))
        load_data_commands()

    def test_teacher_list_view(self):
        request = RequestFactory().get(reverse('teacher-agreement-list'))
        view = TeacherListView()
        view.setup(request)
        context = view.get_context_data()
        self.assert_(context['teacher_list'].last())
        self.assert_(context['backoffice'].last())


class StaffModelTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.client.login(username=env('SUPERADMIN_NAME'), password=env('SUPERADMIN_PW'))
        self.user = env('SUPERADMIN_NAME')
        load_data_commands()
        self.staff_super_user = Staff.objects.get(user__username=self.user)

    def test_model_exists(self):
        assert self.staff_super_user.name == 'Andrea'

    def test_model_methods(self):
        self.assertEqual(self.staff_super_user.get_absolute_url(), '/anagrafica/staff/1/')
        self.assertEqual(self.staff_super_user.generate_badge_code(), 'ATT0ATTnuu1ATTnuudct2ATTN')
        self.assertEqual(self.staff_super_user.__str__(), 'Tuci Andrea')
