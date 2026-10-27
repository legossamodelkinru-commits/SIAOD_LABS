import json
import math
import random
import statistics
import time
from collections import Counter
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


variant = 19
seed = 30 + variant
project_dir = Path(__file__).resolve().parent
data_dir = project_dir / "data" / "generated"


# 1. Алгоритмы

# Сумма элементов
def array_sum(numbers):
    total = 0

    for number in numbers:
        total = total + number

    return total


# Поиск максимума
def array_max(numbers):
    if len(numbers) == 0:
        raise ValueError("Список пуст")

    maximum = numbers[0]

    for number in numbers:
        if number > maximum:
            maximum = number

    return maximum


# Подсчёт равных пар
def count_equal_pairs(numbers):
    count = 0

    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if numbers[i] == numbers[j]:
                count = count + 1

    return count


# Бинарное возведение в степень
def binary_pow(base, exponent, mod=None):
    if exponent < 0:
        raise ValueError("Показатель должен быть неотрицательным")

    if mod is not None:
        if mod <= 0:
            raise ValueError("Модуль должен быть положительным")
        base = base % mod

    result = 1

    while exponent > 0:
        if exponent % 2 == 1:
            result = result * base
            if mod is not None:
                result = result % mod

        base = base * base
        if mod is not None:
            base = base % mod

        exponent = exponent // 2

    if mod is not None:
        result = result % mod

    return result


# 2. Расчёт наклона графика

def calculate_slope(sizes, times):
    log_sizes = []
    log_times = []

    for size in sizes:
        log_sizes.append(math.log2(size))

    for elapsed in times:
        log_times.append(math.log2(elapsed))

    average_x = sum(log_sizes) / len(log_sizes)
    average_y = sum(log_times) / len(log_times)

    numerator = 0
    denominator = 0

    for i in range(len(sizes)):
        dx = log_sizes[i] - average_x
        dy = log_times[i] - average_y

        numerator = numerator + dx * dy
        denominator = denominator + dx * dx

    return numerator / denominator


# 3. Проверки

assert array_sum([]) == 0
assert array_sum([7]) == 7
assert array_sum([-3, 1, 5]) == 3

assert array_max([7]) == 7
assert array_max([-5, -2, -8]) == -2
assert array_max([4, 4, 4]) == 4

assert count_equal_pairs([]) == 0
assert count_equal_pairs([7]) == 0
assert count_equal_pairs([5, 5, 5]) == 3
assert count_equal_pairs([1, 2, 3]) == 0

assert binary_pow(2, 0) == 1
assert binary_pow(2, 10) == 1024
assert binary_pow(2, 10, 1000) == 24
assert binary_pow(2, 0, 1) == 0

test_arrays = [
    [3, 1, 3],
    [-5, -2, -8],
    [4, 4, 4],
    [7],
    [],
]

for numbers in test_arrays:
    assert array_sum(numbers) == sum(numbers)

    if len(numbers) > 0:
        assert array_max(numbers) == max(numbers)

assert binary_pow(3, 5, 7) == pow(3, 5, 7)
assert binary_pow(2, 10, 1000) == pow(2, 10, 1000)

rng = random.Random(seed)

for test in range(200):
    numbers = []

    for i in range(rng.randint(0, 60)):
        numbers.append(rng.randint(-10, 10))

    assert array_sum(numbers) == sum(numbers)

    if len(numbers) > 0:
        assert array_max(numbers) == max(numbers)

    frequencies = Counter(numbers)
    expected_pairs = 0

    for count in frequencies.values():
        expected_pairs = expected_pairs + count * (count - 1) // 2

    assert count_equal_pairs(numbers) == expected_pairs

    base = rng.randint(-10, 10)
    exponent = rng.randint(0, 30)
    mod = rng.randint(1, 1000)

    assert binary_pow(base, exponent) == pow(base, exponent)
    assert binary_pow(base, exponent, mod) == pow(base, exponent, mod)

try:
    array_max([])
except ValueError:
    pass
else:
    raise AssertionError("Для пустого списка ожидается ValueError")

for base, exponent, mod in [(2, -1, None), (2, 3, 0), (2, 3, -5)]:
    try:
        binary_pow(base, exponent, mod)
    except ValueError:
        pass
    else:
        raise AssertionError("Ожидается ValueError для неверных аргументов")

print("Все проверки пройдены")

# 4. Данные варианта

with open(data_dir / "manifest.json", encoding="utf-8") as file:
    manifest = json.load(file)

