from django import forms
from anagrafica.models import Staff, Student, Communication
from captcha.fields import CaptchaField

class DateInput(forms.DateInput):
    input_type = 'date'
    template_name = 'utils/date.html'


class CommunicationCourseModelForm(forms.ModelForm):

    class Meta:
        model = Communication
        fields = '__all__'
        #widgets = {
        #    'note_text': forms.Textarea
        #}
        #labels = {
        #    'solved': 'Situazione risolta [Archivia nota]',
        # }


class CreateStudentUserForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ['course']


class FirstAccessModelForm(forms.ModelForm):
    captcha = CaptchaField(label='Captcha: scrivi nella casella le lettere che leggi nell`immagine')

    class Meta:
        model = Staff
        exclude = ['user', 'active', 'curriculum', 'INPS', 'IRPEF', 'badge']

        labels = {'avatar': 'Foto:'}
        widgets = {
            'task': forms.Select(attrs={'id':'taskID'}),
            #'specialization': forms.SelectMultiple(attrs={'id': 'specializationID'}),
            'date_of_birth': DateInput,
            'contract_expiration': DateInput,
        }
