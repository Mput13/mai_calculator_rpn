class RPNError(Exception):
    """Базовая ошибка калькулятора."""
    pass


class InvalidTokenError(RPNError):
    """Поднимается, когда мы не можем обработать токен."""
    pass


class TooManyOperandsError(RPNError):
    """Поднимается, когда в стеке нет значений, а операнды остались."""
    pass


class NotEnoughOperandsError(RPNError):
    """Поднимается когда в стеке осталось несколько значений, а все операнды обработаны."""
    pass


class WrongBracketCombinationError(RPNError):
    """Поднимается, когда напутали со скобочками."""
    pass
