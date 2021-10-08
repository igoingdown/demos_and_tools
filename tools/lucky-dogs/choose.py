#!/usr/bin/python3

"""
===============================================================================
author: 赵明星
desc:   我们一起来抓阄。
===============================================================================
"""


import numpy as np


def choose_lucky_dog(candidates, total_dog_num):
    dogs = []
    while len(dogs) < total_dog_num:
        dog_candidate = np.random.randint(1, len(candidates))
        if dog_candidate not in dogs:
            dogs.append(dog_candidate)
    return [candidates[lucky_dog] for lucky_dog in dogs]


def choose_a_luck_num(low, high):
    return np.random.randint(low, high)


if __name__ == "__main__":
    print(choose_a_luck_num(50, 200))

