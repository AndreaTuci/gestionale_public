import csv
import io
from functools import reduce
import datetime
from collections import OrderedDict
from .models import Student, Course
import locale
from datetime import datetime as date
from django.contrib.auth.models import Group
from django.core.serializers.json import DjangoJSONEncoder
from openpyxl import load_workbook
from anagrafica.models import Company, Sector
import sys

locale.setlocale(locale.LC_ALL, 'it_IT.utf8')


def copy_spreadsheet(spreadsheet, sector):
    wb = load_workbook(spreadsheet)
    rows = {}
    copy_error = []
    if sector == '1':
        sheet = wb.worksheets[0]
        for rowOfCellObjects in sheet['B3':'I282']:
            row_name = rowOfCellObjects[0].value
            rows[row_name] = {
                'Nome': rowOfCellObjects[0].value,
                'Indirizzo': rowOfCellObjects[1].value,
                'Telefono': rowOfCellObjects[2].value,
                'Cel': rowOfCellObjects[4].value,
                'Referente': rowOfCellObjects[5].value,
                'Mail': rowOfCellObjects[6].value,
                'Zona/Comune': rowOfCellObjects[7].value,
            }

        for key in rows:
            try:

                telephone = str(rows[key]['Telefono']) + ' ' + str(rows[key]['Cel'])
                Company.objects.create(
                    sector=Sector.objects.get(sector_name='Elettricista'),
                    name=rows[key]['Nome'],
                    registered_office_city=rows[key]['Zona/Comune'],
                    registered_office_address=rows[key]['Indirizzo'],
                    telephone=telephone,
                    email = rows[key]['Mail'],
                    company_contact = rows[key]['Referente'],
                )
            except BaseException:
                print("Errore per: ", rows[key], ' ', str(sys.exc_info()[1]))
                copy_error.append("Errore per: " + rows[key]['Nome'] + ' ' + str(sys.exc_info()[1]))

    elif sector == '2':
        sheet = wb.worksheets[1]
        for rowOfCellObjects in sheet['B3':'I562']:
            row_name = rowOfCellObjects[0].value
            rows[row_name] = {
                'Nome': rowOfCellObjects[0].value,
                'Indirizzo': rowOfCellObjects[1].value,
                'Telefono': rowOfCellObjects[2].value,
                'Cel': rowOfCellObjects[4].value,
                'Referente': rowOfCellObjects[5].value,
                'Mail': rowOfCellObjects[6].value,
                'Zona/Comune': rowOfCellObjects[7].value,

            }

        for key in rows:
            try:

                telephone = str(rows[key]['Telefono']) + ' ' + str(rows[key]['Cel'])
                Company.objects.create(
                    sector=Sector.objects.get(sector_name='Idraulico'),
                    name=rows[key]['Nome'],
                    registered_office_city=rows[key]['Zona/Comune'],
                    registered_office_address=rows[key]['Indirizzo'],
                    telephone=telephone,
                    email = rows[key]['Mail'],
                    company_contact = rows[key]['Referente'],
                )
            except BaseException:
                print("Errore per: ", rows[key], ' ', str(sys.exc_info()[1]))
                copy_error.append("Errore per: " + rows[key]['Nome'] + ' ' + str(sys.exc_info()[1]))

        return copy_error

class Dictionary(dict):

    def new(self, key, value):
        self[key] = value

    def sum(self, key, attribute, value):
        self[key][attribute] += value

    def add_attribute(self, key, attribute, value):
        self[key][attribute] = value

    def add_value(self, key, value):
        self[key] = value


def get_from_dict(data_dict, map_list):
    """Iterate nested dictionary"""
    return reduce(dict.get, map_list, data_dict)


def csv_regione_toscana_reader(csv_file, course):
    csv_encoded = encode_csv_regione_toscana(csv_file)

    for record in csv_encoded:
        Student.objects.create(
            name=csv_encoded[record]['name'],
            surname=csv_encoded[record]['surname'],
            date_of_birth=csv_encoded[record]['date_of_birth'],
            place_of_birth=csv_encoded[record]['place_of_birth'],
            resident_in_city=csv_encoded[record]['resident_in_city'],
            resident_in_address=csv_encoded[record]['resident_in_address'],
            postal_code=csv_encoded[record]['postal_code'],
            fiscal_code=csv_encoded[record]['fiscal_code'],
            parent_email_1=csv_encoded[record]['parent_email_1'],
            parent_telephone_1=csv_encoded[record]['parent_telephone_1'],
            course=course,
            number=csv_encoded[record]['number'],
            registration_date=csv_encoded[record]['registration_date'],
        )
    return csv_encoded


