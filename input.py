import math


def fx(t: float) -> float:
    """
    uninterrupted function
    :param t:
    :return:
    """
    return 1 / t


def fy(t: float) -> float:
    """
    uninterrupted function
    :param t:
    :return:
    """
    return math.sin(2 * t * math.pi)


'''
prepare function data using param interpolation with dynamic shift 
when distance increase your segment length and decrease shift by half until length won't be less then
segment length 
'''

start_shift = 0.01
""" start shift of parameter for naive approach"""

max_length_difference = 0.0001
""" accuracy for naive approach"""

limits = [-8, -8, 8, 8]

t0 = 0.5
""" min parameter value for fx fy functions"""

t_max = 3
""" max parameter value for fx fy functions"""

interpolation_step = 0.00001
"""interpolation step of parameter for sampling"""

segment_length = 0.5
"""length of segment for fast interpolation by length or for naive approach"""

output_size = 40
"""max count of point after interpolation"""

create_csv = True
