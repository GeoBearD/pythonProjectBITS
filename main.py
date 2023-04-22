import csv
import os
import urllib.request
import datetime
from collections import Counter
import re
from prettytable import PrettyTable
import charset_normalizer

NUMBERS_OF_DIGITS_IN_PHONE = 11  # Корректное колличество цифр в номере
FILENAME = './base.csv'  # Заданное имя файла
URL = 'https://lk.globtelecom.ru/upload/test_prog1.csv'  # Ссылка на файл


def download_file():  # Функция для скачивания файла
    urllib.request.urlretrieve(URL, FILENAME)


def detect_encoding(file: str) -> str:  # Функция, определяющая кодировку файла и норм. его
    with open(file, 'rb') as f:
        result = charset_normalizer.detect(f.read())
        return result.get('encoding')


def validate_phone(phone: str) -> str:  # Проверка номер на валидность
    phone = re.sub(r'\D', '', phone)
    return phone


def calculate_age(dob: str) -> int:  # Определение возраста на данный момент
    birthdate = datetime.datetime.strptime(dob, '%d.%m.%Y')
    today = datetime.datetime.now()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age


def read_content():
    encoding = detect_encoding(FILENAME)
    with open(FILENAME, 'r', encoding=encoding) as f:
        return f.readlines()


def after_read_statistic(content):
    phones = []
    surnames = []
    years = {}
    male_count = 0
    female_count = 0
    lgbt_count = 0
    reader = csv.reader(content, delimiter=';')
    for line in reader:
        fullname = line[4]
        surname = fullname.split(' ')[0]
        surnames.append(surname)
        name = fullname.split(' ')[1]
        if name.endswith(('А', 'Я', 'Е')):
            female_count += 1
        elif name.endswith(('Ь')):
            lgbt_count += 1
        else:
            male_count += 1
        phone = validate_phone(line[0])
        phones.append(phone)
        date_string = line[8]
        date_obj = datetime.datetime.strptime(date_string, "%d.%m.%Y")
        year = date_obj.year
        if year in years:
            years[year] += 1
        else:
            years[year] = 1
    same_surname_count = sum(count for count in Counter(surnames).values() if count > 1)
    duplicate_phones = set(phone for phone in phones if phones.count(phone) > 1)
    num_duplicate_phones = len(duplicate_phones)
    table = PrettyTable()
    table.field_names = ["Количество повторяющихся номеров",
                         "Повторяющиеся номера"]
    table.add_row([num_duplicate_phones, ", ".join(duplicate_phones)])
    print(table)
    table2 = PrettyTable()
    table2.field_names = ["Год", "Количество родившихся"]
    for year, count in sorted(years.items()):
        table2.add_row([year, count])
    print(table2)
    table4 = PrettyTable()
    unique_surnames = set(surnames)
    duplicates = []
    for sur_name in unique_surnames:
        if sur_name.endswith(('А', 'Я', 'Е')):
            female_count += 1
        elif sur_name.endswith(('О', 'Ь')):
            lgbt_count += 1
        else:
            male_count += 1
        if surnames.count(sur_name) > 1:
            duplicates.append((sur_name, surnames.count(sur_name)))
    table3 = PrettyTable()
    table3.field_names = ["Количество однофамильцев всего в файле:",
                          "Количество мужчин", "Количество женщин", "Колличество LGBT+"]
    table3.add_row([same_surname_count, male_count, female_count, lgbt_count])
    print(table3)
    table4.field_names = ["Фамилия", "Количество однофамильцев"]
    for sur_name, count in duplicates:
        table4.add_row([sur_name, count])
    print(table4)


def sort_in_files(content):  # Считываем файл, раскидываем по двум файлам и выводим некорректные номера
    encoding = detect_encoding(FILENAME)
    reader = csv.reader(content, delimiter=';')
    for i, line in enumerate(reader, start=1):
        phone = line[0]
        name_surname = line[3]
        initials = line[4]
        payment_method = line[7]
        dob = line[8]
        age = calculate_age(line[8])
        formatted_line = f'ФИО: {initials}; Телефон: {validate_phone(phone)}; Дата Рождения: {dob}; Возраст на сегодня: {age}; \n'
        if len(validate_phone(phone)) != NUMBERS_OF_DIGITS_IN_PHONE:
            defect_line = f'{i} - ИО: {name_surname}; Телефон: {validate_phone(phone)};'
            print(defect_line)
        elif validate_phone(phone) and payment_method == 'pos':
            with open("pos_h.csv", "a", encoding=encoding) as f:
                f.write(formatted_line)
        elif validate_phone(phone) and payment_method == 'cash':
            with open("cash_h.csv", "a", encoding=encoding) as f:
                f.write(formatted_line)


def delete():  # Удаляем файл после манипуляций
    os.remove(FILENAME)


def main():
    download_file()
    content = read_content()
    sort_in_files(content)
    after_read_statistic(content)
    delete()


if __name__ == '__main__':
    main()
