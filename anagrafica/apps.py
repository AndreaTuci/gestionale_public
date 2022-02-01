from django.apps import AppConfig
from django.db.models.signals import post_save, pre_save
from django.core.signals import request_finished

class AnagraficaConfig(AppConfig):
    name = 'anagrafica'

   # def ready(self):
   #     from frequenze.models import TeacherAttendance
   #     from anagrafica.signals import my_callback
   #     pre_save.connect(my_callback, sender=TeacherAttendance)
