import random
from collections import Counter

# Сортировка
def sort_key(item):
    if isinstance(item, tuple):
        return item[0]
    return item

# Сортировка пузырьком
def bubble_sort(a):
    numbers = a.copy()
    comparisons = 0
    swaps = 0

    for end in range(len(numbers) - 1, 0, -1):
        swapped = False

        for i in range(end):
            comparisons += 1

            if sort_key(numbers[i]) > sort_key(numbers[i + 1]):
                numbers[i], numbers[i + 1] = numbers[i + 1], numbers[i]
                swaps += 1
                swapped = True

        if not swapped:
            break

    return numbers, comparisons, swaps


print("Сортировка пузырьком:")
print(bubble_sort([3, 1, 2]))
print(bubble_sort([1, 2, 3]))

# Сортировка вставками
def insertion_sort(a):
    numbers = a.copy()
    comparisons = 0
    shifts_right = 0

    for i in range(1, len(numbers)):
        value = numbers[i]
        j = i - 1

        while j >= 0:
            comparisons += 1

            if numbers[j] <= value:
                break

            numbers[j + 1] = numbers[j]
            shifts_right += 1
            j -= 1

        numbers[j + 1] = value

    return numbers, comparisons, shifts_right


print("Сортировка вставками:")
print(insertion_sort([3, 1, 2]))
print(insertion_sort([1, 2, 3]))

# Сортировка выбором
def selection_sort(a):
    numbers = a.copy()
    comparisons = 0
    swaps = 0

    for i in range(len(numbers) - 1):
        min_index = i

        for j in range(i + 1, len(numbers)):
            comparisons += 1

            if sort_key(numbers[j]) < sort_key(numbers[min_index]):
                min_index = j

        if min_index != i:
            numbers[i], numbers[min_index] = numbers[min_index], numbers[i]
            swaps += 1

    return numbers, comparisons, swaps


print("Сортировка выбором:")
print(selection_sort([3, 1, 2]))
print(selection_sort([1, 2, 3]))

# Разбиение
def partition(numbers, lo, hi, rng):
    pivot_index = rng.randrange(lo, hi)
    pivot = numbers[pivot_index]
    numbers[pivot_index], numbers[hi - 1] = numbers[hi - 1], numbers[pivot_index]

    boundary = lo

    for i in range(lo, hi - 1):
        if sort_key(numbers[i]) < sort_key(pivot):
            numbers[i], numbers[boundary] = numbers[boundary], numbers[i]
            boundary += 1

    numbers[boundary], numbers[hi - 1] = numbers[hi - 1], numbers[boundary]
    return boundary


numbers = [4, 1, 3, 2, 5]
position = partition(numbers, 0, len(numbers), random.Random(49))

print("Разбиение:")
print("После разбиения:", numbers)
print("Опорное число:", numbers[position])

# QuickSort
def quick_sort(a, rng=None):
    numbers = a.copy()

    if rng is None:
        rng = random.Random()

    pending = [(0, len(numbers))]

    while pending:
        lo, hi = pending.pop()

        if hi - lo <= 1:
            continue

        pivot_position = partition(numbers, lo, hi, rng)

        pending.append((lo, pivot_position))
        pending.append((pivot_position + 1, hi))

    return numbers


print("QuickSort")
print("Полный QuickSort:", quick_sort([4, 1, 3, 2, 5], random.Random(49)))

# Проверка
def check_sorts():
    test_cases = [[], [7], [5, 5, 5], [1, 2, 3], [3, 2, 1]]
    rng = random.Random(49)

    for _ in range(300):
        numbers = []
        for _ in range(rng.randint(0, 80)):
            numbers.append(rng.randint(-100, 100))
        test_cases.append(numbers)

    algorithms = [bubble_sort, insertion_sort, selection_sort, quick_sort]

    for sort in algorithms:
        for numbers in test_cases:
            original = numbers.copy()

            if sort is quick_sort:
                result = sort(numbers, random.Random(49))
            else:
                result, comparisons, changes = sort(numbers)

            for i in range(len(result) - 1):
                if result[i] > result[i + 1]:
                    raise ValueError(f"{sort.__name__}: нарушен порядок")

            if Counter(result) != Counter(original):
                raise ValueError(f"{sort.__name__}: изменился набор элементов")

            if result != sorted(original) or numbers != original:
                raise ValueError(f"{sort.__name__}: неверный результат или изменён вход")

        print(sort.__name__, "— проверки пройдены")


check_sorts()

# Демонстрация
pairs = [(2, "А"), (2, "Б"), (1, "В")]

print("Пузырёк:", bubble_sort(pairs)[0])
print("Вставки:", insertion_sort(pairs)[0])
print("Выбор:", selection_sort(pairs)[0])
print("QuickSort:", quick_sort(pairs, random.Random(0)))
print("Проверка ключа:", bubble_sort([(2, "Б"), (2, "А")])[0])
print("Проверка выбора:", selection_sort([(2, "А"), (2, "Б"), (1, "В")])[0])