def csv_reader(csv_file):

    csv_encoded = encode_csv(csv_file)
    meetings = write_meetings_dictionary(csv_encoded)
    users = write_users_dictionary(csv_encoded)
    log_result = write_log_result_base(csv_encoded)
    meetings = add_meetings_duration(meetings, log_result)
    log_result = add_warning_flag(meetings, log_result)
    log_result = OrderedDict(sorted(log_result.items()))
    meeting_check = ''
    for log in log_result:
        if log_result[log]['meeting'] != meeting_check:
            log_result[log]['meeting_change'] = True
            meeting_check = log_result[log]['meeting']

    for user in users:

        for log in log_result:
            matching_user = log_result[log]['user']

            if user == matching_user:
                if log_result[log]['meeting'] not in users[user]:
                    users.add_attribute(user, log_result[log]['meeting'], log_result[log])

    users = OrderedDict(sorted(users.items()))
    return users


def csv_reader_student_list(csv_file):

    csv_encoded = encoded_csv_student_list(csv_file)

    for record in csv_encoded:
        course = Course.objects.get(name=csv_encoded[record]['course'])
        Student.objects.create(
            name=csv_encoded[record]['name'],
            surname=csv_encoded[record]['surname'],
            date_of_birth=date.strptime(csv_encoded[record]['date_of_birth'], '%d/%m/%Y'),
            place_of_birth=csv_encoded[record]['place_of_birth'],
            resident_in_city=csv_encoded[record]['resident_in_city'],
            resident_in_address=csv_encoded[record]['resident_in_address'],
            postal_code=csv_encoded[record]['postal_code'],
            fiscal_code=csv_encoded[record]['fiscal_code'],
            handicap=csv_encoded[record]['handicap'],
            email=csv_encoded[record]['email'],
            telephone=csv_encoded[record]['telephone'],
            parent_email_1=csv_encoded[record]['parent_email_1'],
            parent_telephone_1=csv_encoded[record]['parent_telephone_1'],
            parent_email_2=csv_encoded[record]['parent_email_2'],
            parent_telephone_2=csv_encoded[record]['parent_telephone_2'],
            course=course,
        )

    return csv_encoded


