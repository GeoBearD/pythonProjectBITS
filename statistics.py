import csv
import datetime
from collections import Counter
import re
from prettytable import PrettyTable


def validate_phone(phone: str) -> str:  # Проверка номер на валидность
    phone = re.sub(r'\D', '', phone)
    return phone


def calculate_age(dob: str) -> int:  # Определение возраста на данный момент
    birthdate = datetime.datetime.strptime(dob, '%d.%m.%Y')
    today = datetime.datetime.now()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age


def print_numbers(content):
    phones = []
    phone_counts = {}
    reader = csv.reader(content, delimiter=';')
    for line in reader:
        phone = validate_phone(line[0])
        phones.append(phone)
    for phone in phones:
        if phone in phone_counts:
            phone_counts[phone] += 1
        else:
            phone_counts[phone] = 1

    table_1 = PrettyTable()
    table_1.field_names = ["Количество повторений", "Номер телефона"]
    for phone, count in phone_counts.items():
        if count > 1:
            table_1.add_row([count, phone])
    print(table_1)


def print_yob(content):
    years = {}
    reader = csv.reader(content, delimiter=';')
    for line in reader:
        date_string = line[8]
        date_obj = datetime.datetime.strptime(date_string, "%d.%m.%Y")
        year = date_obj.year
        if year in years:
            years[year] += 1
        else:
            years[year] = 1

    table_2 = PrettyTable()
    table_2.field_names = ["Год", "Количество родившихся"]
    for year, count in sorted(years.items()):
        table_2.add_row([year, count])
    print(table_2)


def print_namesakes(content):
    base = []
    surnames = []
    patronymics = []
    male_count = 0
    female_count = 0
    name_duplicates = {}
    reader = csv.reader(content, delimiter=';')
    for line in reader:
        fullname = line[4]
        surname = fullname.split(' ')[0]
        surnames.append(surname)
        if surname in name_duplicates:
            name_duplicates[surname].append(fullname)
        else:
            name_duplicates[surname] = [fullname]
    same_surname_count = sum(count for count in Counter(surnames).values() if count > 1)

    table_3 = PrettyTable()
    table_3.field_names = ["Фамилия", "Количество однофамильцев"]
    for sur_name, name_list in name_duplicates.items():
        if len(name_list) > 1:
            base.append(name_list)
            table_3.add_row([sur_name, len(name_list)])
    print(table_3)

    for name_list in base:
        patronymic_list = [name.split(' ')[2] for name in name_list]
        patronymics.extend(patronymic_list)
    for patron in patronymics:
        if patron.endswith('А'):
            female_count += 1
        else:
            male_count += 1

    table_4 = PrettyTable()
    table_4.field_names = ["Количество однофамильцев всего в файле:", "Количество мужчин", "Количество женщин"]
    table_4.add_row([same_surname_count, male_count, female_count])
    print(table_4)
