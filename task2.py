from time import time
from multiprocessing import Pool, Process, cpu_count


def get_divisors(number):
    divisors = []
    for i in range(1, number + 1):
        if number % i == 0:
            divisors.append(i)

    return divisors


def factorize_sync(*numbers):
    
    divisors = []
    for number in numbers:
        divisors.append(get_divisors(number))
    
    return divisors


def factorize_parallel(*numbers):

    num_cores = cpu_count()
    with Pool(processes=num_cores) as pool:
        divisors = pool.map(get_divisors,numbers)

    return divisors

if __name__ == "__main__":
    test_data = (128, 255, 99999, 10651060)

    start_time = time()
    a_s, b_s, c_s, d_s = factorize_sync(*test_data)
    sync_duration = time() - start_time
    print(f"Синхронне виконання зайняло: {sync_duration:.4f} секунд")

    start_time = time()
    a, b, c, d = factorize_parallel(*test_data)
    parallel_duration = time() - start_time
    print(f"Паралельне виконання зайняло: {parallel_duration:.4f} секунд")

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1,2,4,5,7,10,14,20,28,35,70,140,76079,152158,304316,380395,532553,760790,1065106,1521580,2130212,2662765,5325530, 10651060,
    ]

    print("\n[Успіх!] Всі assert-перевірки пройдено успішно.")