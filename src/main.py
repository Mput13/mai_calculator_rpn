from src.calc import RPNCalculator
from src.exceptions import RPNError


def main() -> None:
    """Тут мы запускаем калькулятор, обрабатываем ввод пользователя и ошибочки"""
    calc = RPNCalculator()

    print("Калькулятор ОПН: введите Q, чтобы выйти")
    while True:
        try:
            line = input("> ").strip()
            if line in ["q", "Q"]:
                break
            if not line:
                continue
            res = calc.solve(line)
            print(res)
        except (RPNError, ZeroDivisionError) as e:
            print(f"{e.__class__.__name__}: {e}")


if __name__ == "__main__":
    main()
