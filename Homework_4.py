# 1. Напишите функцию для транспонирования матрицы
# Пример:
# [[1, 2, 3], [4, 5, 6]] -> [[1,4], [2,5], [3, 6]]

def matrix(list_: list[list]) -> list[list]:
    return list(map(list, zip(*list_)))
  
print(matrix([[3, 4, 5], [6, 7, 8]]))


# Напишите функцию принимающую на вход только ключевые
# параметры и возвращающую словарь, где ключ — значение
# переданного аргумента, а значение — имя аргумента. Если
# ключ не хешируем, используйте его строковое представление.

def dict_from_args(**kwargs):
    equipments = dict()
    for k, v in kwargs.items():
        if isinstance(v, (list, dict, set, bytearray)):
            v = str(v)
        equipments[v] = k
    return equipments


print(dict_from_args(desktop='DellOptiplex750', laptop={'DellLatitude1200': 3, 'DellLatitude1400': 2}, mobile=['SamsungET100', 'XiaomiM5s', 'RedmiNote10'], dect={'PanasonicEB1275', 'SamsungDR7025'}))


# Возьмите задачу о банкомате из семинара 2.
# Разбейте её на отдельные операции — функции.
# Дополнительно сохраняйте все операции поступления и снятия средств в список.


class Bank:
    _BALANCE = 0
    _MIN = 50
    _MAX = 5000000
    _COMMISSION = 0.015
    _BONUS = 0.03
    _TAX = 0.10
    _OPERATION: int
    _OPERATIONS: list[str]

    def __init__(self):
        self._OPERATION = 0
        self._OPERATIONS = dict()

    def _in(self, cash: int, tax: int) -> tuple[int, int] | None:
        if cash % self._MIN == 0:
            self._BALANCE += cash + tax
            self._OPERATION += 1
            self._OPERATIONS[f'+ {cash + tax}'] = 'Пополнение'
            return self._BALANCE, self._OPERATION
        else:
            return None

    def _out(self, cash: int, commission: int, tax: int) -> tuple[int, int] | None:
        if cash % self._MIN == 0 and self._BALANCE > 0 and self._BALANCE - (cash + commission + tax) >= 0:
            self._BALANCE -= cash + commission + tax
            self._OPERATION += 1
            self._OPERATIONS[f'- {cash + commission + tax}'] = 'Снятие'
            return self._BALANCE, self._OPERATION
        else:
            return None

    def _check_commission(self, cash: int) -> int:
        sum_commission = cash * self._COMMISSION
        _MAX = 600
        _MIN = 30
        if sum_commission > _MAX:
            sum_commission = _MAX
        elif sum_commission < _MIN:
            sum_commission = _MIN
        else:
            sum_commission = int(sum_commission)
        return sum_commission

    def _check_tax(self, cash: int) -> int:
        if cash >=self._MAX:
            print(f'\nВнимание был снят налог на богатство в размере {cash * self._TAX}')
            return cash * self._TAX
        else:
            return 0

    def _exit(self):
        return "Всего доброго, приходите к нам еще"

    def add_bonus(self):
            self._BALANCE += self._BALANCE * self._BONUS
            return f'Поздравляем, вы получили бонус за каждую 3-юю операцию в нашем банке . ' \
                   f'На ваш счет было зачислено: {int(self._BALANCE * self._BONUS)}\n'

    def _show_operations(self) -> None:
        for summ, op in self._OPERATIONS.items():
            print(f'{summ} - {op}')

    def start(self, mode: str, cash: int = 0) -> str:
        if self._OPERATION % 3 == 0:
             print(self.add_bonus())
        tax = self._check_tax(cash)
        match mode:
            case "in":
                self._in(cash=cash, tax=tax)
                return f"Средства были зачислены сумма: {cash}, баланс: {int(self._BALANCE)}"
            case "out":
                commission = self._check_commission(cash=cash)
                data = self._out(cash=cash, commission=commission, tax=tax)
                if data:
                    return f"Операция осуществлена успешно, сумма: {cash}, коммисия: {commission}, " \
                           f"баланс: {int(self._BALANCE)}"
                else:
                    return "Нехватает средств"

            case "show":
                self._show_operations()

            case "exit":
                return self._exit()


bank = Bank()
print(bank.start(mode='in', cash=4000000))
print(bank.start(mode='in', cash=100000))
print(bank.start(mode='out', cash=100000))
print(bank.start(mode='in', cash=100000))
print(bank.start(mode='in', cash=1000000))
print(bank.start(mode='in', cash=2000000))
print(bank.start(mode='out', cash=5000000))
print(bank.start(mode='show'))
