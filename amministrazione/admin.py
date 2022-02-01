from django.contrib import admin
from amministrazione.models import *


class TimecardEntryModelAdmin(admin.ModelAdmin):
    model = TimeCardEntry
    list_filter = ["employee", 'entry_date']

class TeacherAgreementModelAdmin(admin.ModelAdmin):
    model = TeacherAgreement
    list_filter = ["training_unit__course", 'employee']

admin.site.register(TimeCardEntry, TimecardEntryModelAdmin)
admin.site.register(TeacherAgreement, TeacherAgreementModelAdmin)
admin.site.register(Warehouse)
admin.site.register(Movement)
admin.site.register(Order)
