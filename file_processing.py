import csv
import charset_normalizer
import os
import urllib.request
import re
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class SourceCSVFile:
    def __init__(self, filename):
        self.filename = filename
        self.__content = None

    def get_raw_content(self):
        return self.__content

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

    def delete_file(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)
            logger.info(f"Файл {self.filename} успешно удален.")
        else:
            logger.info(f"Файл {self.filename} не найден.")
