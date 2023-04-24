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


def after_read_statistic(content):
    phones = []
    base = []
    surnames = []
    years = {}
    male_count = 0
    female_count = 0
    name_duplicates = {}
    reader = csv.reader(content, delimiter=';')
    for line in reader:
        fullname = line[4]
        surname = fullname.split(' ')[0]
        surnames.append(surname)

        phone = validate_phone(line[0])
        phones.append(phone)

        date_string = line[8]
        date_obj = datetime.datetime.strptime(date_string, "%d.%m.%Y")
        year = date_obj.year
        if year in years:
            years[year] += 1
        else:
            years[year] = 1
        if surname in name_duplicates:
            name_duplicates[surname].append(fullname)
        else:
            name_duplicates[surname] = [fullname]

    same_surname_count = sum(count for count in Counter(surnames).values() if count > 1)
    duplicate_phones = set(phone for phone in phones if phones.count(phone) > 1)
    num_duplicate_phones = len(duplicate_phones)
    table1 = PrettyTable()
    table1.field_names = ["Количество повторяющихся номеров", "Повторяющиеся номера"]
    table1.add_row([num_duplicate_phones, ", ".join(duplicate_phones)])
    print(table1)

    table2 = PrettyTable()
    table2.field_names = ["Год", "Количество родившихся"]
    for year, count in sorted(years.items()):
        table2.add_row([year, count])
    print(table2)

    table4 = PrettyTable()
    table4.field_names = ["Фамилия", "Количество однофамильцев"]
    for sur_name, name_list in name_duplicates.items():
        if len(name_list) > 1:
            base.append(name_list)
            table4.add_row([sur_name, len(name_list)])
    print(table4)

    patronymics = []
    for name_list in base:
        patronymic_list = [name.split(' ')[2] for name in name_list]
        patronymics.extend(patronymic_list)
    for patron in patronymics:
        if patron.endswith('А'):
            female_count += 1
        else:
            male_count += 1
    table3 = PrettyTable()
    table3.field_names = ["Количество однофамильцев всего в файле:", "Количество мужчин", "Количество женщин"]
    table3.add_row([same_surname_count, male_count, female_count])
    print(table3)
