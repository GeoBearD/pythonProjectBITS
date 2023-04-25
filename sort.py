import csv
from file import FILENAME
from file import detect_encoding
from statistics import validate_phone, calculate_age
from prettytable import PrettyTable

NUMBERS_OF_DIGITS_IN_PHONE = 11  # Корректное колличество цифр в номере


def write_to_file(line, filename, encoding):
    with open(filename, "a", encoding=encoding) as f:
        f.write(line)


def sort_in_files(content):  # Считываем файл, раскидываем по двум файлам и выводим некорректные номера
    encoding = detect_encoding(FILENAME)
    reader = csv.reader(content, delimiter=';')
    table_1 = PrettyTable()
    table_1.field_names = ["ID", "ФИО", "Некорректные номера"]
    for i, line in enumerate(reader, start=1):
        phone = line[0]
        name_surname = line[3]
        initials = line[4]
        payment_method = line[7]
        dob = line[8]
        age = calculate_age(line[8])
        formatted_line = f'ФИО: {initials}; Телефон: {validate_phone(phone)}; Дата Рождения: {dob}; Возраст на сегодня: {age}; \n'
        if len(validate_phone(phone)) != NUMBERS_OF_DIGITS_IN_PHONE:
            table_1.add_row([i, name_surname, validate_phone(phone)])
        else:
            write_to_file(formatted_line, f'{payment_method}_h.csv', encoding)

    if len(table_1._rows) > 0:
        print(table_1)
    else:
        print("Нет некорректных номеров телефонов.")
