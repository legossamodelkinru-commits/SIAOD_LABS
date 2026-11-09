import random
from statistics import median
from time import perf_counter

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from LAB03 import bubble_sort, insertion_sort, selection_sort, quick_sort


SEED = 49  # Вариант 19: 30 + 19
REPEATS = 5

SIMPLE_SIZES = [500, 1000, 2000, 4000, 8000]
QUICK_SIZES = [1000, 3000, 10000, 30000, 100000]

ALGORITHMS = [
    ("Пузырёк", bubble_sort, SIMPLE_SIZES),
    ("Вставки", insertion_sort, SIMPLE_SIZES),
    ("Выбор", selection_sort, SIMPLE_SIZES),
    ("QuickSort", quick_sort, QUICK_SIZES),
]


def make_inputs(n):
    rng = random.Random(SEED + n)
    values = [rng.randint(-1_000_000, 1_000_000) for _ in range(n)]
    ordered = sorted(values)

    return {
        "Случайный": values,
        "Отсортированный": ordered,
        "Обратный": ordered[::-1],
    }


def measure(sort, values):
    def run():
        if sort is quick_sort:
            return sort(values, random.Random(SEED))
        return sort(values)

    result = run()  # Прогрев: время этого запуска не записываем
    times = []

    for _ in range(REPEATS):
        start = perf_counter()
        run()
        times.append(perf_counter() - start)

    if sort is quick_sort:
        ordered = result
        comparisons, moves = "-", "-"
    else:
        ordered, comparisons, moves = result

    if ordered != sorted(values):
        raise ValueError(f"Ошибка сортировки: {sort.__name__}")

    return median(times), comparisons, moves


def main():
    all_sizes = sorted(set(SIMPLE_SIZES + QUICK_SIZES))
    inputs = {n: make_inputs(n) for n in all_sizes}

    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    input_types = ["Случайный", "Отсортированный", "Обратный"]

    print("Алгоритм | Вход | n | Медиана, с | Сравнения | Обмены/сдвиги")

    for ax, input_type in zip(axes, input_types):
        for name, sort, sizes in ALGORITHMS:
            times = []

            for n in sizes:
                elapsed, comparisons, moves = measure(sort, inputs[n][input_type])
                times.append(elapsed)
                print(
                    f"{name} | {input_type} | {n} | {elapsed:.8f} | "
                    f"{comparisons} | {moves}",
                    flush=True,
                )

            ax.loglog(sizes, times, marker="o", label=name)

        ax.set_title(input_type)
        ax.set_xlabel("Размер списка, n")
        ax.set_ylabel("Время, с")
        ax.grid(True, which="both", alpha=0.3)
        ax.legend()

    fig.tight_layout()
    fig.savefig("lab03_times.png", dpi=150)
    print("График сохранён: lab03_times.png")


if __name__ == "__main__":
    main()