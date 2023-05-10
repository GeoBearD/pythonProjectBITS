from file_processing import SourceCSVFile
from data_output import DataOutput
from sort_in_files import Sort


FILENAME = './base.csv'  # Заданное имя файла
URL = 'https://lk.globtelecom.ru/upload/test_prog1.csv'  # Ссылка на файл


if __name__ == '__main__':
    file = SourceCSVFile(FILENAME)
    file.download_file(URL)
    content = file.read_file()
    data = DataOutput(content)
    sort = Sort(content, data)
    sort.sort_in_files()
    data.print_yob()
    data.same_numbers()
    data.print_namesakes()
    file.delete_file()



