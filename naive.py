from functools import reduce
import numpy as np
import math
from input import start_shift, max_length_difference, fx, fy, t_max, segment_length, t0


def length(x0: float, y0: float, x1: float, y1):
    return math.sqrt(math.pow(x1 - x0, 2) + math.pow(y0 - y1, 2))


def interpolate_by_length():
    x = []
    y = []

    shift = start_shift
    t = t0
    previous_xi = fx(t)
    previous_yi = fy(t)
    current_segment_length = 0
    while t <= t_max and shift > 0:
        previous_segment_length = current_segment_length
        t_start = t
        t += shift
        x.append(previous_xi)
        y.append(previous_yi)
        xi = fx(t)
        yi = fy(t)
        current_segment_length = length(previous_xi, previous_yi, xi, yi)

        # calibrate shit of t

        diff = math.fabs(current_segment_length - segment_length)
        pre_diff = diff + 1
        try_add = False
        while math.fabs(current_segment_length - segment_length) > max_length_difference and shift > 0:
            # try add or try diff until difference decreases
            while pre_diff > diff > max_length_difference and shift > 0:
                if try_add:
                    t -= shift
                else:
                    t += shift

                pre_diff = diff
                xi = fx(t)
                yi = fy(t)
                current_segment_length = length(previous_xi, previous_yi, xi, yi)
                diff = math.fabs(current_segment_length - segment_length)

            if diff > max_length_difference:
                shift /= 2
                try_add = not try_add
                pre_diff = diff + 1
            else:
                break

        if len(x) == 1:
            shift = math.fabs(t0 - t)
        else:
            shift = math.fabs(t - t_start)

        print('shift of t= ', shift, ' current_length = ', current_segment_length)
        if previous_segment_length == current_segment_length:
            print('can`t achieve accuracy, break evaluation')
            break
        previous_xi, xi = xi, previous_xi
        previous_yi, yi = yi, previous_yi

    print('count of points = ', len(x))
    return {'x': x, 'y': y}


def smooth(f, start, period, step):
    values = [f(t) / period for t in np.linspace(start, start + period, math.trunc(period / step))]
    return reduce((lambda x, y: x + y), values) / len(values)
