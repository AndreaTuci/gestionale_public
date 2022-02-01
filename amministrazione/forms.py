from django import forms
from .models import *
from django.forms import SelectDateWidget


class DateInput(forms.DateInput):
    input_type = 'date'

    #template_name = 'utils/date.html'


class TeacherAgreementModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TeacherAgreementModelForm, self).__init__(*args, **kwargs)
        year = datetime.strftime(datetime.now(), '%Y')
        date_time_obj = datetime.strptime(f'01/09/{year}', '%d/%m/%Y')
        self.fields['school_year'].initial = f'{year}/{int(year)+1}'
        self.fields['date'].initial = f'01/09/{year}'
        self.fields['start_date'].initial = f'01/09/{year}'
        self.fields['end_date'].initial = f'30/06/{int(year)+1}'

    class Meta:
        model = TeacherAgreement
        fields = "__all__"


class NewProductMovementModelForm(forms.ModelForm):
    class Meta:
        model = Movement
        exclude = ['product', 'movement_type']

class MovementModelForm(forms.ModelForm):
    class Meta:
        model = Movement
        exclude = ['product']

class NewProductModelForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        exclude = ['barcode', 'quantity']
