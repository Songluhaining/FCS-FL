import math

import numpy as np

from methods.mutual_information import su_calculation

import numpy as np


def softmax(x):
    c = np.max(x)
    exp_a = np.exp(x - c)  # 溢出对策
    sum_exp_a = np.sum(exp_a)
    y = exp_a / sum_exp_a

    return y


