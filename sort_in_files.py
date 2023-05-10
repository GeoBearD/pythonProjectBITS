from prettytable import PrettyTable

NUMBERS_OF_DIGITS_IN_PHONE = 11  # Корректное количество цифр в номере


class Sort:
    def __init__(self, content, data):
        self.__content = content
        self.data = data

    @staticmethod
    def write_to_file(line, filename, encoding):
        with open(filename, "a", encoding=encoding) as f:
            f.write(line)

    def sort_in_files(self):
        table_1 = PrettyTable()
        table_1.field_names = ["ID", "ФИО", "Некорректные номера"]

        # Создать словарь для хранения данных, которые будут записаны в файлы
        data_by_payment_method = {}

        for i, line in enumerate(self.__content, start=1):
            age = self.data.calculate_age(line)

            formatted_line = f"ФИО: {line['fullname']}; Телефон: {line['phone']}; Дата Рождения: {line['dob']};" \
                             f" Возраст на сегодня: {age}; \n"
            if len(line['phone']) != NUMBERS_OF_DIGITS_IN_PHONE:
                table_1.add_row([i, line['initials'], line['phone']])
            else:
                payment_method = line['payment_method']

                # Добавить данные в соответствующий словарь по способу оплаты
                if payment_method in data_by_payment_method:
                    data_by_payment_method[payment_method].append(formatted_line)
                else:
                    data_by_payment_method[payment_method] = [formatted_line]

        if len(table_1._rows) > 0:
            print(table_1)
        else:
            print(f"Нет некорректных номеров телефонов.")

        # Записать данные из словаря в файлы
        for payment_method, data in data_by_payment_method.items():
            filename = f"{payment_method}_h.csv"
            for line in data:
                self.write_to_file(line, filename, encoding='UTF-8')
