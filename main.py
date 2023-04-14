import csv
import urllib.request
import datetime
import charset_normalizer


def download_file():
    url = 'https://lk.globtelecom.ru/upload/test_prog1.csv'
    filename = 'test.csv'
    urllib.request.urlretrieve(url, filename)


def detect_encoding(filepath: str):
    with open(filepath, 'rb') as f:
        result = charset_normalizer.detect(f.read())
        return result.get('encoding')


def index_of_line():
    with open('./test.csv', 'r') as f:
        for i, line in enumerate(f, start=1):
            return i


def validate_phone(phone: str) -> bool:
    return len(phone) == 11


def calculate_age(dob: str):
    birthdate = datetime.datetime.strptime(dob, '%d.%m.%Y')
    today = datetime.datetime.now()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age


def read_file():
    filepath = './test.csv'
    encoding = detect_encoding(filepath)
    with open(filepath, 'r', encoding=encoding) as f:
        reader = csv.reader(f, delimiter=';')
        for line in reader:
            if not validate_phone(line[0]):
                defect_line = f' ИО: {line[3]}; Телефон: {line[0]};'
                print(defect_line)
            formated_line = f'ФИО: {line[4]}; Телефон: {line[0]}; Дата рождения: {line[8]}; Возраст на сегодня: {calculate_age(line[8])}'
            print(formated_line)


def main():
    download_file()
    read_file()


if __name__ == '__main__':
    main()
