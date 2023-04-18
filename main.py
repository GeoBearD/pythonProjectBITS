import csv
import os
import urllib.request
import datetime
from collections import Counter
import re
from prettytable import PrettyTable
import charset_normalizer

NUMBERS_OF_DIGITS_IN_PHONE = 11                           # Корректное колличество цифр в номере
filename = './base.csv'                                  # Заданное имя файла
url = 'https://lk.globtelecom.ru/upload/test_prog1.csv'  # Ссылка на файл


def download_file():                                     # Функция для скачивания файла
    urllib.request.urlretrieve(url, filename)


def detect_encoding(filename: str) -> str:               # Функция, определяющая кодировку файла и норм. его
    with open(filename, 'rb') as f:
        result = charset_normalizer.detect(f.read())
        return result.get('encoding')


def validate_phone(phone: str) -> bool:                  # Проверка номер на валидность
    valid_numbers = r"^[0-9]+$"
    return len(phone) == NUMBERS_OF_DIGITS_IN_PHONE and re.match(valid_numbers, phone)


def calculate_age(dob: str) -> int:                      # Определение возраста на данный момент
    birthdate = datetime.datetime.strptime(dob, '%d.%m.%Y')
    today = datetime.datetime.now()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age

def read_content():
    encoding = detect_encoding(filename)
    with open(filename, 'r', encoding=encoding) as f:
        return f.readlines()


def phone_numbers_statistic(content):                           # Статистика по одинаковым номерам в консоли в виде таблицы
    phones = []
    for line in content:
        phone = line.strip().split(';')[0]
        phones.append(phone)
    duplicate_phones = set([phone for phone in phones if phones.count(phone) > 1])
    num_duplicate_phones = len(duplicate_phones)
    table_num = PrettyTable()
    table_num.field_names = ["Количество повторяющихся номеров телефона", "Повторяющиеся номера"]
    table_num.add_row([num_duplicate_phones, duplicate_phones])
    print(table_num)


def surname_statistic(content):                                 # Статистика по однофамильцам в консоли в виде таблицы
        surnames = []
        for line in content:
            surname = line.split()[4]
            surnames.append(surname)
        surname_counts = Counter(surnames)
        same_surname_count = 0
        for surname, count in surname_counts.items():
            if count > 1:
                same_surname_count += count
        table_sur = PrettyTable()
        table_sur.field_names = ["Количество однофамильцев"]
        table_sur.add_row([same_surname_count])
        print(table_sur)


def dob_statistic(content):                                    # Статистика по годам рождения в консоли в виде таблицы
        years = {}
        for line in content:
            date_string = line.strip().split(';')[8]
            date_obj = datetime.datetime.strptime(date_string, "%d.%m.%Y")
            year = date_obj.year
            if year in years:
                years[year] += 1
            else:
                years[year] = 1
        print("Статистика по годам рождения:")
        table = PrettyTable()
        table.field_names = ["Год", "Количество"]
        for year, count in sorted(years.items()):
            count = years[year]
            table.add_row([year, count])
        print(table)


def read_file():                             # Считываем файл, раскидываем по двум файлам и выводим некорректные номера
    encoding = detect_encoding(filename)
    with open(filename, 'r', encoding=encoding) as f:
        reader = csv.reader(f, delimiter=';')
        for i, line in enumerate(reader, start=1):
            formated_line = f'ФИО: {line[4]}; Телефон: {line[0]}; Дата Рождения: {line[8]}; Возраст на сегодня: {calculate_age(line[8])}; \n'
            if not validate_phone(line[0]):
                defect_line = f'{i} - ИО: {line[3]}; Телефон: {line[0]};'
                print(defect_line)
            elif validate_phone(line[0]) and line[7] == 'pos':
                with open("pos_h.csv", "a", encoding=encoding) as f:
                    f.write(formated_line)
            elif validate_phone(line[0]) and line[7] == 'cash':
                with open("cash_h.csv", "a", encoding=encoding) as f:
                    f.write(formated_line)


def delete():                                           # Удаляем файл после манипуляций
    os.remove(filename)


def main():
    download_file()
    content = read_content()
    read_file()
    phone_numbers_statistic(content)
    surname_statistic(content)
    dob_statistic(content)
    delete()


if __name__ == '__main__':
    main()
