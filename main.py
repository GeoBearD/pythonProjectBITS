import csv
import os
import urllib.request
import datetime
from collections import Counter
import re
from prettytable import PrettyTable
import charset_normalizer

number_of_digits_in_number = 11


def download_file():
    url = 'https://lk.globtelecom.ru/upload/test_prog1.csv'
    filename = 'base.csv'
    urllib.request.urlretrieve(url, filename)


def detect_encoding(filepath: str):
    with open(filepath, 'rb') as f:
        result = charset_normalizer.detect(f.read())
        return result.get('encoding')


def index_of_line():
    with open('./base.csv', 'r') as f:
        for i, line in enumerate(f, start=1):
            return i


def validate_phone(phone: str) -> bool:
    valid_numbers = r"^[0-9]+$"
    return len(phone) == number_of_digits_in_number and re.match(valid_numbers, phone)


def calculate_age(dob: str):
    birthdate = datetime.datetime.strptime(dob, '%d.%m.%Y')
    today = datetime.datetime.now()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age


def stats():
    filepath = './base.csv'
    encoding = detect_encoding(filepath)
    with open(filepath, 'r', encoding=encoding) as f:
        phones = []
        surnames = []
        years = {}
        for line in f:
            phone = line.strip().split(';')[0]
            phones.append(phone)
            surname = line.split()[4]
            surnames.append(surname)
            date_string = line.strip().split(';')[8]
            date_obj = datetime.datetime.strptime(date_string, "%d.%m.%Y")
            year = date_obj.year

            if year in years:
                years[year] += 1
            else:
                years[year] = 1

        duplicate_phones = set([phone for phone in phones if phones.count(phone) > 1])
        num_duplicate_phones = len(duplicate_phones)
        table_num = PrettyTable()
        table_num.field_names = ["Количество повторяющихся номеров телефона", "Повторяющиися номера"]
        table_num.add_row([num_duplicate_phones, duplicate_phones])
        print(table_num)

        surname_counts = Counter(surnames)
        duplicate_surnames = [surname for surname, count in surname_counts.items() if count > 1]
        num_duplicate_surnames = len(duplicate_surnames)
        samesurname_count = 0
        for surname, count in surname_counts.items():
            if count > 1:
                samesurname_count += count
        print(samesurname_count)
        table_sur = PrettyTable()
        table_sur.field_names = ["Количество однофамильцев"]
        table_sur.add_row([samesurname_count])
        print(table_sur)

        print("Статистика по годам рождения:")
        table = PrettyTable()
        table.field_names = ["Год", "Количество"]
        for year, count in sorted(years.items()):
            count = years[year]
            table.add_row([year, count])
        print(table)


def read_file():
    filepath = './base.csv'
    encoding = detect_encoding(filepath)
    with open(filepath, 'r', encoding=encoding) as f:
        reader = csv.reader(f, delimiter=';')
        for i, line in enumerate(reader):
            if not validate_phone(line[0]):
                defect_line = f'{i + 1} - ИО: {line[3]}; Телефон: {line[0]};'
                print(defect_line)
            if validate_phone(line[0]) and line[7] == 'pos':
                formated_line = f'ФИО: {line[4]}; Телефон:{line[0]}; Дата Рождения: {line[8]}; Возраст на сегодня:{calculate_age(line[8])}; \n'
                with open("pos_h.csv", "a", encoding=encoding) as f:
                    f.write(right_string)
            if validate_phone(line[0]) and line[7] == 'cash':
                right_string = f'ФИО: {line[4]}; Телефон:{line[0]}; Дата Рождения: {line[8]}; Возраст на сегодня:{calculate_age(line[8])}; \n'
                with open("cash_h.csv", "a", encoding=encoding) as f:
                    f.write(right_string)


def delete():
    filepath = './base.csv'
    os.remove(filepath)


def main():
    download_file()
    read_file()
    stats()
    delete()


if __name__ == '__main__':
    main()
