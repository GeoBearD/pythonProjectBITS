import charset_normalizer
import os
import urllib.request


FILENAME = './base.csv'  # Заданное имя файла
URL = 'https://lk.globtelecom.ru/upload/test_prog1.csv'  # Ссылка на файл


def download_file():  # Функция для скачивания файла
    if os.path.exists(FILENAME):
        print(f"Файл {FILENAME} уже существует.")
    else:
        urllib.request.urlretrieve(URL, FILENAME)
        print(f"Файл {FILENAME} успешно загружен.")


def detect_encoding(file: str) -> str:  # Функция, определяющая кодировку файла и норм. его
    with open(file, 'rb') as f:
        result = charset_normalizer.detect(f.read())
        return result.get('encoding')


def read_content():
    encoding = detect_encoding(FILENAME)
    with open(FILENAME, 'r', encoding=encoding) as f:
        return f.readlines()


def delete():  # Удаляем файл после манипуляций
    if os.path.exists(FILENAME):
        os.remove(FILENAME)
        print(f"Файл {FILENAME} успешно удален.")
    else:
        print(f"Файл {FILENAME} не найден.")
