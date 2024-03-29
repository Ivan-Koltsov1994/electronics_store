import csv
from scr.errors import InstantiateCSVError


class Product:
    """Класс для работы с продуктами"""
    pay_rate = 1  # атрибут устанавливает уровень цен
    all = []  # атрибут для хранения созданных экземпляров класса

    def __new__(cls, *args, **kwargs):
        print("Создается новый экземпляр Product.")
        return super().__new__(cls)

    def __init__(self, name, price, amount):
        print("Инициализируется новый экземпляр Product.")
        self.__name = name
        self.price = price
        self.amount = amount
        self.all.append(self)
        super().__init__()  # при множественном наследовании "пробрасываем" на следующий класс

    def __repr__(self):
        return f'Товар: {self.__name}, цена: {self.price}, в наличии: {self.amount}'

    def __str__(self):
        return f'Товар: {self.__name}'

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str) -> None:
        """Возвращает имя товара, при превышении 10 символов возвращает исключение """
        if len(name) <= 10:
            self.__name = name
        else:
            raise Exception("Название не может быть длиннее 10 символов.")

    def apply_discount(self):
        """Метод возвращает общую стоимость конкретного товара в магазине"""
        self.price = self.price * self.pay_rate

    def calculate_total_price(self):
        """Метод возвращает цену товара с установленной скидкой"""
        total = self.price * self.amount
        return total

    @classmethod
    def instantiate_from_csv(cls, path) -> None:
        """Метод cчитывает данные из csv-файла и создает экземпляры класса,
        инициализируя их данными из файла"""
        items = []
        try:
            with open(path, 'r', encoding='windows-1251', newline='') as csvfile:
                list = csv.DictReader(csvfile)
                for row in list:
                    if list == ['name', 'price', 'quantity']:
                        items.append(cls(row['name'], int(row['price']), int(row['quantity'])))
                    else:
                        raise InstantiateCSVError
        except FileNotFoundError:
            print(f"По указанному пути  файл item.csv отсутствует")

        except InstantiateCSVError:
            print("Файл item.csv поврежден")

    @staticmethod
    def is_integer_num(num):
        """Метод проверяет, является ли число (например, полученное из csv-файла) целым, если нет, то возвращает в
        виде целого """
        if isinstance(num, int):
            return True
        if isinstance(num, float):
            return num.is_integer()
