import random
import numpy as np
from statistics import mean

# Using "random" to create a dataset
def create_dataset(hm, variance, step=2, correlation=False):
    val = 1
    sy = []
    for i in range(hm):
        y = val + random.randrange(-variance, variance)
        sy.append(y)
        if correlation and correlation == 'pos':
            val += step
        elif correlation and correlation == 'neg':
            val -= step

    sx = [i for i in range(len(sy))]

    return np.array(sx, dtype=np.float64), np.array(sy, dtype=np.float64)


# finding best fit slope and intercept of dataset
def best_fit_slope_and_intercept(sx, sy):
    m = (((mean(sx) * mean(sy)) - mean(sx * sy)) /
         ((mean(sx) * mean(sx)) - mean(sx * sx)))

    b = mean(sy) - m * mean(sx)

    return m, b


# dataset - coefficient of determination
def coefficient_of_determination(sy_orig, sy_line):
    y_mean_line = [mean(sy_orig) for y in sy_orig]

    squared_error_regr = sum((sy_line - sy_orig) * (sy_line - sy_orig))
    squared_error_y_mean = sum((y_mean_line - sy_orig) * (y_mean_line - sy_orig))

    print(squared_error_regr)
    print(squared_error_y_mean)

    r_squared = 1 - (squared_error_regr / squared_error_y_mean)

    return r_squared


def get_result():
    sx, sy = create_dataset(20, 10, 3)
    m, b = best_fit_slope_and_intercept(sx, sy)
    regression_line = [(m * x) + b for x in sx]
    r_squared = coefficient_of_determination(sy, regression_line)
    print('Rsquared result: ')
    return r_squared