if manifest["variant"] != variant:
    raise ValueError("Данные другого варианта")

if manifest["seed"] != seed:
    raise ValueError("Неверный seed")

print("Данные варианта", variant, "проверены")


# 5. Замеры суммы и максимума

sizes = [1000, 3000, 10000, 30000, 100000]
sum_times = []
max_times = []

for size in sizes:
    path = data_dir / f"arrays_random_{size}.txt"

    with open(path, encoding="utf-8") as file:
        text = file.read()

    numbers = []

    for value in text.split():
        numbers.append(int(value))

    if len(numbers) != size:
        raise ValueError(f"В файле {path.name} должно быть {size} чисел")

    array_sum(numbers)

    times = []

    for repeat in range(5):
        start = time.perf_counter()
        result = array_sum(numbers)
        finish = time.perf_counter()

        times.append(finish - start)

    median_time = statistics.median(times)
    sum_times.append(median_time)

    print("Сумма. Размер:", size, "Медиана:", median_time, "секунд")

    array_max(numbers)

    times = []

    for repeat in range(5):
        start = time.perf_counter()
        result = array_max(numbers)
        finish = time.perf_counter()

        times.append(finish - start)

    median_time = statistics.median(times)
    max_times.append(median_time)

    print("Максимум. Размер:", size, "Медиана:", median_time, "секунд")


# График суммы и максимума

plt.plot(sizes, sum_times, marker="o", label="Сумма")
plt.plot(sizes, max_times, marker="o", label="Максимум")

plt.xscale("log")
plt.yscale("log")

plt.xlabel("Количество элементов")
plt.ylabel("Время, секунды")
plt.title("Сумма и поиск максимума")
plt.grid(True, which="both")
plt.legend()

plt.savefig(project_dir / "lab01_linear.png")
plt.close()

# 6. Замеры подсчёта пар

pair_sizes = [500, 1000, 3000, 10000, 30000]
pair_times = []

for size in pair_sizes:
    file_size = size

    if size == 500:
        file_size = 1000

    path = data_dir / f"arrays_dups_{file_size}.txt"

    with open(path, encoding="utf-8") as file:
        text = file.read()

    numbers = []

    for value in text.split():
        numbers.append(int(value))

    if len(numbers) != file_size:
        raise ValueError(f"В файле {path.name} должно быть {file_size} чисел")

    numbers = numbers[:size]

    count_equal_pairs(numbers)

    times = []

    for repeat in range(5):
        start = time.perf_counter()
        result = count_equal_pairs(numbers)
        finish = time.perf_counter()

        times.append(finish - start)

    median_time = statistics.median(times)
    pair_times.append(median_time)

    print("Пары. Размер:", size, "Медиана:", median_time, "секунд")


# График подсчёта пар

plt.plot(pair_sizes, pair_times, marker="o")

plt.xscale("log")
plt.yscale("log")

plt.xlabel("Количество элементов")
plt.ylabel("Время, секунды")
plt.title("Подсчёт пар равных элементов")
plt.grid(True, which="both")

plt.savefig(project_dir / "lab01_pairs.png")
plt.close()

# 7. Замеры бинарного возведения в степень

exponents = [1000, 10000, 100000, 1000000, 10000000]
power_times = []

calls = 20000
mod = 1000000007

for exponent in exponents:
    for call in range(calls):
        binary_pow(3, exponent, mod)

    times = []

    for repeat in range(5):
        start = time.perf_counter()

        for call in range(calls):
            binary_pow(3, exponent, mod)

        finish = time.perf_counter()
        times.append((finish - start) / calls)

    median_time = statistics.median(times)
    power_times.append(median_time)

    print("Показатель:", exponent, "Медиана:", median_time, "секунд")


# График бинарного возведения в степень

log_exponents = []

for exponent in exponents:
    log_exponents.append(math.log2(exponent))

plt.plot(log_exponents, power_times, marker="o")

plt.xlabel("log₂ показателя степени")
plt.ylabel("Время одного вызова, секунды")
plt.title("Бинарное возведение в степень")
plt.grid(True)

plt.savefig(project_dir / "lab01_power.png")
plt.close()


# 8. Вывод наклонов

print("Наклон суммы:", calculate_slope(sizes, sum_times))
print("Наклон максимума:", calculate_slope(sizes, max_times))
print("Наклон пар:", calculate_slope(pair_sizes, pair_times))
