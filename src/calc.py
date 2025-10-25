from typing import List, Dict, Callable, Tuple

from src.exceptions import WrongBracketCombinationError, NotEnoughOperandsError, InvalidTokenError, TooManyOperandsError


class RPNCalculator:
    """Класс калькулятора"""

    def __init__(self):
        """
        При инициализации создаем словарь с операциями и пустой стек
        """
        self.stack: List[float] = []
        self.operations: Dict[str, Callable[[float, float], float]] = {
            "+": self.add,
            "-": self.subtract,
            "*": self.multiply,
            "/": self.divide,
            "**": self.power,
        }

    def process_token(self, tokens: List[Tuple[str, float | str]], i: int) -> int:
        """
        Метод обработки токена:
        Встретили скобку - начали собирать побочное выражение, решили его, закинули в стек.
        Встретили число - закинули в стек.
        Встретили операцию - обработали ее.
        Встретили закрывающую скобку - вызвали ошибку, тк если она не была обработана после того как мы дошли до
        открывающей, то у нее просто нет пары.
        """
        type, value = tokens[i]
        if type == "(":
            sub_calc = RPNCalculator()
            sub_tokens, new_i = self.collect_subtokens(tokens, i + 1)
            subres = sub_calc.solve(self.detokenize(sub_tokens))
            self.push(subres)
            return new_i
        elif type == "NUM":
            self.push(value)  # type: ignore
            return i + 1
        elif type == "OPR":
            self.process_operation(value)   # type: ignore
            return i + 1
        elif type == ")":
            raise WrongBracketCombinationError("Напутали со скобочками.")
        else:
            raise InvalidTokenError(f"Неизвестный тип токена: {type}")

    def collect_subtokens(self, tokens: List[Tuple[str, float | str]], i: int) -> Tuple[
        List[Tuple[str, float | str]], int]:
        """
        Этот метод запускаем после встречи с открывающей скобкой. Тут мы собираем всю последовательность,
        считая скобочки.
        Возвращаем новый i (индекс) элемента, стоящего после этой подпоследовательности и саму подпоследовательность.
        """
        bracket_count = 1
        sub_tokens: List[Tuple[str, float | str]] = []
        while i < len(tokens):
            token = tokens[i]
            type, value = tokens[i]
            if type == "(":
                bracket_count += 1
            elif type == ")":
                bracket_count -= 1
                if bracket_count == 0:
                    return sub_tokens, i + 1
            sub_tokens.append(token)
            i += 1
        raise WrongBracketCombinationError("Несбалансированные скобки")

    def process_operation(self, operation: str) -> None:
        """
        Обработчик токена операции. По его значению определяем нужную функцию все это лежит в словаре операций из
        инициализации. Забираем два верхних элемента стека, производим операцию, закидываем результат в стек
        """
        func = self.operations[operation]
        b = self.pop()
        a = self.pop()
        res = func(a, b)
        self.push(res)

    def solve(self, line: str) -> float:
        """
        Главная функция класса, тут мы принимаем строку, токенизируем ее. Далее идем по токенам и обрабатываем их.
        Почему итерация while-ом? Это нужно, чтобы спокойно менять переменную i, когда мы сталкиваемся с подвыражениями.
        Это позволяет нам проскакивать их.
        """
        tokens = self.tokenize(line)
        i = 0
        while i < len(tokens):
            i = self.process_token(tokens, i)
        if len(self.stack) != 1:
            raise NotEnoughOperandsError("Несбалансированная комбинация: несколько значений осталось в стеке.")
        return self.stack.pop()

    def tokenize(self, line: str) -> List[Tuple[str, float | str]]:
        """
        Токенизатор строки, идем по строке, разбитой split-ом по пробелам. Определяем тип токена, кладем его в кортеж со
        значением токена.
        """
        res: List[Tuple[str, float | str]] = []
        for el in line.strip().replace("()", "").split():
            if el[-1].isdigit() and el[0] in "+-0123456789":
                res.append(("NUM", float(el)))
            elif el in self.operations:
                res.append(("OPR", el))
            elif el in "()":
                res.append((el, el))
            else:
                raise InvalidTokenError(f"Невозможно определить токен комбинации: '{el}'")
        return res

    def detokenize(self, tokens: List[Tuple[str, float | str]]) -> str:
        """
        Тут мы детокенизируем последовательность токенов. По сути эта функция обратна токенайзеру. Она нужна, чтобы при
        сборке подвыражения мы могли посчитать через наш же калькулятор.
        """
        res = ""
        for token in tokens:
            value = token[1]
            res += f" {value}"
        return res

    def push(self, x: float) -> None:
        """
        Добавляет в стек значение.
        """
        self.stack.append(x)

    def pop(self) -> float:
        """
        Достает верхнее значение стека.
        """
        if not self.stack:
            raise TooManyOperandsError("Некорректное количество операнд.")
        return self.stack.pop()

    def add(self, a: float, b: float) -> float:
        """
        Сумма элементов.
        """
        return a + b

    def subtract(self, a: float, b: float) -> float:
        """
        Разность элементов.
        """
        return a - b

    def multiply(self, a: float, b: float) -> float:
        """
        Перемножение элементов.
        """
        return a * b

    def divide(self, a: float, b: float) -> float:
        """
        Деление элементов.
        """
        if b != 0:
            return a / b
        else:
            raise Exception(ZeroDivisionError("Деление на ноль."))

    def power(self, a: float, b: float) -> float:
        """
        Возведение в степень.
        """
        return a ** b
