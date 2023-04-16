import csv
import os
import urllib.request
import datetime
from collections import Counter
import re
from prettytable import PrettyTable
import charset_normalizer

number_of_digits_in_phone = 11
filename = './base.csv'
url = 'https://lk.globtelecom.ru/upload/test_prog1.csv'


def download_file():
    urllib.request.urlretrieve(url, filename)


def detect_encoding(filename: str) -> str:
    with open(filename, 'rb') as f:
        result = charset_normalizer.detect(f.read())
        return result.get('encoding')


def validate_phone(phone: str) -> bool:
    valid_numbers = r"^[0-9]+$"
    return len(phone) == number_of_digits_in_phone and re.match(valid_numbers, phone)


def calculate_age(dob: str) -> int:
    birthdate = datetime.datetime.strptime(dob, '%d.%m.%Y')
    today = datetime.datetime.now()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age


def after_read_statistic():
    encoding = detect_encoding(filename)
    with open(filename, 'r', encoding=encoding) as f:
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
        samesurname_count = 0
        for surname, count in surname_counts.items():
            if count > 1:
                samesurname_count += count
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
    encoding = detect_encoding(filename)
    with open(filename, 'r', encoding=encoding) as f:
        reader = csv.reader(f, delimiter=';')
        for i, line in enumerate(reader, start=1):
            formated_line = f' ФИО: {line[4]}; Телефон: {line[0]}; Дата Рождения: {line[8]}; Возраст на сегодня: {calculate_age(line[8])}; \n'
            if not validate_phone(line[0]):
                defect_line = f'{i} - ИО: {line[3]}; Телефон: {line[0]};'
                print(defect_line)
            elif validate_phone(line[0]) and line[7] == 'pos':
                with open("pos_h.csv", "a", encoding=encoding) as f:
                    f.write(formated_line)
            elif validate_phone(line[0]) and line[7] == 'cash':
                with open("cash_h.csv", "a", encoding=encoding) as f:
                    f.write(formated_line)


def delete():
    os.remove(filename)


def main():
    download_file()
    read_file()
    after_read_statistic()
    delete()


if __name__ == '__main__':
    main()
