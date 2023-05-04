import csv
import charset_normalizer
import os
import urllib.request
import logging
import re

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
FILENAME = './base.csv'  # Заданное имя файла
URL = 'https://lk.globtelecom.ru/upload/test_prog1.csv'  # Ссылка на файл
NUMBERS_OF_DIGITS_IN_PHONE = 11  # Корректное колличество цифр в номере


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

    def detect_encoding(self):  # Функция, определяющая кодировку файла и норм. его
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

    def split_content(self):
        pass

    def validate_phone(self):
        pass


class SortStatistic:
    def __init__(self, content):
        self.__content = content


if __name__ == '__main__':
    file1 = SourceCSVFile.from_web(FILENAME, URL)
    content = file1.get_raw_content()
    print(content)
