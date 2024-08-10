import math


def get_error(output, target):
    # find the difference between both outputs and their target values
    lambda_diff = output[0] - target[0]
    ecc_diff = output[1] - target[1]
    return math.sqrt(lambda_diff**2 + ecc_diff**2)
