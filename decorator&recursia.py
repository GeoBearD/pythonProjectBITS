# декоратор (паттерн)

def printer(function):
    def inner(*args, **kwargs):
        result = function(*args, **kwargs)
        message = f'Результат выполнения функции: {result}'
        return message
    return inner

# рекурсия

def custom_sum1(numbers):
    result = 0
    for number in numbers:
        result += number
    return result

def custom_sum2(numbers):
    if len(numbers) == 1:
        return numbers[0]
    head, *tail = numbers
    return  head + custom_sum2(tail)

@printer
def custom_sum3(*numbers):
    print(numbers)
    return sum(numbers)


if __name__ == '__main__':
    print(custom_sum2([2, 3, 4, 5]))
    print(custom_sum3(2, 3, 4, 5))



# НАПИСАТЬ ДЕКОРАТОР, КОТОРЫЙ БУДЕТ СЧИТАТЬ ВРЕМЯ ВЫПОЛНЕНИЯ ФУНКЦИИ МИЛИСЕКУНДАХ
# ЗАДАНИЕ СО ЗВЕЗДОЧКОЙ - ЭТОТ ДЕКОРАТОР ДОЛЖЕН ПРИНИМАТЬ 1 АРГУМЕНТ(СЕКУНДЫ) И ЕСЛИ ВРЕМЯ ВЫПОЛНЕНИЯ БУДЕТ БОЛЬШЕ ЭТИХ СЕКУНД, ДОЛЖНО ВЫДАВАТЬ ОШИБКУ (ТЕКСТ: ВРЕМЯ ВЫПОЛНЕНИЕ ПРЕВЫСИЛО (АРГУМЕНТ)
# ПОЧИТАТЬ В ИНТЕРНЕТАХ О ТОМ КАК ПЕРЕДАВАТЬ АРГУМЕНТЫ В ДЕКОРАТОР И ПРОЧИТАЬ ЧТО ТАКОЕ ЭКСЭПШН(ИСКЛЮЧЕНИЯ)

