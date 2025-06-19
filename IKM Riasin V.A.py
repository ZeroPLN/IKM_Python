""" 
Многочлен P(x) = a_n * x^n + a_(n-1) * x^(n-1) + ... + a_1 * x + a_0 с целыми коэффициентами можно представить в виде списка,
в котором первое информационное поле соответствует коэффициенту при неизвестном, а второе показателю степени этого же неизвестного. 
Написать процедуры для ввода и вывода многочлена из строкового формата в список. 
В качестве строкового формата может использоваться запись типа: 52y^10 – 3y^8 + y, где знак ^ означает возведение в степень. Реализовать процедуру для приведения подобных слагаемых в многочлене. 
С помощью описанных процедур ввести многочлен из файла, привести подобные члены и вывести результирующий многочлен в конец исходного файла, расположив его члены в порядке убывания степеней. 
Использовать однонаправленный линейный список. 
"""
# Класс узла односвязного списка для хранения члена многочлена.
class Node:
    def __init__(self, coef: int, degree: int) -> None:
        self.coef = coef      # Коэффициент
        self.degree = degree  # Степень
        self.next = None      # Ссылка на следующий элемент

# Класс для работы с многочленом в виде односвязного списка
class PolynomialList:
    def __init__(self) -> None:
        self.head = None # Голова списка

    # Добавление нового члена в конец списка
    def push(self, coef: int, degree: int) -> None:
        if coef == 0:
            return
        new_node = Node(coef, degree)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    # Приведение подобных членов (с одинаковой степенью)
    def combine_like_terms(self) -> None:
        current = self.head
        while current:
            prev = current
            checker = current.next
            while checker:
                if checker.degree == current.degree:
                    current.coef += checker.coef
                    prev.next = checker.next
                    checker = checker.next
                else:
                    prev = checker
                    checker = checker.next
            current = current.next

        # Удаление нулевых коэффициентов
        while self.head and self.head.coef == 0:
            self.head = self.head.next

        current = self.head
        while current and current.next:
            if current.next.coef == 0:
                current.next = current.next.next
            else:
                current = current.next

    # Сортировка членов по убыванию степени (пузырьком)
    def bubble_sort(self) -> None:
        if self.head is None:
            return
        swapped = True
        while swapped:
            swapped = False
            prev = None
            current = self.head
            while current and current.next:
                if current.degree < current.next.degree:
                    swapped = True
                    nxt = current.next
                    current.next = nxt.next
                    nxt.next = current
                    if prev:
                        prev.next = nxt
                    else:
                        self.head = nxt
                    prev = nxt
                else:
                    prev = current
                    current = current.next

    # Преобразование списка в строку для вывода
    def list_to_string(self, variable: str = 'y') -> str:
        current = self.head
        if not current:
            return "0"
        result = ""
        while current:
            c, d = current.coef, current.degree
            sign = " + " if c > 0 else " - "
            if result == "":
                sign = "-" if c < 0 else ""
            result += sign
            abs_coef = abs(c)
            if d == 0:
                result += str(abs_coef)
            elif d == 1:
                result += f"{'' if abs_coef == 1 else abs_coef}{variable}"
            else:
                result += f"{'' if abs_coef == 1 else abs_coef}{variable}^{d}"
            current = current.next
        return result.strip(" +")


