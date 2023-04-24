import csv
from file import FILENAME
from file import detect_encoding
from statistics import validate_phone, calculate_age

NUMBERS_OF_DIGITS_IN_PHONE = 11  # Корректное колличество цифр в номере


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
        elif validate_phone(phone) and payment_method == 'cards':
            with open("cards_h.csv", "a", encoding=encoding) as f:
                f.write(formatted_line)
