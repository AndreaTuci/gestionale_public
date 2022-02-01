from django import forms
from .models import Classroom, Company, Convention, Course, CourseType, DisciplinaryMeasure, \
    Sector, Staff, Stage, Student, TrainingUnit, Communication
from django.forms import SelectDateWidget


class DateInput(forms.DateInput):
    input_type = 'date'

    #template_name = 'utils/date.html'


class ClassroomModelForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = "__all__"


class CommunicationCourseModelForm(forms.ModelForm):

    class Meta:
        model = Communication
        exclude = ['student', 'read_by_family', 'date_of_reading']
        widgets = {
            'created_at': forms.SelectDateWidget
        }
        labels = {
           'created_at': 'Data della comunicazione',
        }


class CompanyModelForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = "__all__"
        widgets = {
            'chief_legal_birth': DateInput,
        }


class CompanyUpdateModelForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = "__all__"



class ConventionModelForm(forms.ModelForm):
    class Meta:
        model = Convention
        fields = "__all__"
        widgets = {
            'date': DateInput,
        }


class ConventionUpdateModelForm(forms.ModelForm):
    class Meta:
        model = Convention
        fields = "__all__"


class CourseModelForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = "__all__"
        widgets = {
            'start_date': DateInput,
            'expected_end_date': DateInput,
            'actual_end_date': DateInput,
        }


class CourseUpdateModelForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = "__all__"


class CourseTypeModelForm(forms.ModelForm):
    class Meta:
        model = CourseType
        fields = "__all__"


class DisciplinaryMeasureModelForm(forms.ModelForm):
    tutor_reporting = forms.ModelChoiceField(queryset=Staff.objects.filter(task="T"), label="Tutor")
    teacher_reporting = forms.ModelChoiceField(required=False,queryset=Staff.objects.filter(task="D"), label="Docente")

    def __init__(self, *args, **kwargs):
        super(DisciplinaryMeasureModelForm, self).__init__(*args, **kwargs)
        self.fields['students'].queryset = Student.objects.filter(is_withdrawn=False)

    class Meta:
        model = DisciplinaryMeasure
        fields = "__all__"

        widgets = {
            'reporting_date': DateInput,
        }


class DisciplinaryMeasureCourseModelForm(forms.ModelForm):
    tutor_reporting = forms.ModelChoiceField(queryset=Staff.objects.filter(task="T"), label="Tutor")
    teacher_reporting = forms.ModelChoiceField(queryset=Staff.objects.filter(task="D"), label="Docente")

    def __init__(self, *args, **kwargs):
        super(DisciplinaryMeasureCourseModelForm, self).__init__(*args, **kwargs)
        self.fields['students'].queryset = Student.objects.filter(is_withdrawn=False)

    class Meta:
        model = DisciplinaryMeasure
        fields = "__all__"

        widgets = {
            'reporting_date': DateInput,
        }


class DisciplinaryMeasureUpdateModelForm(forms.ModelForm):
    tutor_reporting = forms.ModelChoiceField(queryset=Staff.objects.filter(task="T"), label="Tutor")
    teacher_reporting = forms.ModelChoiceField(required=False, queryset=Staff.objects.filter(task="D"), label="Docente")

    def __init__(self, *args, **kwargs):
        super(DisciplinaryMeasureUpdateModelForm, self).__init__(*args, **kwargs)
        self.fields['students'].queryset = Student.objects.filter(is_withdrawn=False)

    class Meta:
        model = DisciplinaryMeasure
        fields = "__all__"


class SectorModelForm(forms.ModelForm):
    class Meta:
        model = Sector
        fields = "__all__"


class CreateStaffModelForm(forms.ModelForm):

    class Meta:
        model = Staff
        exclude = ['user', 'active', 'badge']
        widgets = {
            'date_of_birth': DateInput(),
            'contract_expiration': DateInput(),
        }

class UpdateStaffModelForm(forms.ModelForm):

    class Meta:
        model = Staff
        exclude = ['user', 'active', 'task', 'badge']
        widgets = {
            'date_of_birth': forms.DateInput,
            'contract_expiration': forms.DateInput,
        }

class UpdateAdminStaffModelForm(forms.ModelForm):

    class Meta:
        model = Staff
        fields = ['active', 'task']



# class StageConventionModelForm(forms.ModelForm):

#   class Meta:
#      model = StageConvention
#     fields = "__all__"
#    widgets = {
#       'date' : DateInput,
#      'begin': DateInput,
#     'end': DateInput,
#    'return_day_one': DateInput,
#   'return_day_two': DateInput,
#  'return_day_three': DateInput,
# }

class StageModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(StageModelForm, self).__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.filter(is_finished=False)

    class Meta:
        model = Stage
        fields = '__all__'
        widgets = {
            'start_date': DateInput,
            'end_date': DateInput,
            'medical_examination_date': DateInput,
            'medical_examination_renoval_date': DateInput,
            'safety_certificate_date': DateInput
        }

class StageUpdateModelForm(forms.ModelForm):
    class Meta:
        model = Stage
        fields = '__all__'


class StudentModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(StudentModelForm, self).__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.filter(is_finished=False)

    class Meta:
        model = Student
        fields = "__all__"
        widgets = {
            'date_of_birth': DateInput,
            'registration_date': DateInput,
            'withdrawal_date': DateInput,
            'qualification_date': DateInput,
        }

        labels = {
            'photo': 'Fotografia',
        }



class StudentUpdateModelForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = "__all__"

    labels = {
        'photo': 'Fotografia',
    }
# class TeacherModelForm(forms.ModelForm):

#   class Meta:
#      model = Teacher
#     fields = "__all__"
#    widgets = {
#       'date_of_birth': DateInput,
#      'contract_expiration': DateInput,
# }


class TrainingUnitModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TrainingUnitModelForm, self).__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.filter(is_finished=False)


    class Meta:
        model = TrainingUnit
        fields = "__all__"


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()
