import time
from functools import reduce
import math
import matplotlib.pyplot as plt
import numpy as np
from input import fx, fy, t_max, segment_length, t0, max_length_difference, interpolation_step, start_shift, limits, \
    output_size
import algorithm as alg


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


def __init__():
    plt.xticks(np.arange(limits[0], limits[2], 1))
    plt.yticks(np.arange(limits[1], limits[3], 1))
    plt.figure(1)

    '''
    plt.plot(params,
             [smooth(
                 lambda x: math.sin(200 / x),
                 t,
                 0.5,
                 0.1
             ) for t in params],
             '-')
    '''
    start_time = time.time()
    int_points = alg.fast_len_interpolation(fx, fy, t0, t_max, segment_length, interpolation_step, output_size)
    total_time = int(round((time.time() - start_time) * 1000))
    points = alg.sampling(fx, fy, t0, t_max, interpolation_step)
    print('fast interpolation:')
    print('1) count of point after sampling: ', len(points))
    print('2) count of points after interpolation by length: ', len(int_points))
    print('3) evaluation time milis: ', total_time, ' ms')
    ax1 = plt.subplot(221)
    plt.grid()
    ax1.set_title('{x(t),y(t)}')
    plt.plot([p.x for p in points], [p.y for p in points], '-')
    ax2 = plt.subplot(222)
    plt.grid()
    ax2.set_title('interpolated by len')
    plt.plot([p.x for p in int_points], [p.y for p in int_points], '*')
    ax3 = plt.subplot(223)
    plt.grid()
    ax3.set_title('fast interpolation')
    plt.plot([p.x for p in points], [p.y for p in points], '-')
    plt.plot([p.x for p in int_points], [p.y for p in int_points], '*')
    ax4 = plt.subplot(224)
    plt.grid()
    ax4.set_title('line interpolation using step calibration (naive approach)')
    # ax4.set_title('interpolation vs sampling')
    # count_of_samples = 15
    # multiplication_kof = 12
    # test_samples = alg.sampling(fx, fy, t0, t_max, (t_max - t0) / count_of_samples)
    # test_points = alg.interpolation_spline(test_samples, multiplication_kof)
    # plt.plot([p.x for p in test_points], [p.y for p in test_points], '-')
    # plt.plot([p.x for p in test_samples], [p.y for p in test_samples], '*')
    #
    # plt.figure(2)
    print()
    start_time = time.time()
    interpolated = interpolate_by_length()
    total_time = int(round((time.time() - start_time) * 1000))
    print('evaluation time for accurate line interpolation with const segment length: ',total_time)
    plt.plot([p.x for p in points], [p.y for p in points], '-')
    plt.plot(interpolated['x'], interpolated['y'], '*-')
    plt.show()
    print('done')


__init__()

'''
new alg description:
1) interpolation by t with minimal shift of t
2) line or spline interpolation 
3) shift by length using 
'''
