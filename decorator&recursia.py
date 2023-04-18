# декоратор (паттерн)

def printer(function):
    def inner(*args, **kwargs):
        result = function(*args, **kwargs)
        message = f'Результат выполнения функции: {result}'
        return message

    return inner


# рекурсия



def custom_sum2(numbers):
    if len(numbers) == 1:
        return numbers[0]
    head, *tail = numbers
    return head + custom_sum2(tail)


@printer
def custom_sum3(*numbers):
    print(numbers)
    return sum(numbers)


def FUCKtorial_chisla1(number):   # Функция факториала числа через рекурсию
    if number == 0:
        return 1
    else:
        return number * FUCKtorial_chisla1(number - 1)


def FUCKtorial_chisla2(number):   # Функция факториала числа без рекурсии
    result = 1
    for i in range(1, number + 1):
        result *= i
    return result


if __name__ == '__main__':
    print(custom_sum2([2, 3, 4, 5]))
    print(custom_sum3(2, 3, 4, 5))
    print(FUCKtorial_chisla1(5))
    print(FUCKtorial_chisla2(5))

# НАПИСАТЬ ДЕКОРАТОР, КОТОРЫЙ БУДЕТ СЧИТАТЬ ВРЕМЯ ВЫПОЛНЕНИЯ ФУНКЦИИ МИЛИСЕКУНДАХ
# ЗАДАНИЕ СО ЗВЕЗДОЧКОЙ - ЭТОТ ДЕКОРАТОР ДОЛЖЕН ПРИНИМАТЬ 1 АРГУМЕНТ(СЕКУНДЫ) И ЕСЛИ ВРЕМЯ ВЫПОЛНЕНИЯ БУДЕТ БОЛЬШЕ ЭТИХ
# СЕКУНД, ДОЛЖНО ВЫДАВАТЬ ОШИБКУ (ТЕКСТ: ВРЕМЯ ВЫПОЛНЕНИЕ ПРЕВЫСИЛО (АРГУМЕНТ)
# ПОЧИТАТЬ В ИНТЕРНЕТАХ О ТОМ КАК ПЕРЕДАВАТЬ АРГУМЕНТЫ В ДЕКОРАТОР И ПРОЧИТАЬ ЧТО ТАКОЕ ЭКСЭПШН(ИСКЛЮЧЕНИЯ)

import time


def decorator_for_decorator(seconds):
    def decorator(func):
        def inner(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            time.sleep(2)
            end = time.time()
            working_time = (end - start) * 1000
            if working_time > seconds * 1000:
                raise TimeoutError(f'время выполнения превысило {seconds} секунд')
            print(f'функция работала {working_time:.3f} миллисекунд')
            return result
        return inner
    return decorator


@decorator_for_decorator(2)
def mult(a, d):
    return (a ** d) * 250 * 20 / 50 * 34 / 45 * 59


print(mult(4, 6))