# Функция преобразования строки в односвязный список многочлена 
def parsing_polynomial(input_str: str) -> tuple['PolynomialList', str]:
    input_str = input_str.replace(' ', '')
    if not input_str:
        print("Пустой ввод!")
        return None, None

    # Определяем переменную (первая буква)
    variable = 'y'
    for ch in input_str:
        if ch.isalpha():
            variable = ch
            break

    # Проверка на наличие других переменных
    for ch in input_str:
        if ch.isalpha() and ch != variable:
            print(f"Ошибка: обнаружена вторая переменная '{ch}' (разрешена только одна переменная! например: '{variable}')")
            return None, None

    input_str = input_str.lower().replace('-', '+-')
    terms = input_str.split('+')
    poly = PolynomialList()

    for term in terms:
        if not term:
            continue

        # Проверка на некорректные случаи
        if term.count(variable) > 1:
            print(f"Ошибка: некорректный формат слагаемого '{term}' (двойная переменная)")
            return None, None
        if term.count('^') > 1:
            print(f"Ошибка: некорректный формат слагаемого '{term}' (двойная степень)")
            return None, None
        if '^' in term and variable not in term:
            print(f"Ошибка: некорректный формат слагаемого '{term}' (степень без переменной)")
            return None, None
        if '^' in term and term.index('^') < term.index(variable):
            print(f"Ошибка: некорректный формат слагаемого '{term}' (степень до переменной)")
            return None, None
        if '^' in term and term.endswith('^'):
            print(f"Ошибка: некорректный формат слагаемого '{term}' (нет степени после ^)")
            return None, None
        if variable in term and '^' in term:
            idx_var = term.index(variable)
            idx_pow = term.index('^')
            if idx_pow != idx_var + 1:
                print(f"Ошибка: некорректный формат слагаемого '{term}' (неправильное расположение ^)")
                return None, None
            if idx_var == 0 and (len(term) == 1 or term[0] == variable):
                coef = 1
            else:
                coef = term[:idx_var]
            degree = term[idx_pow+1:]
        elif variable in term:
            idx_var = term.index(variable)
            if idx_var == 0:
                coef = 1
            else:
                coef = term[:idx_var]
            degree = 1
        else:
            coef = term
            degree = 0

        # Преобразование коэффициента и степени к числу
        if coef == "" or coef == "+":
            coef = 1
        elif coef == "-":
            coef = -1
        try:
            coef = int(coef)
            degree = int(degree)
        except ValueError:
            print(f"Ошибка парсинга: '{term}'")
            return None, None
        
        poly.push(coef, degree)
        
    return poly, variable

# Функция для ввода данных
def input_data(filename: str) -> str: 
    while True:
        n = input("Выберите способ ввода данных: \n1 - Загрузить из файла " \
        "\n2 - Ввод с клавиатуры\nВыберите номер-> ")
        if n == "1":
            try:
                data = read_file(filename)
                if not data:
                    print("Файл пустой или не содержит данных. Попробуйте снова.")
                    continue
                print(f"Исходный многочлен из файла: {data}")
                return data
            except FileNotFoundError:
                print(f"Файл '{filename}' не найден. Попробуйте снова.")
            except Exception as e:
                print(f"Ошибка при чтении файла: {e}. Попробуйте снова.")
        elif n == "2":
            expr = input(
                "Введите строку с одним неизвестным "\
                "(в виде 52y^10 - 3y^8 + y - y + 5) -> "
            ).strip()
            if not expr:
                print("Ввод не может быть пустым. Попробуйте снова.")
                continue
            return expr
        else:
            print("Введите цифру 1 или 2!")

# Функция для считывания данных из файла
def read_file(filename: str) -> str:
    try:
        with open(filename, "r") as f:
            expression = f.readline().strip()
            if not expression:
                print("Файл пустой!")
                return ""
            return expression
    except FileNotFoundError:
        print(f"Файл '{filename}' не найден. Будет создан новый файл.")
        return ""
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return ""

# Функция для записи результата в файл
def write_to_file(filename: str, result: str) -> None:
    try:
        # Проверяем существование файла
        try:
            with open(filename, "r") as f:
                content = f.read()
        except FileNotFoundError:
            content = ""
        
        # Записываем результат
        with open(filename, "a") as file:
            if content:  # Если файл не пустой, добавляем перенос строки
                file.write("\n" + result)
            else:  # Если файл пустой, записываем без переноса
                file.write(result)
        print("Результат успешно записан в файл.")
    except Exception as e:
        print(f"Ошибка при записи в файл: {e}")

# Главная функция программы
def main() -> None:
    filename = "Polynom.txt"
    
    while True:
        input_string = input_data(filename)
        if not input_string:
            continue
            
        poly, variable = parsing_polynomial(input_string)
        if poly is None or variable is None:
            print("Ошибка при парсинге многочлена. Пожалуйста, введите многочлен снова.")
            continue

        poly.combine_like_terms()
        poly.bubble_sort()

        result = poly.list_to_string(variable)

        print(f"\nКонечный результат после приведения и сортировки: {result}")

        # Запись результата в файл
        write_to_file(filename, result)
        break

if __name__ == "__main__":
    main()
