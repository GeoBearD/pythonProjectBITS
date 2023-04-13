import csv
import urllib.request

import charset_normalizer


def download_file():
    url = 'https://lk.globtelecom.ru/upload/test_prog1.csv'
    filename = 'test.csv'
    urllib.request.urlretrieve(url, filename)


def detect_encoding(filepath: str):
    with open(filepath, 'rb') as f:
        result = charset_normalizer.detect(f.read())
        return result.get('encoding')


def validate_phone(phone: str) -> bool:
    return len(phone) == 11


def calculate_age(dob: str) -> str:
    pass


def read_file():
    filepath = './test.csv'
    encoding = detect_encoding(filepath)
    with open(filepath, 'r', encoding=encoding) as f:
        reader = csv.reader(f, delimiter=';')
        for line in reader:
            if not validate_phone(line[0]):
                print(line)
            formated_line = f'ФИО: {line[4]}; Телефон: {line[0]}; Дата рождения: {line[8]}'
            print(formated_line)


def main():
    download_file()
    read_file()


if __name__ == '__main__':
    main()
