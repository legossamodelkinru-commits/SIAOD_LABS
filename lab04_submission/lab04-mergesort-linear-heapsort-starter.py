#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ЛР 4. MergeSort, Counting, Radix и HeapSort: оценка производительности — стартовая заготовка.

Заготовка — это каркас, а не решение: заполните все TODO самостоятельно
в соответствии с КИМ-04 и правилами использования генеративного ИИ
(docs/ai-verification.md). QuickSort перенесите из собственной ЛР 3.

Запуск: python lab04-mergesort-linear-heapsort-starter.py --variant N
"""
from __future__ import annotations

import argparse
import random
import statistics
import time

# ---------------------------------------------------------------------------
# 1. Сортировки (реализуются вручную; sorted() используется только как эталон)
# ---------------------------------------------------------------------------


def merge(left: list, right: list, key) -> list:
    """Стабильное слияние двух отсортированных списков в новый список.

    Стабильность: при равенстве ключей элемент из left идёт раньше.
    Ожидаемая сложность: TODO (обосновать в отчёте).
    """
    # TODO: два индекса, сравнение key(left[i]) <= key(right[j])
    result = []
    i = 0
    j = 0
    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result



def merge_sort(a: list, key=lambda x: x) -> list:
    """MergeSort: возвращает новый отсортированный список. Ожидаемая сложность: TODO."""
    # TODO: рекурсивное деление пополам + merge()
    if len(a) <= 1:
        return a.copy()

    mid = len(a) // 2
    left = merge_sort(a[:mid], key)
    right = merge_sort(a[mid:], key)

    return merge(left, right, key)


def counting_sort(a: list[int], key_max: int) -> list[int]:
    """Устойчивая сортировка подсчётом: ключи — целые из диапазона [0, key_max].

    Схема: массив счётчиков -> префиксные суммы -> расстановка с конца.
    Ожидаемые время и память: TODO — выразить через n и k = key_max + 1;
    ограничение диапазона ключей обсудить в отчёте.
    """
    # TODO: реализовать; проход расстановки — с конца массива (иначе теряется устойчивость)
    if not a:
        return []

    counts = [0] * (key_max + 1)

    for value in a:
        counts[value] += 1

    for i in range(1, len(counts)):
        counts[i] += counts[i - 1]

    result = [0] * len(a)

    for value in reversed(a):
        counts[value] -= 1
        result[counts[value]] = value

    return result


def radix_sort_lsd(a: list[int]) -> list[int]:
    """RadixSort LSD по десятичным разрядам, неотрицательные целые.

    Поверх устойчивой поразрядной counting-сортировки: от младшего разряда
    к старшему. Ожидаемая сложность: TODO — выразить через n и число разрядов d.
    """
    # TODO: цикл по разрядам (exp = 1, 10, 100, ...) с устойчивой сортировкой
    # по цифре (a[i] // exp) % 10; объяснить, почему без устойчивости
    # внутреннего прохода алгоритм неверен
    if not a:
        return []

    result = a.copy()
    max_value = max(result)
    exp = 1

    while max_value // exp > 0:
        counts = [0] * 10

        for value in result:
            digit = (value // exp) % 10
            counts[digit] += 1

        for i in range(1, 10):
            counts[i] += counts[i - 1]

        output = [0] * len(result)
        for value in reversed(result):
            digit = (value // exp) % 10
            counts[digit] -= 1
            output[counts[digit]] = value

        result = output
        exp *= 10

    return result


def sift_down(a: list[int], i: int, n: int) -> None:
    """Просейка вниз элемента i в куче a[0:n] (max-heap), на месте."""
    # TODO: спуск с обменом с большим из потомков, пока нарушено свойство кучи
    while True:
        left = 2 * i + 1
        right = 2 * i + 2
        largest = i

        if left < n and a[left] > a[largest]:
            largest = left
        if right < n and a[right] > a[largest]:
            largest = right

        if largest == i:
            return

        a[i], a[largest] = a[largest], a[i]
        i = largest

def heap_sort(a: list[int]) -> None:
    """HeapSort in-place: сортирует список a на месте, без вспомогательного массива.

    Схема: построение max-кучи просейками вниз (снизу вверх, O(n)),
    затем обмен вершины с последним элементом и просейка. Сложность: TODO.
    """
    # TODO: построение кучи + фаза извлечения максимумов
    n = len(a)

    for i in range(n // 2 - 1, -1, -1):
        sift_down(a, i, n)

    for end in range(n - 1, 0, -1):
        a[0], a[end] = a[end], a[0]
        sift_down(a, 0, end)


def sort_key(item):
    if isinstance(item, tuple):
        return item[0]
    return item


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



# ---------------------------------------------------------------------------
# 2. Верификация: инварианты + сверка с эталоном sorted()
#    (шаги 1–3 методики docs/ai-verification.md)
# ---------------------------------------------------------------------------


def self_check() -> None:
    """Граничные и типовые случаи, стабильность, сверка с эталоном sorted()."""
    # Граничные случаи: пустой массив, один элемент, все элементы равны
    assert merge_sort([]) == []
    assert merge_sort([7]) == [7]
    assert merge_sort([5, 5, 5]) == [5, 5, 5]
    assert counting_sort([], key_max=10) == []
    assert radix_sort_lsd([0]) == [0]
    single = [42]
    heap_sort(single)
    assert single == [42]

    # Стабильность слияния: пары (ключ, порядковый номер); эталон sorted() стабилен,
    # поэтому при равных ключах порядок номеров обязан совпасть
    rng = random.Random(0)
    pairs = [(rng.randint(0, 5), i) for i in range(100)]
    assert merge_sort(pairs, key=lambda p: p[0]) == sorted(pairs, key=lambda p: p[0])

    # Случайные тесты: инвариант перестановки + сверка с эталоном
    for _ in range(200):
        a = [rng.randint(0, 999) for _ in range(rng.randint(0, 60))]
        expected = sorted(a)
        assert quick_sort(a, rng=random.Random(49)) == expected
        assert merge_sort(a) == expected
        assert counting_sort(a, key_max=999) == expected
        assert radix_sort_lsd(a) == expected
        buf = list(a)
        heap_sort(buf)
        assert buf == expected
        assert sorted(buf) == expected  # выход — перестановка входа
    print("self_check: OK")


# ---------------------------------------------------------------------------
# 3. Бенчмарк (методика — docs/reproducibility.md)
# ---------------------------------------------------------------------------

SIZES = [1_000, 3_000, 10_000, 30_000, 100_000]
REPEATS = 5
SMALL_KEY_MAX = 100        # узкий диапазон: counting уместен
WIDE_KEY_MAX = 10**9       # широкий диапазон: counting теряет смысл (обсудить в отчёте)


def make_datasets(rng: random.Random, n: int) -> dict[str, list[int]]:
    """Массивы разных распределений и диапазонов ключей для размера n."""
    almost = list(range(n))
    for _ in range(max(1, n // 100)):  # ~1 % случайных обменов
        i, j = rng.randrange(n), rng.randrange(n)
        almost[i], almost[j] = almost[j], almost[i]
    return {
        "random_wide": [rng.randint(0, WIDE_KEY_MAX) for _ in range(n)],
        "random_small": [rng.randint(0, SMALL_KEY_MAX) for _ in range(n)],
        "sorted": list(range(n)),
        "reversed": list(range(n, 0, -1)),
        "almost_sorted": almost,
    }


def bench(fn, data: list[int]) -> float:
    """Медиана времени fn на копии data по REPEATS запускам, с прогревом.

    Каждый запуск получает свежую копию: сортировка на месте не должна
    превращать последующие запуски в сортировку уже отсортированного массива.
    """
    fn(list(data))  # прогрев — не учитывается
    times = []
    for _ in range(REPEATS):
        buf = list(data)
        t0 = time.perf_counter()
        fn(buf)
        times.append(time.perf_counter() - t0)
    return statistics.median(times)


def run_benchmarks(seed: int) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    rng = random.Random(seed)
    pivot_rng = random.Random(seed)
    algorithms = [
        ("MergeSort", merge_sort),
        ("CountingSort", lambda a: counting_sort(a, key_max=max(a))),
        ("RadixSort", radix_sort_lsd),
        ("HeapSort", heap_sort),
        ("QuickSort", lambda a: quick_sort(a, rng=pivot_rng)),
        ("sorted()", sorted),
    ]
    titles = {
        "random_wide": "Случайный, широкий диапазон",
        "random_small": "Случайный, узкий диапазон",
        "sorted": "Отсортированный",
        "reversed": "Обратный",
        "almost_sorted": "Почти отсортированный",
    }
    results = {name: {} for name in titles}

    for n in SIZES:
        for distribution, data in make_datasets(rng, n).items():
            for name, fn in algorithms:
                if name == "CountingSort" and distribution == "random_wide":
                    print(f"{distribution} | {n} | {name} | пропуск: широкий диапазон")
                    continue

                elapsed = bench(fn, data)
                results[distribution].setdefault(name, []).append(elapsed)
                print(f"{distribution} | {n} | {name} | {elapsed:.8f} с", flush=True)

    fig, axes = plt.subplots(2, 3, figsize=(15, 8))

    for ax, (distribution, title) in zip(axes.flat, titles.items()):
        for name, times in results[distribution].items():
            ax.loglog(SIZES, times, marker="o", label=name)

        ax.set_title(title)
        ax.set_xlabel("Размер списка")
        ax.set_ylabel("Время, с")
        ax.grid(True, which="both", alpha=0.3)
        ax.legend(fontsize=8)

    axes.flat[-1].axis("off")
    fig.tight_layout()
    fig.savefig("lab04_times.png", dpi=150)
    plt.close(fig)
    print("График сохранён: lab04_times.png")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--variant", type=int, required=True, help="номер варианта")
    args = ap.parse_args()
    seed = 30 + args.variant
    random.seed(seed)
    self_check()
    run_benchmarks(seed)


if __name__ == "__main__":
    main()
