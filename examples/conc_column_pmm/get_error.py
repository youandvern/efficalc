import math


def get_error(output, target, load_span):
    # find the difference between both outputs and their target values
    lambda_diff = output[0] - target[0]
    load_diff = output[3] - target[1]
    return math.sqrt((lambda_diff / (math.pi / 2)) ** 2 + (load_diff / load_span) ** 2)
