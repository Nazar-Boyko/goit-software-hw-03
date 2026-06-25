from time import time
from multiprocessing import Pool, Process, cpu_count



# def factorize(*number):

    
#     all_divisors = []
#     for n in number:
#         all_divisors.append(factorize_one(n))
#     return all_divisors

def factorize_one(number):
    divisors = []

    for i in range(1, int(number**0.5)+1):
        if number % i == 0:
            divisors.append(i)

    return divisors


if __name__ == "__main__":

    numbers = [
    99999937,
    99999935,
    ]


    start1 = time()

    result1 = [
        factorize_one(n)
        for n in numbers
    ]

    end1 = time()


    print("Sync:")

    for res in result1:
        print(res)

    print(end1 - start1)



    with Pool(processes=cpu_count()) as pool:

        start2 = time()

        result2 = pool.map(
            factorize_one,
            numbers
        )

        end2 = time()


    print("Parallel:")

    for res in result2:
        print(res)

    print(end2 - start2)