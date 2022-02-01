from highcharts.views import (HighChartsMultiAxesView, HighChartsPieView,
                              HighChartsSpeedometerView, HighChartsHeatMapView, HighChartsPolarView)
from frequenze.models import StudentAttendance
from anagrafica.models import Course, DisciplinaryMeasure
from datetime import datetime, timedelta
from calendar import monthrange


class StudentsPieChartJSONView(HighChartsPieView):
    title = 'Iscritti'
    subtitle = 'Suddivisi per classe'


    @property
    def series(self):
        corsi = Course.objects.all()
        data = []

        for course in corsi:
            data.append({'name': course.name,
                         'y': course.get_students_count()})
        series = [
            {
                'name': 'Studenti',
                'colorByPoint': 'true',
                'data': data
            }
        ]
        return series

    @property
    def drilldown(self):
        drilldown = {
            'series': [
                {'id': 'emorroidi',
                 'name': 'Emorroidi',
                 'data': [
                     ['brand1', 7],
                     ['brand2', 3],
                     ['brand3', 5]
                 ]},
                {'id': 'igiene',
                 'name': 'Igiene e Bellezza',
                 'data': [
                     ['brand1', 3],
                     ['brand2', 1],
                     ['brand3', 4],
                     ['brand4', 5]
                 ]},
                {'id': 'omeopatia',
                 'name': 'Omeopatia',
                 'data': [
                     ['brand1', 3],
                     ['brand2', 1],
                     ['brand3', 4],
                     ['', 0]
                 ]}
            ]
        }
        return drilldown


class DisciplinaryMeasuresPieChartJSONView(HighChartsPieView):
    title = 'Segnalazioni'
    subtitle = 'Suddivise per classe'


    @property
    def series(self):
        corsi = Course.objects.all()
        data = []

        for course in corsi:
            data.append({'name': course.name,
                         'y': course.get_disciplinay_measures_count()})
        series = [
            {
                'name': 'Segnalazioni',
                'colorByPoint': 'true',
                'data': data
            }
        ]
        return series




class AttendancesBarJSONView(HighChartsMultiAxesView):

    title = '% Assenti'
    #subtitle = 'Assenze negli ultimi 30 giorni'
    #categories = [Course.objects.get(pk=5)]
    chart_type = ''
    chart = {'zoomType': 'xy'}
    tooltip = {'shared': 'true'}
    legend = {'layout': 'horizontal', 'align': 'left',
              'floating': 'true', 'verticalAlign': 'top',
              'y': 0, 'borderColor': '#e3e3e3'}


    @property
    def yaxis(self):
        y_axis = [
            {'gridLineWidth': 1,
             'max': 100,
             'min': 0,
             'title': False,
             'labels': {'format': '{value} %', 'style': {'color': '#666666'}},
             'opposite': 'true'}
        ]
        return y_axis

    @property
    def series(self):

        course = Course.objects.get(pk=self.kwargs['course'])
        #month = int(datetime.strftime(datetime.now(), '%m'))
        #year = int(datetime.strftime(datetime.now(), '%Y'))
        #month_lenght = monthrange(year, month)[1]
        frequencies_dict = {}
        day = datetime.now() - timedelta(21)

        frequencies_dict[course.pk] = []
        course_attendances = StudentAttendance.objects.filter(student__course__name=course,
                                                              attendance_date__gte=day)
        while day < datetime.now():
            absences = 0
            for attendance in course_attendances.filter(attendance_date__day=day.day):
                if attendance.event == 'A':
                    absences += 1

            if len(course_attendances.filter(attendance_date__day=day.day)) > 0:
                daily_attendances = int((100 * absences) / len(course_attendances.filter(attendance_date__day=day.day)))
            else:
                daily_attendances = 0
            if course_attendances.filter(attendance_date__day=day.day):
                frequencies_dict[course.pk].append([day.strftime('%d/%m'), daily_attendances])
            day += timedelta(1)

        series = [
            {
                'enableMouseTracking': False,
                'name': course.name,
                'dataLabels': {'enabled': True,
                               'format': '{y}%',
                               'padding': 15,
                               },
                'type': 'spline',
                'data': frequencies_dict[course.pk],
                'color': '#f69e4e'
            }
        ]
        return series

class GeneralAttendancesBarJSONView(HighChartsMultiAxesView):

    title = '% Assenti'
    #subtitle = 'Assenze negli ultimi 30 giorni'
    #categories = [Course.objects.get(pk=5)]
    chart_type = ''
    chart = {'zoomType': 'xy'}
    tooltip = {'shared': 'true'}
    legend = {'layout': 'horizontal', 'align': 'left',
              'floating': 'true', 'verticalAlign': 'top',
              'y': 0, 'borderColor': '#e3e3e3'}


    @property
    def yaxis(self):
        y_axis = [
            {'gridLineWidth': 1,
             'max': 100,
             'min': 0,
             'title': False,
             'labels': {'format': '{value} %', 'style': {'color': '#666666'}},
             'opposite': 'true'}
        ]
        return y_axis

    @property
    def series(self):

        #month = int(datetime.strftime(datetime.now(), '%m'))
        #year = int(datetime.strftime(datetime.now(), '%Y'))
        #month_lenght = monthrange(year, month)[1]
        day = datetime.now() - timedelta(21)

        frequencies = []
        course_attendances = StudentAttendance.objects.filter(attendance_date__gte=day)

        while day < datetime.now():
            absences = 0
            for attendance in course_attendances.filter(attendance_date__day=day.day):
                if attendance.event == 'A':
                    absences += 1

            if len(course_attendances.filter(attendance_date__day=day.day)) > 0:
                daily_attendances = int((100 * absences) / len(course_attendances.filter(attendance_date__day=day.day)))
            else:
                daily_attendances = 0
            if course_attendances.filter(attendance_date__day=day.day):
                frequencies.append([day.strftime('%d/%m'), daily_attendances])
            day += timedelta(1)

        series = [
            {
                'enableMouseTracking': False,
                'name': 'Studenti di tutte le classi',
                'dataLabels': {'enabled': True,
                               'format': '{y}%',
                               'padding': 15,
                               },
                'type': 'spline',
                'data': frequencies,
                'color': '#f69e4e'
            }
        ]
        return series
