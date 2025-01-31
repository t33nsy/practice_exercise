class DoubleHashingMap:
    def __init__(self, initial_capacity=8):
        self.capacity = initial_capacity  # Размер таблицы (должен быть степенью 2 для эффективности)
        self.size = 0  # Количество элементов в таблице
        self.table = [None] * self.capacity
        self.deleted = object()  # Флаг удаленного элемента

    def _hash1(self, key) -> int:
        """Первая хэш-функция

        Args:
            key: ключ для хэширования

        Returns:
            int: полученный хэш
        """
        return hash(key) % self.capacity

    def _hash2(self, key) -> int:
        """Вторая хэш-функция, гарантирующая нечетное смещение для того, чтобы точно пройти всю таблицу

        Args:
            key: ключ

        Returns:
            int: полученный хэш
        """
        return 1 + (hash(key) % (self.capacity - 1))

    def _probe(self, key, i) -> int:
        """Вычисляет индекс с учетом двойного хэширования (пробирование)

        Args:
            key: ключ
            i: сдвиг при пробировании

        Returns:
            int: индекс
        """
        return (hash(key) + i * hash(key)) % self.capacity

    def insert(self, key, value) -> None:
        """Вставка ключа и значения в таблицу

        Args:
            key: ключ
            value: значение

        Raises:
            RuntimeError: ошибка вставки
        """
        if self.size >= self.capacity // 2:  # Перехеширование при заполнении 50%
            self._resize()

        for i in range(self.capacity):
            index = self._probe(key, i)
            if self.table[index] is None or self.table[index] is self.deleted:
                self.table[index] = (key, value)
                self.size += 1
                return
            # Если ключ уже существует, обновляем значение
            if self.table[index][0] == key:
                self.table[index] = (key, value)
                return

        raise RuntimeError("Hash table insertion failed")

    def search(self, key):
        """Поиск значения по ключу

        Args:
            key: ключ для поиска

        Returns:
            (Any | None): значение, если ключ найден, иначе None
        """
        for i in range(self.capacity):
            index = self._probe(key, i)
            if self.table[index] is None:
                return None
            if self.table[index] is not self.deleted and self.table[index][0] == key:
                return self.table[index][1]
        return None

    def delete(self, key) -> None:
        """Удаление элемента по ключу

        Args:
            key: ключ для удаления
        """
        for i in range(self.capacity):
            index = self._probe(key, i)
            if self.table[index] is None:
                return
            if self.table[index] is not self.deleted and self.table[index][0] == key:
                self.table[index] = self.deleted
                self.size -= 1
                return

    def _resize(self) -> None:
        """Ресайзинг таблицы, перехеширование с увеличением размера таблицы"""
        old_table = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.size = 0

        for entry in old_table:
            if entry is not None and entry is not self.deleted:
                self.insert(entry[0], entry[1])

    def __str__(self) -> str:
        """Получение удобного вида таблицы

        Returns:
            str: строковое представление таблицы
        """
        return (
            "{"
            + ", ".join(
                f"{k}" for k in self.table if k is not None and k is not self.deleted
            )
            + "}"
        )


# класс-обертка над хэшмапой для удобного использования с помощью переопределенных операторов
class MyDict:
    def __init__(self):
        self.map = DoubleHashingMap()

    def __getitem__(self, key):
        """Магический метод получения по ключу (arr[key])

        Args:
            key: ключ

        Returns:
            (Any | None): значение, если ключ найден, иначе None
        """
        return self.map.search(key)

    def __setitem__(self, key, value) -> None:
        """Магический метод для вставки по ключу (arr[key] = value)

        Args:
            key: ключ
            value: значение
        """
        self.map.insert(key, value)

    def __delitem__(self, key) -> None:
        """Магический метод для удаления по ключу (del)

        Args:
            key: ключ
        """
        self.map.delete(key)

    def __contains__(self, key) -> bool:
        """Магический метод проверки наличия по ключу (key in map)

        Args:
            key (_type_): _description_

        Returns:
            bool: _description_
        """
        return self.map.search(key) is not None

    def __str__(self) -> str:
        """Магический метод получения строкового представления таблицы

        Returns:
            str: строковое представление таблицы
        """
        return str(self.map)


# Пример использования
if __name__ == "__main__":
    map = DoubleHashingMap()
    map.insert("apple", 10)
    map.insert("banana", 20)
    map.insert("orange", 30)
    map.insert("grape", 40)
    map.insert(1, 40)

    print("Initial map:", map)

    print("Search for 'apple':", map.search("apple"))
    print("Search for 'banana':", map.search("banana"))

    map.delete("banana")
    print("Map after deleting 'banana':", map)

    map.insert("kiwi", 50)
    print("Map after inserting 'kiwi':", map)

    # проверка работоспособности обертки
    print("-------------")
    dictr = MyDict()
    dictr["apple"] = 10
    dictr["banana"] = 20
    dictr["orange"] = 30
    dictr["grape"] = 40
    dictr[1] = 40
    print(dictr)
    print("Search for 'apple':", dictr["apple"])
    print("Search for 'banana':", dictr["banana"])
    del dictr["banana"]
    print("Map after deleting 'banana':", dictr)
    dictr["kiwi"] = 50
    print("Map after inserting 'kiwi':", dictr)

    # проверка размера побольше
    map2 = DoubleHashingMap()
    for i in range(100000):
        map2.insert(i, i)
