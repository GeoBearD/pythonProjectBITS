import csv
import charset_normalizer
import os
import urllib.request
import logging
import re
import datetime
from collections import Counter
from prettytable import PrettyTable

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
FILENAME = './base.csv'
URL = 'https://lk.globtelecom.ru/upload/test_prog1.csv'  # Ссылка на файл
NUMBERS_OF_DIGITS_IN_PHONE = 11  # Корректное количество цифр в номере


class SourceCSVFile:
    def __init__(self, filename):
        self.filename = filename
        self.__content = None

    def get_raw_content(self):
        return self.__content

    @classmethod
    def from_web(cls, filename, url):
        obj = cls(filename)
        obj.download_file(url)
        obj.__content = obj.read_file()
        return obj

    def download_file(self, url):
        if os.path.isfile(self.filename):
            logger.info(f"Файл {self.filename} уже существует.")
        else:
            urllib.request.urlretrieve(url, self.filename)
            logger.info(f"Файл {self.filename} успешно загружен.")

    @classmethod
    def from_file(cls, filename):
        return cls(filename)

    def detect_encoding(self):  # Функция, определяющая кодировку файла и нормализующая его
        with open(self.filename, 'rb') as f:
            result = charset_normalizer.detect(f.read())
            return result.get('encoding')

    def read_file(self):
        encoding = self.detect_encoding()
        with open(self.filename, 'r', encoding=encoding) as f:
            reader = csv.reader(f, delimiter=';')
            self.__content = [
                {'phone': re.sub(r'\D', '', row[0]), 'initials': row[3], 'fullname': row[4], 'payment_method': row[7],
                 'dob': row[8]} for
                row in reader]
            return self.__content

    @staticmethod
    def write_to_file(line, filename, encoding):
        with open(filename, "a", encoding=encoding) as f:
            f.write(line)

    @staticmethod
    def calculate_age(line):
        birthdate = datetime.datetime.strptime(line['dob'], '%d.%m.%Y')
        today = datetime.datetime.now()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        return age

    def sort_in_files(self):
        table_1 = PrettyTable()
        table_1.field_names = ["ID", "ФИО", "Некорректные номера"]

        # Создать словарь для хранения данных, которые будут записаны в файлы
        data_by_payment_method = {}

        for i, line in enumerate(self.__content, start=1):
            age = self.calculate_age(line)

            formatted_line = f"ФИО: {line['fullname']}; Телефон: {line['phone']}; Дата Рождения: {line['dob']};" \
                             f" Возраст на сегодня: {age}; \n"
            if len(line['phone']) != NUMBERS_OF_DIGITS_IN_PHONE:
                table_1.add_row([i, line['initials'], line['phone']])
            else:
                payment_method = line['payment_method']

                # Добавить данные в соответствующий словарь по способу оплаты
                if payment_method in data_by_payment_method:
                    data_by_payment_method[payment_method].append(formatted_line)
                else:
                    data_by_payment_method[payment_method] = [formatted_line]

        if len(table_1._rows) > 0:
            print(table_1)
        else:
            print(f"Нет некорректных номеров телефонов.")

        # Записать данные из словаря в файлы
        for payment_method, data in data_by_payment_method.items():
            filename = f"{payment_method}_h.csv"
            encoding = self.detect_encoding()
            for line in data:
                self.write_to_file(line, filename, encoding)

    # def sort_in_files(self):
    #     table_1 = PrettyTable()
    #     table_1.field_names = ["ID", "ФИО", "Некорректные номера"]
    #     for i, line in enumerate(self.__content, start=1):
    #         age = self.calculate_age(line)
    #
    #         formatted_line = f"ФИО: {line['fullname']}; Телефон: {line['phone']}; Дата Рождения: {line['dob']};" \
    #                          f" Возраст на сегодня: {age}; \n"
    #         if len(line['phone']) != NUMBERS_OF_DIGITS_IN_PHONE:
    #             table_1.add_row([i, line['initials'], line['phone']])
    #         else:
    #             self.write_to_file(formatted_line, f"{line['payment_method']}_h.csv", self.detect_encoding())
    #     if len(table_1._rows) > 0:
    #         print(table_1)
    #     else:
    #         print(f"Нет некорректных номеров телефонов.")



    def print_numbers(self):
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

    def delete_file(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)
            logger.info(f"Файл {self.filename} успешно удален.")
        else:
            logger.info(f"Файл {self.filename} не найден.")


if __name__ == '__main__':
    file1 = SourceCSVFile.from_web(FILENAME, URL)
    file1.sort_in_files()
    file1.print_numbers()
    file1.print_namesakes()
    file1.print_yob()
    file1.delete_file()
