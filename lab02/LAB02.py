# Лабораторна работа N2 (СиАОД)

# Факториал числа
def factorial(n):
    if n < 0:
        raise ValueError("Число не должно быть отрицательным")

    if n == 0:
        return 1

    return n * factorial(n - 1)

print(factorial(4))

# Словарь, в котором лежат 2 счётчика
CALLS = {"fib_naive": 0, "fib_memo": 0}

# Числа Фибоначчи
def fib_naive(n):
    if n < 0:
        raise ValueError("Номер должен быть неотрицательным")

    CALLS["fib_naive"] = CALLS["fib_naive"] + 1

    if n <= 1:
        return n

    return fib_naive(n - 1) + fib_naive(n - 2)

print("F(5):", fib_naive(5))
print("Количество вызовов:", CALLS["fib_naive"])

# Мемоизация
def fib_memo(n, memo = None):
    if n < 0:
        raise ValueError("Номер должен быть неотрицательным")
    CALLS["fib_memo"] = CALLS["fib_memo"] + 1

    if memo is None:
        memo = {}

    if n in memo:
        return memo[n]

    if n <= 1:
        memo[n] = n
    else:
        memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)

    return memo[n]

print("F(5):", fib_memo(5))
print("Количество вызовов:", CALLS["fib_memo"])

# Эксперимент
print("n | F(n) | Обычная | С запоминанием")

for n in [5, 10, 15, 20, 25, 30]:
    CALLS["fib_naive"] = 0
    CALLS["fib_memo"] = 0

    result_naive = fib_naive(n)
    result_memo = fib_memo(n)

    if result_naive != result_memo:
        raise ValueError("Результаты функций различаются")

    print(
        n,
        result_naive,
        CALLS["fib_naive"],
        CALLS["fib_memo"],
        sep=" | ",
    )

# Ханойские башни
def hanoi(n, src="A", dst="C", aux="B", moves=None):
    if n < 0:
        raise ValueError("Количество дисков должно быть неотрицательным")

    if n == 0:
        return 0

    count = hanoi(n - 1, src, aux, dst, moves)

    if moves is not None:
        moves.append((src, dst))

    count = count + 1
    count = count + hanoi(n - 1, aux, dst, src, moves)

    return count


moves = []
count = hanoi(3, moves=moves)

print("Перемещения:", moves)
print("Количество ходов:", count)

# Динамический массив
class DynamicArray:
    INITIAL_CAPACITY = 4

    def __init__(self):
        self._capacity = self.INITIAL_CAPACITY
        self._size = 0
        self._buffer = [None] * self._capacity
        self.copies = 0

    def __len__(self):
        return self._size

    @property
    def capacity(self):
        return self._capacity

    def _grow(self):
        new_capacity = self._capacity * 2
        new_buffer = [None] * new_capacity

        for i in range(self._size):
            new_buffer[i] = self._buffer[i]
            self.copies = self.copies + 1

        self._buffer = new_buffer
        self._capacity = new_capacity

    def append(self, value):
        if self._size == self._capacity:
            self._grow()

        self._buffer[self._size] = value
        self._size = self._size + 1

    def get(self, index):
        if index < 0 or index >= self._size:
            raise IndexError("Индекс вне границ массива")

        return self._buffer[index]

    def set(self, index, value):
        if index < 0 or index >= self._size:
            raise IndexError("Индекс вне границ массива")

        self._buffer[index] = value

    def pop(self):
        if self._size == 0:
            raise IndexError("Массив пуст")

        value = self._buffer[self._size - 1]
        self._buffer[self._size - 1] = None
        self._size = self._size - 1

        return value

# Стэк
class Stack:
    def __init__(self):
        self._data = DynamicArray()

    def __len__(self):
        return len(self._data)

    def push(self, value):
        self._data.append(value)

    def pop(self):
        return self._data.pop()

    def peek(self):
        if len(self._data) == 0:
            raise IndexError("Стек пуст")

        return self._data.get(len(self._data) - 1)

# Дэк
class _Node:
    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None


class Deque:
    def __init__(self):
        self._head = None
        self._tail = None
        self._size = 0

    def __len__(self):
        return self._size

    def push_front(self, value):
        node = _Node(value)
        node.next = self._head

        if self._head is None:
            self._tail = node
        else:
            self._head.prev = node

        self._head = node
        self._size = self._size + 1

    def push_back(self, value):
        node = _Node(value)
        node.prev = self._tail

        if self._tail is None:
            self._head = node
        else:
            self._tail.next = node

        self._tail = node
        self._size = self._size + 1

    def pop_front(self):
        if self._head is None:
            raise IndexError("Дек пуст")

        node = self._head
        self._head = node.next

        if self._head is None:
            self._tail = None
        else:
            self._head.prev = None

        self._size = self._size - 1
        return node.value

    def pop_back(self):
        if self._tail is None:
            raise IndexError("Дек пуст")

        node = self._tail
        self._tail = node.prev

        if self._tail is None:
            self._head = None
        else:
            self._tail.next = None

        self._size = self._size - 1
        return node.value

# Проверка
dq = Deque()

dq.push_back(10)
dq.push_front(5)
dq.push_back(20)

print(dq.pop_front())
print(dq.pop_back())
print(dq.pop_front())
print("Размер:", len(dq))
