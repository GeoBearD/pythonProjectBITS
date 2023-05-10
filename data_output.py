import datetime
from collections import Counter
from prettytable import PrettyTable


class DataOutput:
    def __init__(self, content):
        self.__content = content

    @staticmethod
    def calculate_age(line):
        birthdate = datetime.datetime.strptime(line['dob'], '%d.%m.%Y')
        today = datetime.datetime.now()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        return age

    def same_numbers(self):
        phones = []
        phone_counts = {}
        for line in self.__content:
            phone = line['phone']
            phones.append(phone)
        for phone in phones:
            if phone in phone_counts:
                phone_counts[phone] += 1
            else:
                phone_counts[phone] = 1

        table_5 = PrettyTable()
        table_5.field_names = ["Количество повторений", "Номер телефона"]
        for phone, count in phone_counts.items():
            if count > 1:
                table_5.add_row([count, phone])
        print(table_5)

    def print_yob(self):
        years = {}
        for line in self.__content:
            date_string = line['dob']
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

    def print_namesakes(self):
        base = []
        surnames = []
        patronymics = []
        male_count = 0
        female_count = 0
        name_duplicates = {}
        for line in self.__content:
            fullname = line['fullname']
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