def split_list(alist, wanted_parts=2):
    length = len(alist)
    return [ alist[i*length // wanted_parts: (i+1)*length // wanted_parts]
             for i in range(wanted_parts) ]


def encode_csv_regione_toscana(csv_file):

    csvfile = io.TextIOWrapper(csv_file)
    csv_encoded = Dictionary()
    dialect = csv.Sniffer().sniff(csvfile.read(), delimiters=",")

    csvfile.seek(0)
    csv_to_dictonary = csv.reader(csvfile, dialect)

    for index, row in enumerate(csv_to_dictonary):
        if row[0] != 'Attivita':
            split_name = row[3].split()
            name = split_list(split_name, 2)[1]
            surname = split_list(split_name, 2)[0]
            name_str = ''
            surname_str = ''
            for word in name:
                name_str += word.capitalize() + ' '
            for word in surname:
                surname_str += word.capitalize() + ' '
            csv_encoded.add_value(index, {
                'name': name_str[:-1],
                'surname': surname_str[:-1],
                'date_of_birth': datetime.datetime.strptime(row[6], '%d/%m/%Y'),
                'place_of_birth': row[7],
                'resident_in_city': row[17],
                'resident_in_address': row[14] + ' ' + row[15] + ' ' + row[16],
                'postal_code': row[18],
                'fiscal_code': row[4],
                'parent_email_1': row[13],
                'parent_telephone_1': row[12],
                'number': row[0],
                'registration_date': datetime.datetime.strptime(row[34], '%d/%m/%Y'),
            })
    csv_encoded = OrderedDict(sorted(csv_encoded.items()))
    return csv_encoded



def encode_csv(csv_file):

    csvfile = io.TextIOWrapper(csv_file)
    csv_encoded = Dictionary()
    dialect = csv.Sniffer().sniff(csvfile.read(1024), delimiters=",")
    csvfile.seek(0)
    csv_to_dictonary = csv.reader(csvfile, dialect)
    for index, row in enumerate(csv_to_dictonary):

        if row[3] != 'Identificatore partecipante':
            date_str = row[0]
            csv_encoded.add_value(index, {
                'Codice riunione': row[2],
                'Utente': row[5],
                'Durata connessione': int(row[4]),
                'Orario di uscita': datetime.datetime.strptime(date_str, '%d %b %Y, %H:%M:%S %Z').time(),
                'Data': datetime.datetime.strptime(date_str, '%d %b %Y, %H:%M:%S %Z').date()
            })
    csv_encoded = OrderedDict(sorted(csv_encoded.items()))
    return csv_encoded


def encoded_csv_student_list(csv_file):
    csv_encoded = Dictionary()

    csvfile = io.TextIOWrapper(csv_file)

    dialect = csv.Sniffer().sniff(csvfile.read(1024), delimiters=",")
    csvfile.seek(0)
    csv_to_dictonary = csv.reader(csvfile, dialect)
    for index, row in enumerate(csv_to_dictonary):

        if row[0] != 'Nome [richiesto]':
            csv_encoded.add_value(index, {
                'name': row[0],
                'surname': row[1],
                'date_of_birth': row[2],
                'place_of_birth': row[3],
                'resident_in_city': row[4],
                'resident_in_address': row[5],
                'postal_code': row[6],
                'fiscal_code': row[7],
                'handicap': row[8],
                'email': row[9],
                'telephone': row[10],
                'parent_email_1': row[11],
                'parent_telephone_1': row[12],
                'parent_email_2': row[13],
                'parent_telephone_2': row[14],
                'course': row[15],
            })

    return csv_encoded


def write_meetings_dictionary(csv_encoded):
    result_dict = Dictionary()
    for record in csv_encoded:
        if csv_encoded[record]['Codice riunione'] not in result_dict.values():
            result_dict.new(csv_encoded[record]['Codice riunione'], {
                'Durata': 0,
                'Presenti': 0,
                'valore minimo': 100000,
                'valore massimo': 0
            })
    return result_dict


def write_users_dictionary(csv_encoded):
    result_dict = Dictionary()
    for record in csv_encoded:
        if csv_encoded[record]['Utente'] not in result_dict.values():
            result_dict.new(csv_encoded[record]['Utente'], {

            })
    return result_dict


def write_log_result_base(csv_encoded):
    log_result = Dictionary()
    for record in csv_encoded:
        key = csv_encoded[record]['Codice riunione'] + " - " + csv_encoded[record]['Utente']
        if key not in log_result.keys():
            log_result.new(key, {
                'meeting': csv_encoded[record]['Codice riunione'],
                'user': csv_encoded[record]['Utente'],
                'elapsed_time': csv_encoded[record]['Durata connessione'],
                'time': csv_encoded[record]['Orario di uscita'],
                'date': csv_encoded[record]['Data'],
                'meeting_change': False
            })

        else:
            log_result.sum(key, 'elapsed_time', csv_encoded[record]['Durata connessione'])
            if csv_encoded[record]['Orario di uscita'] > log_result[key]['time']:
                log_result.add_attribute(key, 'time', csv_encoded[record]['Orario di uscita'])

    return log_result


def add_meetings_duration(meetings_dict, log_result):
    for log in log_result:
        meeting = log_result[log]['meeting']
        meetings_dict.sum(meeting, 'Durata', log_result[log]['elapsed_time'])
        meetings_dict.sum(meeting, 'Presenti', 1)
        if log_result[log]['elapsed_time'] < meetings_dict[meeting]['valore minimo']:
            meetings_dict.add_attribute(meeting, 'valore minimo', log_result[log]['elapsed_time'])
        if log_result[log]['elapsed_time'] > meetings_dict[meeting]['valore massimo']:
            meetings_dict.add_attribute(meeting, 'valore massimo', log_result[log]['elapsed_time'])
    meetings_dict = calculate_meeting_average_duration(meetings_dict)

    return meetings_dict


def calculate_meeting_average_duration(meetings_dict):
    for meeting in meetings_dict:
        if meetings_dict[meeting]["Presenti"] > 2:
            duration = (meetings_dict[meeting]['Durata'] - meetings_dict[meeting]['valore minimo'] - meetings_dict[meeting]['valore massimo'])
            mean = int((duration / (meetings_dict[meeting]['Presenti'] - 2)))
        else:
            duration = (meetings_dict[meeting]['Durata'])
            mean = int((duration / (meetings_dict[meeting]['Presenti'])))

        meetings_dict.add_attribute(meeting, 'Durata', mean)
        meetings_dict.add_attribute(meeting, 'Durata_ore', round(mean/60/60))
    return meetings_dict


def add_warning_flag(meetings, log_result):
    for log in log_result:
        meeting = meetings.get(log_result[log]['meeting'])
        if log_result[log]['elapsed_time'] > (meeting['Durata'] + 1000) or log_result[log]['elapsed_time'] < (meeting['Durata'] - 1000) or log_result[log]['elapsed_time'] < 2700:
            log_result.add_attribute(log, 'too_much', True)
    return log_result


def set_permissions(user, task):

    if task == 'T':
        group = Group.objects.get(name='Tutor')
        group.user_set.add(user)

    elif task == 'D':
        group = Group.objects.get(name='Docenti')
        group.user_set.add(user)

    elif task == 'S':
        group = Group.objects.get(name='Segreteria')
        group.user_set.add(user)

    elif task == 'C':
        group = Group.objects.get(name='Coordinamento')
        group.user_set.add(user)

    elif task == 'P':
        group = Group.objects.get(name='Direzione')
        group.user_set.add(user)

    return


class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Student):
            return str(obj)
        return super().default(obj)

